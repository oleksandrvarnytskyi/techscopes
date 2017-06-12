from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from comments.forms import CommentForm
from comments.models import Comment


class HttpResponseSeeOther(HttpResponseRedirect):
    status_code = 303


@login_required
@require_POST
def add_comment(request):
    """Check if object for commenting exists. If it is so redirects to the
    object page. If an object is a comment redirects to an object which has
    this comment"""
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        try:
            obj = comment.content_type.get_object_for_this_type(
                pk=comment.object_id)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()
        comment.author = request.user
        comment.save()
        if isinstance(obj, Comment):
            return HttpResponseSeeOther(obj.content_object.get_absolute_url())
        else:
            return HttpResponseSeeOther(obj.get_absolute_url())
    else:
        return HttpResponseBadRequest()
