from django.conf.urls import url

from .views import PostDetailView, like_add


urlpatterns = [
    url(
        r'^post-detail/(?P<pk>\d+)/$',
        PostDetailView.as_view(),
        name='post_detail',
    ),
    url(
        r'^likes/$',
        like_add,
        name='like_add',
    ),
]
