from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^list/$', 'scratchpad.views.view_list',name='scratchpad-list'),
    url(r'^$', 'scratchpad.views.view_list',name='scratchpad-list-index'),
    url(r'^new/$', 'scratchpad.views.new_scratchpad',name="scratchpad-new"),
    url(r'^(?P<scratch_id>\d+)/$', 'scratchpad.views.scratchpad',name="scratchpad-scratchpad_view"),
    url(r'^(?P<scratch_id>\d+)/del$', 'scratchpad.views.scratchpad_del',name="scratchpad-delete"),
    url(r'^add/$', 'scratchpad.views.add_to',name="scratchpad-addto"),
    url(r'^add/save/$', 'scratchpad.views.save',name="scratchpad-save"),
    url(r'^item/(?P<item_id>\d+)/$', 'scratchpad.views.item', name="scratchpad-item"),
    url(r'^item/(?P<item_id>\d+)/del$', 'scratchpad.views.del_item',name="scratchpad-item-delete"),
    url(r'^not_available/$', direct_to_template, dict(template='not_available.html'), name="scratchpad-not-available"),




    url(r'^test/$','scratchpad.views.test')
)

