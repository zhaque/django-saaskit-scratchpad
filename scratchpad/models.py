from django.db import models
from django.contrib.auth.models import User,Group
from muaccounts  import models as muamodels
from todo import models as todomodels
# Create your models here.


class Scratchpad(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    account = models.ForeignKey(muamodels.MUAccount)
    tasks_list = models.ForeignKey(todomodels.List)

    def __unicode__(self):
        return self.title


    class Meta:
        unique_together = ("account", "title")


class Item(models.Model):
    scratchpad = models.ForeignKey(Scratchpad)
    title = models.CharField(max_length=200)
    notes = models.TextField()

    def __unicode__(self):
        return self.title


class ItemComment(models.Model):
    item = models.ForeignKey(Item)
    author = models.ForeignKey(User)
    text = models.TextField()
    parent = models.ForeignKey("ItemComment",null=True,default=None)

    def __unicode__(self):
        return "%s: %s" % (self.author, self.text)