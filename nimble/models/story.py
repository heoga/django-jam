from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import reversion
from polymorphic.models import PolymorphicModel
from markdownx.models import MarkdownxField


@reversion.register()
class Story(PolymorphicModel):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = MarkdownxField(default='')
    typename = 'Story'

    def name(self):
        return '{}{:0>5}'.format(self.ident, self.id)

    def api_url(self):
        return reverse(self.api_detail_name, kwargs={
            'pk': self.pk,
        })

    @classmethod
    def api_keys(cls):
        return ['url', 'author', 'title', 'description']

    @classmethod
    def api_list_url(cls):
        return reverse(cls.api_list_name)

    @classmethod
    def create(cls, author, **kwargs):
        with reversion.create_revision():
            created_object = cls.objects.create(
                author=author, **kwargs
            )
            reversion.set_user(author)
            reversion.set_comment(
                "Created {}".format(cls.typename)
            )
        return created_object

    def update(self, user, data):
        with reversion.create_revision():
            for key, value in data.items():
                setattr(self, key, value)
            self.save()
            reversion.set_user(user)
            reversion.set_comment(
                "Edited {} through web".format(self.typename)
            )
