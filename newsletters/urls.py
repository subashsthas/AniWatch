from django.conf.urls import url
from .import views


app_name = "newsletters"


urlpatterns = [
    url('newsletter/subscribe', views.newsletter_subscribe, name="newsletter_subscribe"),
    url('newsletter/unsubscribe', views.newsletter_unsubscribe, name="newsletter_unsubscribe"),
]