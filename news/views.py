from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views.generic import ListView

from news.models import Like, Post

COMMENTS_PER_LIST = 3


class PostsListView(LoginRequiredMixin, ListView):
    template_name = 'main.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        """Return a queryset sorted by a date of creation in descending order.
        If the parameter 'Sort by' is defined, returns a queryset according to
        this parameter."""
        q = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by')
        queryset = Post.objects.all().order_by('-when_created')
        if q:
            queryset = Post.objects.filter(text__contains=q)
        elif sort_by and len(sort_by) > 0:
            sort_by = sort_by.lower()
            if sort_by == 'country':
                queryset = Post.objects.all().order_by(
                    'author__profile__country')
            if sort_by == 'city':
                queryset = Post.objects.all().order_by('author__profile__city')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostsListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by')
        if q:
            context['q'] = q
        elif sort_by:
            context['sort_by'] = sort_by
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        # Paginate comments
        comments_list = self.object.comments.order_by('-published')
        paginator = Paginator(comments_list, COMMENTS_PER_LIST)
        page = self.request.GET.get('page')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        context['comments'] = comments
        return context


class HttpResponseSeeOther(HttpResponseRedirect):
    status_code = 303


@login_required
@require_POST
def like_add(request):
    """Function adds like to a post. If the post already has like from this
    user, function deletes user's like for the post."""
    content_type = request.POST.get('content_type', None)
    object_id = request.POST.get('object_id', None)
    if content_type and object_id:
        content_type = ContentType.objects.get_for_id(content_type)
        try:
            content_type.get_object_for_this_type(pk=object_id)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()
        like_queryset = Like.objects.filter(author=request.user,
                                            content_type=content_type,
                                            object_id=object_id)

        if like_queryset.exists():
            like_queryset.delete()
            return JsonResponse({"removed_like": True}, status=200)
        new_like = Like(author=request.user,
                        content_type=content_type,
                        object_id=object_id)
        new_like.save()
        return JsonResponse({"added_like": True}, status=200)
    return JsonResponse({}, status=404)
