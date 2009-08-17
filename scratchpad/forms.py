from django.db import models
from django import forms
from django.forms import ModelForm, widgets
from django.contrib.auth.models import User,Group
from scratchpad.models import ScratchPad, Item
import datetime


class AddScratchPadForm(ModelForm):

    class Meta:
        model = ScratchPad
        exclude = ('account','author','tasks_list')


class AddToScratchPad(ModelForm):

    def __init__(self, data, muaccount, *args, **kwargs):
        super(AddToScratchPad, self).__init__(*args, **kwargs)
        self.fields['notes'].initial = data
        self.fields['notes'].widget = widgets.HiddenInput()
        self.fields['scratchpad'].queryset = ScratchPad.objects.filter(account=muaccount)
        self.fields['scratchpad'].label = "Scratchpad"




    class Meta:
        model = Item