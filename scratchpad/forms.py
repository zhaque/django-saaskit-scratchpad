from django.db import models
from django import forms
from django.forms import ModelForm, widgets
from django.contrib.auth.models import User,Group
from scratchpad.models import Scratchpad, Item
import datetime


class AddScratchpadForm(ModelForm):

    class Meta:
        model = Scratchpad
        exclude = ('account','author','tasks_list')


class AddToScratchpad(ModelForm):

    def __init__(self, data, muaccount, *args, **kwargs):
        super(AddToScratchpad, self).__init__(*args, **kwargs)
        self.fields['notes'].initial = data
        self.fields['notes'].widget = widgets.HiddenInput()
        self.fields['scratchpad'].queryset = Scratchpad.objects.filter(account=muaccount)
        self.fields['scratchpad'].label = "Scratchpad"




    class Meta:
        model = Item