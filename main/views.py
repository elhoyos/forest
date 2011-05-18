from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from pagetree.helpers import get_hierarchy, get_section_from_path, get_module, needs_submit, submitted
from django.template import RequestContext


class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items

        return rendered_func

@rendered_with('main/page.html')
def page(request,path):
    hierarchy = request.get_host()
    section = get_section_from_path(path,hierarchy=hierarchy)
    # TODO: handle POST requests for quiz type blocks
    root = section.hierarchy.get_root()
    module = get_module(section)
    return dict(section=section,
                module=module,
                modules=root.get_children(),
                root=section.hierarchy.get_root()
                )

def instructor_page(request,path):
    return HttpResponse("instructor page")

@rendered_with('main/edit_page.html')
def edit_page(request,path):
    hierarchy = request.get_host()
    section = get_section_from_path(path,hierarchy=hierarchy)
    return dict(section=section,
                module=get_module(section),
                root=section.hierarchy.get_root())

