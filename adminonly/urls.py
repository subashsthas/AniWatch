from django.urls import path
from .import views


app_name = "adminonly"


urlpatterns = [
    path('studio/', views.studio, name="studio"),
    path('studio/user/', views.A_user, name="A_user"),
    path("studio/user/<int:pk>/", views.delete_user, name="delete_user"),

    path('studio/genre/', views.A_genre, name="A_genre"),
    path("studio/genre/<int:pk>/", views.delete_genre, name="delete_genre"),

    path('studio/title/', views.A_title, name="A_title"),
    path("studio/title/<int:pk>/", views.delete_title, name="delete_title"),

    path('studio/movies/', views.A_movies, name="A_movies"),
    path("studio/movies/<int:pk>/", views.delete_movies, name="delete_movies"),

    path('studio/series/', views.A_series, name="A_series"),
    path("studio/series/<int:pk>/", views.delete_series, name="delete_series"),

    path('studio/contact/', views.A_contact, name="A_contact"),
    path("studio/contact/<int:pk>/", views.delete_message, name="delete_message"),



]