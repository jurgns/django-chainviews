from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, _get_queryset

####################################################################################################
##### Conditions ###################################################################################

def get_session_key(key):
    """
    """
    def _get_session_key(request, c):
        if key not in request.session:
            return
        return request.session[key]
    return _get_session_key

def get_request_key(key, method='GET'):
    """
    """
    def _get_request_key(request, c):
        return request.__getattribute__(method).get(key, None)
    return _get_request_key

def get_context_key(key):
    """
    """
    def _get_context_key(request, c):
        if key not in c:
            return
        return c[key]
    return _get_context_key

def or_(*conditions):
    """
    """
    def _or_(request, c):
        for condition in conditions:
            value = (callable(condition) and condition(request, c)) or condition
            if value:
                return value
    return _or_

def and_(*conditions):
    """
    """
    def _and_(request, c):
        for condition in conditions:
            value = (callable(condition) and condition(request, c)) or condition
            if not value:
                return value
    return _and_

def not_(condition):
    """
    """
    def _not_(request, c):
        return not ((callable(condition) and condition(request, c)) or condition)
    return _not_

####################################################################################################
##### Partials #####################################################################################

def set_session_key(key, value):
    def _set_session_key(request, c):
        request.session[key] = value
        return request, c
    return _set_session_key

def do_nothing(request, c):
    """
    """
    return request, c

def if_(condition, then_partial=do_nothing, else_partial=do_nothing):
    """
    Executes ``then_partial`` on based on ``condition``. Optional ``else_partial`` will be evaluated
    on ``condition`` failure.

    ``condition`` is a condition in the form f(request, c) -> bool.
    ``then_partial`` and ``else_partial`` should both be partials of the form f(request, c) -> (request, c).
    """
    def _if_(request, c):
        if condition(request, c):
            return then_partial(request, c)
        return else_partial(request, c)
    return _if_

def get_object(Model, query_keys={}, template_object_name='obj'):
    """
    Retrieves and object from the database and places it in the context.

    ``Model`` can be a django Model, Manager or QuerySet.
    
    The object will be retrieved based upon the key-value pairs provided in ``query_keys``. The 
    resulting object will be placed in the context variable ``template_object_name``. An object 
    not found based on criteria will result in server 404.
    """
    # grab the metaclass
    if hasattr(Model, '_meta'):
        meta = Model._meta
    elif hasattr(Model, 'model'):
        meta = Model.model._meta
    else:
        raise Exception
    if not query_keys:
        query_keys = {'pk': "%s_id" % meta.object_name.lower()}
    def _get_object(request, c):
        # function to fetch request key from context
        _fetch = lambda kvpair: (kvpair[0], c[kvpair[1]])
        # qs via django private method
        qs = _get_queryset(Model)
        # map _fetch onto query_keys and return to dictionary
        d = dict(map(_fetch, query_keys.items()))
        # get or 404
        c[template_object_name] = get_object_or_404(qs, **d)
        return request, c
    return _get_object

def get_qs(Model, query_keys={}, template_qs_name='qs'):
    """
    Retrieves a list for ``Model`` and places it in the context.

    ``Model`` can be a django Model, Manager or QuerySet.

    The object list retrived will be placed in the context variable ``template_qs_name``.
    """
    def _get_qs(request, c):
        qs = _get_queryset(Model)
        if query_keys:
            # function to fetch request key from context
            _fetch = lambda kvpair: (kvpair[0], c[kvpair[1]])
            # map _fetch onto query_keys and return to dictionary
            keys = map(_fetch, query_keys.items())
            keys = dict(keys)
            # filter
            c[template_qs_name] = qs.filter(**keys)
        else:
            c[template_qs_name] = qs
        return request, c
    return _get_qs

def filter_qs(query_keys, template_qs_name='qs'):
    """
    """
    def _filter_qs(request, c):
        # function to fetch request key from context
        _fetch = lambda kvpair: (kvpair[0], c[kvpair[1]])
        # map _fetch onto query_keys and return to dictionary
        keys = map(_fetch, query_keys.items())
        keys = dict(keys)
        # filter
        c[template_qs_name] = c[template_qs_name].filter(**keys)
        return request, c
    return _filter_qs 

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

def chain_partial(*partials):
    """
    Simple container for partials, usefull when combinding several partials into a single contained
    unit (partial).
    """
    # fail fast if any partial generators do not return a function
    assert None not in partials
    def _chain_partial(request, c):
        for partial in partials:
            request, c = partial(request, c)
        return request, c
    return _chain_partial

def chain_view(*partials):
    """
    Enables views to be created in a 'chain' fasion.

    Initial arguments are captured into a dictionary that is in turn pased to each ``partial`` in
    turn and the result from the final ``partial`` is returned. 
    All partials must be in the form of partial(request, c) and return request and c, as to keep 
    the chain going. It is also expected that the final ``partial`` will return a response suitable
    for the client in place of ``c``.
    """
    # fail fast if any partial generators do not return a function
    assert None not in partials
    def _chain_view(request, **kwargs):
        r, c = request, kwargs
        for partial in partials:
            r, c = partial(r, c)
            if isinstance(c, HttpResponse):
                return c
        return c 
    return _chain_view

