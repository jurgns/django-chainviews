from django.db.models import Model
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

def model_base(qs, key='qs'):
    def _model_base(request, c):
        if isinstance(qs, Model):
            c[key] = qs.objects.all()
        elif isinstance(qs, QuerySet):
            c[key] = qs
        else:
            raise Exception
        return c
    return _model_base

def filter(fields, qs='qs', query_key='q'):
    def _filter(request, c):
        pass
    return _filter

def get_object(qs='qs', key='id', pk='pk', template_object_name='obj'):
    def _get_object(request, c):
        # qs can be one of the following: Model, query, key for qs in vars
        if isinstance(qs, (Model, QuerySet)):
            d = {pk: c[key]}
            c[template_object_name] = get_object_or_404(qs, **d)
        elif isinstance(qs, str):
            c[template_object_name] = c[qs]
        else:
            raise Exception
        d = {c[field]: key}
        c[template_object_name] = qs.get(**d)
        return c
    return _get_object

def edit(Form, key='obj', method='POST'):
    def _edit(request, c):
        edit_form = Form(request.__getattribute__(method) or None, instance=c[key])
        if edit_form.is_valid():
            c[key] = edit_form.save()
            # redirect?
        return c 

def template(template_path):
    def _template(request, c):
        c['template_path'] = template_path
        return c
    return _template

def render(request, c):
    return render_to_response(c['template_path'], c)

def chain_view(*partials):
    def _chain(request, **kwargs):
        r, c = request, kwargs
        for partial in partials:
            r, c = partial(r, c)
            if isinstance(c, HttpResponse):
                return c
        return c 
        
