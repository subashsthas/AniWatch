from django.contrib import admin

# Register your models here.
from .models import Series, Movies, Genres, Titles, Contact, Watched


class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'season', 'episode', 'language', 'uploaded_date')


class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'language', 'uploaded_date')


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'uploaded_date')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'short_message')


admin.site.register(Series, SeriesAdmin)
admin.site.register(Movies, MoviesAdmin)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(Genres)
admin.site.register(Watched)
admin.site.register(Contact, ContactAdmin)
