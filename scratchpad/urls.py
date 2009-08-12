from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^list/$', 'scratchpad.views.view_list',name='scratchpad-list'),
    url(r'^new/$', 'scratchpad.views.new_scratchpad',name="scratchpad-new"),
    url(r'^(?P<scratch_id>\d)/$', 'scratchpad.views.scratchpad',name="scratchpad-scratchpad_view"),

    url(r'^add/$', 'scratchpad.views.add_to',name="scratchpad-addto"),
    url(r'^add/save/$', 'scratchpad.views.save',name="scratchpad-save"),
    url(r'^item/(?P<item_id>\d)/$', 'scratchpad.views.item',name="scratchpad-item"),





    url(r'^test/$','scratchpad.views.test')
)

