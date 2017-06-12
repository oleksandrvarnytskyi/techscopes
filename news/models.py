from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from comments.models import Comment


class Like(models.Model):
    when_created = models.DateTimeField(
        'When created',
        auto_now_add=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='likes'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ('post',)}
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __unicode__(self):
        return '%s - author: %s' % (self.content_type.name,
                                    self.author.username)


class PostManager(models.Manager):
    def news(self, *args, **kwargs):
        kwargs['rubric'] = self.model.NEWS
        return self.filter(*args, **kwargs)


class Post(models.Model):
    NEWS = 'NEWS'
    RUBRIC_CHOICES = (
        (NEWS, 'News'),
    )
    when_created = models.DateTimeField(
        'When created',
        auto_now_add=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='posts'
    )
    title = models.CharField('Title', max_length=100)
    text = models.TextField('Text')
    rubric = models.CharField(
        max_length=10,
        verbose_name='Rubric',
        choices=RUBRIC_CHOICES,
        blank=True
    )
    image = models.ImageField('Image', upload_to='post_news',
                              blank=True, null=True)
    comments = GenericRelation(Comment, related_query_name='posts')
    likes = GenericRelation(Like, related_query_name='posts')
    objects = PostManager()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __unicode__(self):
        return '%s - author: %s' % (self.title, self.author.username)

    def get_absolute_url(self):
        return reverse('news:post_detail', args=(self.pk,))

    def get_content_type(self):
        return ContentType.objects.get_for_model(self).id

    def get_comments_amount(self):
        return self.comments.count() + \
               sum(comment.reply.count() for comment in self.comments.all())
