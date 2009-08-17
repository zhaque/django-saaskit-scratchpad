
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django import forms
from django.template import RequestContext



from muaccounts  import models as muamodels
from scratchpad import models
from scratchpad.forms import AddScratchPadForm, AddToScratchPad
from todo import models as todomodels

@login_required
def view_list(request):
    """ List all scratchpads a site has """

    # Get all scratchpads connected via muaccounts with this user

    # get account scratchpads only if we have a muaccount!
    if getattr(request,"muaccount",False):

        pads = models.ScratchPad.objects.filter(account=request.muaccount)
    else:
        pads = None

    form = AddScratchPadForm()
    return render_to_response("scratchpad/list_scratchpads.html", locals(), context_instance=RequestContext(request))

@login_required
def new_scratchpad(request):
    """ Shows new scratchpad form and does the actual form processing """

    if request.POST:
        form = AddScratchPadForm(request.POST)
        item = form.save(commit=False)
        item.account=request.muaccount
        item.author=request.user

        newtodo = todomodels.List()
        newtodo.name = item.title
        newtodo.slug = "Tasks for scratchpad %s" % item.title
        newtodo.account = request.muaccount
        newtodo.save()
        item.tasks_list = newtodo
        item.save()
        return HttpResponseRedirect(reverse('scratchpad-list'))



    form = AddScratchPadForm()
    return render_to_response("scratchpad/new_scratchpad.html", locals(), context_instance=RequestContext(request))

@login_required
def del_item(request, item_id):
    """Delete an item from a scratchpad """

    if request.POST:
        item = get_object_or_404(models.Item,id=item_id)
        pad_id = item.scratchpad.id
        item.delete()

        return HttpResponseRedirect(reverse('scratchpad-list'))

    else:
        item = get_object_or_404(models.Item,id=item_id)

        return render_to_response("scratchpad/confirmdel_scratchpad_item.html", locals(), context_instance=RequestContext(request))

@login_required
def scratchpad_del(request, scratch_id):
    """ Delete a scratchpad """

    if request.POST:
        pad = get_object_or_404(models.ScratchPad,id=scratch_id)
        pad.delete()

        return HttpResponseRedirect(reverse('scratchpad-list'))

    else:
        pad = get_object_or_404(models.ScratchPad,id=scratch_id)

        return render_to_response("scratchpad/confirmdel_scratchpad.html", locals())

@login_required
def scratchpad(request, scratch_id):
    """ Shows list items in a scratchpad """
    pad = get_object_or_404(models.ScratchPad,id=scratch_id)

    return render_to_response("scratchpad/view_scratchpad.html", locals())

@login_required
def add_to(request):
    """ Show add-to form"""

    if request.POST:
        data = request.POST['data']

        form = AddToScratchPad(data, request.muaccount)
        comment = forms.CharField(widget=forms.Textarea).widget.render("comment","")

        return render_to_response("scratchpad/addto_scratchpad.html", locals())
    else:
        return HttpResponseRedirect(reverse('scratchpad-list'))

@login_required
def save(request):
    """ Save item sent via add-to form """

    if request.POST:
        item = models.Item()
        item.notes = request.POST['notes']
        item.title = request.POST['title']

        if request.POST['scratchpad_type'] == 'new':
            print "es new"
            spad = models.ScratchPad()
            spad.title = request.POST['new_scratchpad']
            spad.author = request.user
            spad.account = request.muaccount

            newtodo = todomodels.List()
            newtodo.name = spad.title
            newtodo.slug = "Tasks for scratchpad %s" % spad.title
            newtodo.account = request.muaccount
            newtodo.save()

            spad.tasks_list = newtodo
            spad.save()
            item.scratchpad = spad
        else:
            print "es select"
            item.scratchpad = models.ScratchPad.objects.get(id=request.POST['scratchpad'])

        item.save()


        strcomment = request.POST['comment']
        if strcomment != "":

            comment = models.ItemComment()
            comment.item = item
            comment.text = strcomment
            comment.author = request.user
            comment.save()

        return HttpResponseRedirect(reverse('scratchpad-scratchpad_view',args=[item.scratchpad.id]))
    else:
        return HttpResponseRedirect(reverse('scratchpad-list'))

@login_required
def item(request, item_id):
    """ Shows scratchpad item details """
    item = get_object_or_404(models.Item,id=item_id)


    return render_to_response("scratchpad/view_scratchpad_item.html", locals(), context_instance=RequestContext(request))

def test(request):
    """ Test page of add-to scratchpad tag """

    return render_to_response("scratchpad/test.html", locals(), context_instance=RequestContext(request))

