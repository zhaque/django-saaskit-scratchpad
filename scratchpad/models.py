from django.db import models
from django.contrib.auth.models import User,Group
from muaccounts  import models as muamodels
# Create your models here.


class ScratchPad(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    account = models.ForeignKey(muamodels.MUAccount)

    def __unicode__(self):
        return self.title


class Item(models.Model):
    scratchpad = models.ForeignKey(ScratchPad)
    title = models.CharField(max_length=200)
    notes = models.TextField()

    def __unicode__(self):
        return self.title


class ItemComment(models.Model):
    item = models.ForeignKey(Item)
    author = models.ForeignKey(User)
    text = models.TextField()

    def __unicode__(self):
        return "%s: %s" % (self.author, self.text)