
from django.urls import path
from .import views

app_name = "main"


urlpatterns = [
    path('', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path("videos/<str:title>/<int:title_id>", views.videoView, name="VideoView"),
    path('search', views.search, name='search'),
    path('terms', views.terms, name='terms'),
    path('privacy', views.privacy, name='privacy'),
    path('movies/', views.movies, name='movies'),
    path('series/', views.series, name='series'),
    # path('donation/', views.donation, name='donation'),
    # path('charge/', views.charge, name='charge'),
    # path('success/<str:args>/', views.successMsg, name='success'),
]
