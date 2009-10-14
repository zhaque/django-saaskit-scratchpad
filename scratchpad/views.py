
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django import forms
from django.template import RequestContext



from muaccounts  import models as muamodels
from scratchpad import models
from scratchpad.forms import AddScratchpadForm, AddToScratchpad
from todo.forms import AddListForm, AddItemForm, EditItemForm
from todo import models as todomodels
from threadedcomments import models as tmodels
import datetime

@login_required
def view_list(request):
    """ List all scratchpads a site has """

    # Get all scratchpads connected via muaccounts with this user

    # get account scratchpads only if we have a muaccount!
    if getattr(request,"muaccount",False):

        pads = models.Scratchpad.objects.filter(account=request.muaccount)
    else:
        pads = None

    form = AddScratchpadForm()
    return render_to_response("scratchpad/list_scratchpads.html", locals(), context_instance=RequestContext(request))

@login_required
def new_scratchpad(request):
    """ Shows new scratchpad form and does the actual form processing """
    
    if request.POST:
        form = AddScratchpadForm(request.POST)
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
        #return HttpResponseRedirect(reverse('scratchpad-list'))
        return HttpResponseRedirect(reverse('scratchpad-scratchpad_view',args=[item.id]))


    form = AddScratchpadForm()
    return render_to_response("scratchpad/new_scratchpad.html", locals(), context_instance=RequestContext(request))

@login_required
def del_item(request, item_id):
    """Delete an item from a scratchpad """

    #if request.POST:
    item = get_object_or_404(models.Item,id=item_id)
    pad_id = item.scratchpad.id
    item.delete()

    return HttpResponseRedirect(reverse('scratchpad-scratchpad_view',args=[pad_id]))

    #else:
        #item = get_object_or_404(models.Item,id=item_id)
        #task_list = todomodels.Item.objects.filter(list=item.scratchpad.tasks_list.id, list__account=request.muaccount, completed=0)
        # Get all scratchpads connected via muaccounts with this user

        # get account scratchpads only if we have a muaccount!
        #if getattr(request,"muaccount",False):

        #    pads = models.Scratchpad.objects.filter(account=request.muaccount)
        #else:
        #    pads = None
        #form = AddScratchpadForm()
        
        #return render_to_response("scratchpad/confirmdel_scratchpad_item.html", locals(), context_instance=RequestContext(request))

@login_required
def scratchpad_del(request, scratch_id):
    """ Delete a scratchpad """

    #if request.POST:
    pad = get_object_or_404(models.Scratchpad,id=scratch_id)
    pad.delete()

    return HttpResponseRedirect(reverse('scratchpad-list'))

    #else:
        #pad = get_object_or_404(models.Scratchpad,id=scratch_id)
        #task_list = todomodels.Item.objects.filter(list=pad.tasks_list.id, list__account=request.muaccount, completed=0)
        # Get all scratchpads connected via muaccounts with this user

        # get account scratchpads only if we have a muaccount!
        #if getattr(request,"muaccount",False):

            #pads = models.Scratchpad.objects.filter(account=request.muaccount)
        #else:
            #pads = None
        #form = AddScratchpadForm()
        #return render_to_response("scratchpad/confirmdel_scratchpad.html", locals(), context_instance=RequestContext(request))

@login_required
def scratchpad(request, scratch_id):
    """ Shows list items in a scratchpad """
    pad = get_object_or_404(models.Scratchpad,id=scratch_id)
    list = get_object_or_404(todomodels.List, slug=pad.tasks_list.slug)
    listid = list.id

    # Get all scratchpads connected via muaccounts with this user

    # get account scratchpads only if we have a muaccount!
    if getattr(request,"muaccount",False):

        pads = models.Scratchpad.objects.filter(account=request.muaccount)
    else:
        pads = None
    form = AddScratchpadForm()
    
    thedate = datetime.datetime.now()
    created_date = "%s-%s-%s" % (thedate.year, thedate.month, thedate.day)
    
    task_list = todomodels.Item.objects.filter(list=list.id, list__account=request.muaccount, completed=0)

    if request.POST.getlist('add_task') :
        form1 = AddItemForm(list, request.muaccount, request.POST,initial={
        'assigned_to':request.user.id,
        'priority':999,
        })

        if form1.is_valid():
            # Save task first so we have a db object to play with
            new_task = form1.save()

            # Send email alert only if the Notify checkbox is checked AND the assignee is not the same as the submittor
            # Email subect and body format are handled by templates
            if "notify" in request.POST :
                if new_task.assigned_to != request.user :

                    # Send email
                    email_subject = render_to_string("todo/email/assigned_subject.txt", { 'task': new_task })
                    email_body = render_to_string("todo/email/assigned_body.txt", { 'task': new_task, 'site': current_site, })
                    try:
                        send_mail(email_subject, email_body, new_task.created_by.email, [new_task.assigned_to.email], fail_silently=False)
                    except:
                        request.user.message_set.create(message="Task saved but mail not sent. Contact your administrator." )

            request.user.message_set.create(message="New task \"%s\" has been added." % new_task.title )
            return HttpResponseRedirect(request.path)
        else:
            print form1.errors
            #for error in form1.errors:
             #   request.user.message_set.create(message=error[1])           
    else:      
        form1 = AddItemForm(list, request.muaccount, initial={
            'assigned_to':request.user.id,
            'priority':999,
            } )

    if request.POST:
        if request.POST['scratchpad_type']:
            item = models.Item()
            item.notes = request.POST['content']
            item.title = request.POST['title']

            if request.POST['scratchpad_type'] == 'new':
                spad = models.Scratchpad()
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
                request.user.message_set.create(message="New Note added to '%s'" % spad.title)
            else:
                item.scratchpad = models.Scratchpad.objects.get(id=request.POST['scratchpad'])
                request.user.message_set.create(message="New Note added to '%s'" % item.scratchpad.title)

            item.save()


            strcomment = request.POST['comment']
            if strcomment != "":
                comment = tmodels.ThreadedComment()
                comment.content_object = item
                comment.user = request.user
                comment.comment = strcomment
                comment.save()
    
    form2 = AddToScratchpad(None, request.muaccount)
    comment = forms.CharField(widget=forms.Textarea).widget.render("comment","")

    return render_to_response("scratchpad/view_scratchpad.html", locals(), context_instance=RequestContext(request))

@login_required
def scratchpad_items(request, scratch_id):
    return HttpResponseRedirect(reverse('scratchpad-list-index'))

@login_required
def add_to(request):
    """ Show add-to form"""

    if request.POST:
        data = request.POST['data']

        form = AddToScratchpad(data, request.muaccount)
        comment = forms.CharField(widget=forms.Textarea).widget.render("comment","")

        # Get all scratchpads connected via muaccounts with this user

        # get account scratchpads only if we have a muaccount!
        if getattr(request,"muaccount",False):

            pads = models.Scratchpad.objects.filter(account=request.muaccount)
        else:
            pads = None

        scrapform = AddScratchpadForm()

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
            #print "es new"
            spad = models.Scratchpad()
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
            #print "es select"
            item.scratchpad = models.Scratchpad.objects.get(id=request.POST['scratchpad'])

        item.save()


        strcomment = request.POST['comment']
        if strcomment != "":

            #comment = models.ItemComment()
            #comment.item = item
            #comment.text = strcomment
            #comment.author = request.user
            #comment.save()

            comment = tmodels.ThreadedComment()
            comment.content_object = item
            comment.user = request.user
            comment.comment = strcomment
            comment.save()


        return HttpResponseRedirect(reverse('scratchpad-scratchpad_view',args=[item.scratchpad.id]))
    else:
        return HttpResponseRedirect(reverse('scratchpad-list'))

@login_required
def item(request, item_id):
    """ Shows scratchpad item details """
    item = get_object_or_404(models.Item,id=item_id)
    list = get_object_or_404(todomodels.List, slug=item.scratchpad.tasks_list.slug)

    # Get all scratchpads connected via muaccounts with this user

    # get account scratchpads only if we have a muaccount!
    if getattr(request,"muaccount",False):

        pads = models.Scratchpad.objects.filter(account=request.muaccount)
    else:
        pads = None

    scrapform = AddScratchpadForm()
    task_list = todomodels.Item.objects.filter(list=list.id, list__account=request.muaccount, completed=0)

    return render_to_response("scratchpad/view_scratchpad_item.html", locals(), context_instance=RequestContext(request))

def test(request):
    """ Test page of add-to scratchpad tag """

    return render_to_response("scratchpad/test.html", locals(), context_instance=RequestContext(request))

