from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, _get_queryset

def if_(condition, action):
    """
    Executes ``action`` on based on ``condition``.

    Both ``action`` and ``condition`` should be callables of the form f(request, c).
    """
    def _if_(request, c):
        if condition(request, c):
            return action(request, c)
        return request, c

def get_object(Model, request_key='id', model_pk='pk', template_object_name='obj'):
    """
    Retrieves and object from the database and places it in the context.

    ``Model`` can be a django Model, Manager or QuerySet.
    
    The object will be retrieved based upon the model key provided in ``model_pk`` and the request 
    variable ``request_key``. The resulting object will be placed in the context variable 
    ``template_object_name``. An object not found based on criteria will result in server 404.
    """
    def _get_object(request, c):
        qs = _get_queryset(Model)
        d = {model_pk: c[request_key]}
        c[template_object_name] = qs.get(**d)
        return request, c
    return _get_object

def get_list(Model, template_qs_name='qs'):
    """
    Retrieves a list for ``Model`` and places it in the context.

    ``Model`` can be a django Model, Manager or QuerySet.

    The object list retrived will be placed in the context variable ``template_qs_name``.
    """
    def _get_list(request, c):
        qs = _get_queryset(Model)
        c[template_qs_name] = qs
        return request, c
    return _get_list

def edit(Form, template_form_name='edit_form', template_obj_name='obj', method='POST'):
    """
    *** not done yet ***
    """
    def _edit(request, c):
        edit_form = Form(request.__getattribute__(method) or None, instance=c[template_obj_name])
        if edit_form.is_valid():
            c[template] = edit_form.save()
            # redirect?
        c[form_name] = edit_form
        return request, c 
    return _edit

def set_context(template_var_name, value):
    """
    Sets the context variable as given in ``template_var_name`` to ``value``. ``value`` can be 
    either a static value or a callable in the form f(request, c).
    """
    def _set_context(request, c):
        if callable(value):
            c[template_var_name] = value(request, c)
        else:
            c[template_var_name] = value
        return request, c
    return _set_context

def template(template_path):
    """
    Sets the context variable 'template_path' to ``template_path``.
    """
    def _template(request, c):
        c['template_path'] = template_path
        return request, c
    return _template

def render(request, c):
    """
    Return an HttpResponse based on the values in ``c``.
    """
    return request, render_to_response(c['template_path'], c)

def chain_view(*partials):
    """
    Enables views to be created in a 'chain' fasion.

    Initial arguments are captured into a dictionary that is in turn pased to each ``partial`` in
    turn and the result from the final ``partial`` is returned. 
    All partials must be in the form of partial(request, c) and return request and c, as to keep 
    the chain going. It is also expected that the final ``partial`` will return a response suitable
    for the client in place of ``c``.
    """
    def _chain_view(request, **kwargs):
        r, c = request, kwargs
        for partial in partials:
            r, c = partial(r, c)
            if isinstance(c, HttpResponse):
                return c
        return c 
    return _chain_view

