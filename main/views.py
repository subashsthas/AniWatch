from itertools import chain
import itertools

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Movies, Series, Titles, Contact, Watched
from django.core.paginator import Paginator, EmptyPage
import datetime

from django.contrib import messages
import operator

from django.urls import reverse

import pandas as pd
import pickle


# reading csv files
def data():
    # load the database
    anime_db = pd.read_csv('static/data/MAL_final.csv')
    return anime_db


# reading Ai model generated from jupyter file
def Model():
    # oad saved model
    pkl_file = open('static/data/anime_indices.pkl', 'rb')
    indices = pickle.load(pkl_file)
    return indices


def pickle_predictions(indices):
    with open('anime_indices.pkl', 'wb') as fid:
        pickle.dump(indices, fid, 2)


# declare list to add list of similar anime
lis = []


# recommendation calculating
def similar_anime_content(query, indices, anime_db):
    try:
        if query not in anime_db['name']:
            N = anime_db[anime_db['name'] == query].index[0]
            # print('Similar Anime to "{}"----------------:'.format(query))
            for n in indices[N]:
                if query not in anime_db.loc[n]['name']:
                    # print('{}'.format(anime_db.loc[n]['name']))
                    lis.append(anime_db.loc[n]['name'])
            # print(lis)
        else:
            print('The anime {} does not exist in our database.'.format(query))
    except IndexError as error:
        # Output expected IndexErrors.
        print('The anime {} does not exist in our database.'.format(query))


# Views for home page
def home(request):
    # recommendation area
    if request.user.is_authenticated:
        watch = Watched.objects.filter(user=request.user)
        try:
            for ser in watch:
                seriesList = ser.serie.all().distinct('title_id')
            for mov in watch:
                moviesList = mov.movie.all().distinct('title_id')
            animeList = list(chain(seriesList, moviesList))
            # print(animeList)
            for index, item in enumerate(animeList):
                # print(item)
                title = str(item)
                similar_anime_content(title, Model(), data())

            recMov = Movies.objects.filter(title__title__in=lis).distinct('title')
            recSer = Series.objects.filter(title__title__in=lis).distinct('title')
            recommend = list(chain(recSer, recMov))
            Recommend = sorted(recommend, key=operator.attrgetter('views'), reverse=True)[:20]
        except NameError as error:
            Recommend = None
    else:
        Recommend = None
    # end recommendation

    # take a time interval of week
    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    # series part
    trends = Series.objects.filter(uploaded_date__gte=week_ago).order_by('title', '-views').distinct('title')
    trend = sorted(trends, key=operator.attrgetter('views'), reverse=True)
    series = Series.objects.order_by('title', '-uploaded_date').distinct('title')
    result = sorted(series, key=operator.attrgetter('uploaded_date'), reverse=True)
    populars = Series.objects.order_by('title', '-views').distinct('title')
    popular = sorted(populars, key=operator.attrgetter('views'), reverse=True)
    # series part end

    # movies part
    movies = Movies.objects.order_by('-uploaded_date')
    trend_mov = Movies.objects.filter(uploaded_date__gte=week_ago).order_by('-views')
    pop_mov = Movies.objects.order_by('-views')
    # movies part end

    # releasing soon
    rel_series = Series.objects.values_list('title_id', flat=True)
    rel_movies = Movies.objects.values_list('title_id', flat=True)
    not_release = list(chain(rel_series, rel_movies))
    releasing = Titles.objects.exclude(title_id__in=not_release)
    # end releasing soon

    # combining series and movies
    combined = itertools.chain(result, movies)
    combined_trend = list(chain(trend, trend_mov))
    combined_popular = list(chain(popular, pop_mov))
    all = sorted(combined, key=operator.attrgetter('uploaded_date'), reverse=True)
    trend_all = sorted(combined_trend, key=operator.attrgetter('views'), reverse=True)
    pop_all = sorted(combined_popular, key=operator.attrgetter('views'), reverse=True)
    # combining end

    # passing to templates
    context = {
        'result': all[:10],
        'trend': trend_all[:10],
        'popular': pop_all[:20],
        'reco': Recommend,
        'releasing': releasing
    }
    return render(request, 'home.html', context)


# Contact Us
@login_required(login_url='/login')
def contact(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        # passing message if the requested work is done
        messages.info(request,
                      'Thank You For Your Feedback. We will look into your message and get back to you as soon as possible.')
        contact.name = name
        contact.email = email
        contact.message = message
        contact.save()
        return redirect('main:contact')

    else:
        return render(request, 'contactUs.html')


# about us page
def about(request):
    return render(request, 'aboutUs.html')


# movies page
def movies(request):
    movies = Movies.objects.all().order_by('title').distinct('title')
    p = Paginator(movies, 20)

    page_num = request.GET.get('page', 1)

    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context = {
        'movies': page,
    }
    return render(request, 'movies.html', context)


# series page
def series(request):
    series = Series.objects.all().order_by('title').distinct('title')
    p = Paginator(series, 20)

    page_num = request.GET.get('page', 1)

    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context = {
        'series': page,
    }
    return render(request, 'series.html', context)


# page to watch movies and anime
def videoView(request, title, title_id):
    movie = Movies.objects.filter(title_id=title_id)
    # view count + 1 for movies
    for entry in movie:
        entry.views = entry.views + 1
        entry.save()
        if request.user.is_authenticated:
            item_to_save = get_object_or_404(movie, title_id=title_id)
            # Check if the item already exists in that user watchlist
            if Watched.objects.filter(user=request.user, movie=title_id).exists():
                pass
            # Get the user watchlist or create it if it doesn't exists
            user_list, created = Watched.objects.get_or_create(user=request.user)
            # Add the item through the ManyToManyField (Watchlist => item)
            user_list.movie.add(item_to_save)
    # view count end

    series = Series.objects.filter(title_id=title_id)
    # pagination
    p = Paginator(series, 1)

    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    # pagination end

    # view count for series
    seriesone = Series.objects.filter(title_id=title_id).filter(episode=page_num)
    for entrys in seriesone:
        entrys.views = entrys.views + 1
        entrys.save()
        if request.user.is_authenticated:
            item_to_save = get_object_or_404(seriesone, title_id=title_id)
            # Check if the item already exists in that user watchlist
            if Watched.objects.filter(user=request.user, serie=title_id).exists():
                pass
            # Get the user watchlist or create it if it doesn't exists
            user_list, created = Watched.objects.get_or_create(user=request.user)
            # Add the item through the ManyToManyField (Watchlist => item)
            user_list.serie.add(item_to_save)
    # view count end
    return render(request, 'videoView.html', {'series': page, 'title': title, 'movie': movie})


# search query
def search(request):
    query = request.GET['query']
    movies = Movies.objects.filter(title__title__icontains=query)
    series = Series.objects.filter(title__title__icontains=query).distinct('title')

    videos = {
        'movies': movies,
        'series': series,
        'query': query,
    }
    return render(request, 'search.html', videos)


# terms and condition page
def terms(request):
    return render(request, 'TermsandCondition.html')


# privacy page
def privacy(request):
    return render(request, 'privacy.html')

# def donation(request):
#     return render(request, 'donation.html')
#
#
# def charge(request):
#     amount = 5
#     if request.method == 'POST':
#         print('Data:', request.POST)
#
#     return redirect(reverse('success'), args=[amount])
#
#
# def successMsg(request, args):
#     amount = args
#     return render(request, 'success.html', {'amount': amount})
