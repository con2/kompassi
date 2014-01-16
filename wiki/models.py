from django.db import models

from core.utils import SlugField


class Space(models.Model):
    slug = SlugField()
    title = models.CharField(max_length=255)


class Page(models.Model):
    path = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def current_version(self):
        return self.pageversion_set.filter(page=self).order_by('-created_at').first()



class PageVersion(models.Model):
    page = models.ForeignKey(Page)

    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(User)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
