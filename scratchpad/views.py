
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django import forms



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
    return render_to_response("scratchpad/list_scratchpads.html", locals())

def new_scratchpad(request):

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
    return render_to_response("scratchpad/new_scratchpad.html", locals())

def del_item(request, item_id):

    if request.POST:
        item = get_object_or_404(models.Item,id=item_id)
        pad_id = item.scratchpad.id
        item.delete()

        return HttpResponseRedirect(reverse('scratchpad-list'))

    else:
        item = get_object_or_404(models.Item,id=item_id)

        return render_to_response("scratchpad/confirmdel_scratchpad_item.html", locals())

def scratchpad_del(request, scratch_id):
    if request.POST:
        pad = get_object_or_404(models.ScratchPad,id=scratch_id)
        pad.delete()

        return HttpResponseRedirect(reverse('scratchpad-list'))

    else:
        pad = get_object_or_404(models.ScratchPad,id=scratch_id)

        return render_to_response("scratchpad/confirmdel_scratchpad.html", locals())

def scratchpad(request, scratch_id):

    pad = get_object_or_404(models.ScratchPad,id=scratch_id)

    return render_to_response("scratchpad/view_scratchpad.html", locals())

def add_to(request):


    if request.POST:
        data = request.POST['data']

        form = AddToScratchPad(data, request.muaccount)
        comment = forms.CharField(widget=forms.Textarea).widget.render("comment","")

        return render_to_response("scratchpad/addto_scratchpad.html", locals())
    else:
        return HttpResponseRedirect(reverse('scratchpad-list'))

def save(request):

    if request.POST:
        item = models.Item()
        item.notes = request.POST['notes']
        item.title = request.POST['title']
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

def item(request, item_id):

    item = get_object_or_404(models.Item,id=item_id)


    return render_to_response("scratchpad/view_scratchpad_item.html", locals())

def test(request):

    return render_to_response("scratchpad/test.html", locals())

