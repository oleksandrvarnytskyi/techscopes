from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from news.models import Post, Like


class LikeInline(GenericTabularInline):
    model = Like
    fields = ('author', 'when_created', )
    readonly_fields = ['when_created']
    extra = 0

admin.site.register(Like)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    inlines = [LikeInline]
    search_fields = ('title',)

admin.site.register(Post, PostAdmin)
