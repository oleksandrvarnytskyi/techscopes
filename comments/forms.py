from django.forms import ModelForm, HiddenInput
from comments.models import Comment


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text', 'reply_to', 'content_type', 'object_id', 'id')
        widgets = {
            'reply_to': HiddenInput(),
            'object_id': HiddenInput(),
            'content_type': HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['reply_to'].required = False
