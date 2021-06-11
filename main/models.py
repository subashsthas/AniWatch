from django.db import models
from django.template.defaultfilters import truncatechars
from django.contrib.auth.models import User

# Create your models here.
LANGUAGE_CHOICES = (
    ('sub', 'SUB'),
    ('dub', 'DUB'),
)

TYPE_CHOICES = (
    ('ova', 'OVA'),
    ('tv', 'TV'),
    ('ona', 'ONA'),
    ('special', 'SPECIAL'),
)


# model to save all the genre
class Genres(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre


# model to save all the titles
class Titles(models.Model):
    title_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="")
    thumbnail = models.ImageField(upload_to="video/thumbnail", default="")
    genre = models.ManyToManyField(Genres)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="Enter description", max_length=1000)

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'

    def __str__(self):
        return self.title


# model to save all the series
class Series(models.Model):
    series_id = models.AutoField(primary_key=True)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    type = models.CharField(max_length=8, choices=TYPE_CHOICES, default='tv')
    episode = models.IntegerField(default=1)
    season = models.IntegerField(default=1)
    language = models.CharField(max_length=6, choices=LANGUAGE_CHOICES, default='sub')
    uploaded_date = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to="video/uploaded/series", default='')
    views = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'series'
        verbose_name_plural = 'series'

    def __str__(self):
        return self.title.title


# model to save all movie
class Movies(models.Model):
    movies_id = models.AutoField(primary_key=True)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    type = models.CharField(max_length=6, editable=False, default='movie')
    language = models.CharField(max_length=6, choices=LANGUAGE_CHOICES, default='sub')
    uploaded_date = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to="video/uploaded/movies", default='')
    views = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = 'movies'
        verbose_name_plural = 'movies'

    def __str__(self):
        return self.title.title


# model to save all the messages send by the users
class Contact(models.Model):
    name = models.CharField(max_length=30, default='')
    email = models.EmailField()
    message = models.TextField(max_length=200, default='')

    @property
    def short_message(self):
        return truncatechars(self.message, 40)

    def __str__(self):
        return self.name


# models to save user watch history
class Watched(models.Model):
    movie = models.ManyToManyField(Movies)
    serie = models.ManyToManyField(Series)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s Watched"
