# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
    published = models.DateTimeField('When published',
                                     auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name='Author',
                               related_name='comments')
    text = models.CharField('Comment text', max_length=500)
    reply_to = models.ForeignKey('self', blank=True, null=True)
    is_hidden = models.BooleanField('Is hidden', default=False)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ('post', 'comment')}
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    reply = GenericRelation(
        'comments.Comment',
        related_query_name='comments'
    )

    class Meta:
        verbose_name = 'Comments'
        verbose_name_plural = 'Comment'

    def __unicode__(self):
        return '%s %s' % (self.author, self.text)

    def get_content_type(self):
        return ContentType.objects.get_for_model(self).id
