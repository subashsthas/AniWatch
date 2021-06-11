from django.contrib.admin.views.decorators import staff_member_required
from main.models import Movies, Series, Titles, Contact, Genres

from .forms import MoviesForm, SeriesForm, TitleForm, GenreForm, UserForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.

@staff_member_required
def studio(request):
    usercount = User.objects.all().count()
    seriescount = Series.objects.all().count()
    moviescount = Movies.objects.all().count()
    messagecount = Contact.objects.all().count()
    context = {
        'usercount': usercount,
        'seriescount': seriescount,
        'moviescount': moviescount,
        'messagecount': messagecount

    }
    return render(request, 'dashboard.html', context)


@staff_member_required
def A_user(request):
    user = User.objects.all().order_by('first_name')
    userform = UserForm(request.POST)
    if request.method == "POST" and 'adduser' in request.POST:
        if userform.is_valid():
            if User.objects.filter(email=request.POST['email']).exists():
                messages.info(request, 'Email Taken')
                return redirect('adminonly:A_user')
            elif User.objects.filter(username=request.POST['username']).exists():
                messages.info(request, 'Username Taken')
                return redirect('adminonly:A_user')
            else:
                userform.save()
                messages.info(request,
                              'New User has been added successfully.')
                return redirect('adminonly:A_user')

    context = {
        'user': user,
        'userform': userform
    }
    return render(request, 'A_user.html', context)


@staff_member_required
def delete_user(request, pk):
    if request.method == "POST" and 'delete' in request.POST:
        user = User.objects.get(id=pk)
        user.delete()
        messages.info(request, 'User Deleted')
        return redirect('/studio/user')
    elif request.method == "POST" and 'block' in request.POST:
        user = User.objects.get(id=pk)
        if user.is_active is False:
            user.is_active = True
            user.save()
            messages.info(request, 'User Unblocked')
            return redirect('/studio/user')
        else:
            user.is_active = False
            user.save()
            messages.info(request, 'User Blocked')
            return redirect('/studio/user')
    else:
        return redirect('/studio/user')


@staff_member_required
def A_genre(request):
    genre = Genres.objects.all().order_by('genre')
    genreform = GenreForm(request.POST)
    if request.method == "POST" and 'addgenre' in request.POST:
        if genreform.is_valid():
            genreform.save()
            messages.info(request,
                          'New Genre has been added successfully.')
            return redirect('adminonly:A_genre')
    context = {
        'genre': genre,
        'genreform': genreform
    }
    return render(request, 'A_genre.html', context)


@staff_member_required
def delete_genre(request, pk):
    genre = Genres.objects.get(pk=pk)
    genre.delete()
    messages.info(request, 'Deleted Successfully')
    return redirect('adminonly:A_genre')


@staff_member_required
def A_title(request):
    title = Titles.objects.all().order_by('title')
    titleform = TitleForm()
    if request.method == "POST" and 'addtitle' in request.POST:
        titleform = TitleForm(request.POST, request.FILES)
        if titleform.is_valid():
            titleform.save()
            messages.info(request,
                          'New Title has been added successfully.')
            return redirect('adminonly:A_title')
    context = {
        'title': title,
        'titleform': titleform
    }
    return render(request, 'A_title.html', context)


@staff_member_required
def delete_title(request, pk):
    title = Titles.objects.get(pk=pk)
    title.delete()
    messages.info(request, 'Deleted Successfully')
    return redirect('adminonly:A_title')


@staff_member_required
def A_movies(request):
    movies = Movies.objects.all().order_by('title')
    moviesform = MoviesForm()
    if request.method == "POST" and 'addmovies' in request.POST:
        moviesform = MoviesForm(request.POST, request.FILES)
        if moviesform.is_valid():
            moviesform.save()
            messages.info(request,
                          'New Movie has been added successfully.')
            return redirect('adminonly:A_movies')
    context = {
        'movies': movies,
        'moviesform': moviesform
    }
    return render(request, 'A_movies.html', context)


@staff_member_required
def delete_movies(request, pk):
    movies = Movies.objects.get(pk=pk)
    movies.delete()
    messages.info(request, 'Deleted Successfully')
    return redirect('adminonly:A_movies')


@staff_member_required
def A_series(request):
    series = Series.objects.all().order_by('title')
    seriesform = SeriesForm()
    if request.method == "POST" and 'addseries' in request.POST:
        seriesform = SeriesForm(request.POST, request.FILES)
        if seriesform.is_valid():
            seriesform.save()
            messages.info(request,
                          'New Series has been added successfully.')
            return redirect('adminonly:A_series')
    context = {
        'series': series,
        'seriesform': seriesform
    }
    return render(request, 'A_series.html', context)


@staff_member_required
def delete_series(request, pk):
    series = Series.objects.get(pk=pk)
    series.delete()
    messages.info(request, 'Deleted Successfully')
    return redirect('adminonly:A_series')


@staff_member_required
def A_contact(request):
    contact = Contact.objects.all()
    context = {
        'contact': contact
    }
    return render(request, 'A_contact.html', context)


@staff_member_required
def delete_message(request, pk):
    contact = Contact.objects.get(pk=pk)
    contact.delete()
    messages.info(request, 'One Message is Deleted Successfully')
    return redirect('adminonly:A_contact')
