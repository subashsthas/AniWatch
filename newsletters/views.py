from django.shortcuts import render

from .models import NewsletterUser
from .forms import NewsletterUserSignUpForm

from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 


# Create your views here.
def newsletter_subscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            messages.warning(request, 'Sorry! this email already exist',
                             "alert alert-warning alert-dismissible")
        else:
            instance.save()
            messages.success(request, 'Thank You, You are successfully subscribed to our Newsletter',
                             "alert alert-success alert-dismissible")
            subject = "Thank you for joining our newsletter"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            signup_message = """Welcome to AniWatch Newsletter. If you would like to unsubscribe visit http://127.0.0.1:8000/newsletter/unsubscribe"""
            send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=signup_message, fail_silently=False)
    context = {
        'form': form,
    }
    template = "subscribe.html"
    return render(request, template, context)


def newsletter_unsubscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request, 'You have been successfully unsubscribed from our Newsletter')
            subject = "AniWatch Newsletter Unsubscribed"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            signup_message = """You have been unsubscribed from AniWatch Newsletter. If you would like to subscribe visit http://127.0.0.1:8000/newsletter/subscribe"""
            send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=signup_message,
                      fail_silently=False)
        else:
            messages.warning(request, 'Sorry! this email does not exist', "alert alert-warning alert-dismissible")

    context = {
        'form': form,
    }
    template = "unsubscribe.html"
    return render(request, template, context)
