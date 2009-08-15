from django.template import Library, Node, TemplateSyntaxError
from django.template import Variable, resolve_variable
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
#from books.models import Book

register = Library()

def get_add_to_html(html_id):

    code = "<form action='%s' method='post' id='scratchpad_add_%s'>" % (reverse('scratchpad-addto'),html_id)
    code += "<a href='#' onclick='addToScratchPad(\"%s\");'>Add to Scratchpad</a>" % (html_id)
    code +="<input type='hidden' name='data' value=''></form>"

    return code



register.simple_tag(get_add_to_html)

