from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, _get_queryset

def detail(fields, template_var='fields'):
    def _detail(request, c):
        c[template_var] = fields
        return request, c
    return _detail

def list(fields, template_var='fields'):
    def _list(request, c):
        c[template_var] = fields
    return _list

def get_object(Model, request_key='id', model_pk='pk', template_object_name='obj'):
    def _get_object(request, c):
        qs = _get_queryset(Model)
        d = {model_pk: c[request_key]}
        c[template_object_name] = qs.get(**d)
        return request, c
    return _get_object

def get_list(Model, template_qs_name='qs'):
    def _get_list(request, c):
        qs = _get_queryset(Model)
        c[template_qs_name] = qs
        return request, c
    return _get_list

def edit(Form, template_form_name='edit_form', template_obj_name='obj', method='POST'):
    def _edit(request, c):
        edit_form = Form(request.__getattribute__(method) or None, instance=c[template_obj_name])
        if edit_form.is_valid():
            c[template] = edit_form.save()
            # redirect?
        return request, c 

def template(template_path):
    def _template(request, c):
        c['template_path'] = template_path
        return request, c
    return _template

def render(request, c):
    return request, render_to_response(c['template_path'], c)

def chain_view(*partials):
    def _chain_view(request, **kwargs):
        r, c = request, kwargs
        for partial in partials:
            r, c = partial(r, c)
            if isinstance(c, HttpResponse):
                return c
        return c 
    return _chain_view

