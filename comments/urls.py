from django.conf.urls import url

from .views import add_comment


urlpatterns = [
    url(
        r'^$',
        add_comment,
        name='add_comment'
    ),
]
