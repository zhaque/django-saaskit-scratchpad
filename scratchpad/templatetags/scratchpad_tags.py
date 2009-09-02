from django.template import Library, Node, TemplateSyntaxError
from django.template import Variable, resolve_variable
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from todo.models import List, Item
#from books.models import Book

register = Library()

def get_add_to_html(html_id):

    code = "<form action='%s' method='post' id='scratchpad_add_%s'>" % (reverse('scratchpad-addto'),html_id)
    code += "<a href='#' onclick='addToScratchPad(\"%s\");'>Add to Scratchpad</a>" % (html_id)
    code +="<input type='hidden' name='data' value=''></form>"

    return code

def topitems(value, args):
    arglist = args.split(',')
    top = int(arglist[0])
    userid = arglist[1]
    useritems = value.item_set.get(assigned_to = userid)
    if len(useritems) < 3:
        for item in value.item_set:
            if len(useritems) == 3:
                break
            else:
                if item.assigned_to != userid:
                    useritems.item_set.append(item)
    return useritems

register.filter('topitems', topitems)

register.simple_tag(get_add_to_html)

