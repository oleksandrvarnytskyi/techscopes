from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('published', 'author', 'is_hidden')
    list_filter = ('is_hidden', 'content_type')
