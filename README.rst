=================
Django ChainViews
=================

The Django ChainViews is an concept project for creating extremely flexible, semi-generic views. 
Typical views are often repetitive and boring and many turn toward generics. The problem is that when the generic is not quite what you need, users are often left to forgo the built-ins and create their own. This is repetitive and thus why chain views were born.
The concept is simple: piece together smaller 'view partials' to create a complete view. Partials can be created to do a plethora of things, including but not limited to fetching database items, setting context variables and ultimately rendering to a response. If one portion of a view chain does not work to your exact specifications, write a new one and insert it in it's place. This way only a few lines need be replaced, not the entire view. 

=======
Example
=======

Let us assume you have the following Model:

class Foo(models.Model):
    name = models.CharField(max_length=64)
    creator = models.ForeignKey(User)
    description = models.TextField()

To create a chainview for a listing of this model:

from chainviews.views import chain_view, get_list, template, render

foo_list = chain_view(
    get_list(Foo),
    template('foo_list.html'),
    render,
)

To create a detail view:

from chainviews.views import chain_view, get_object, template, render

foo_detail = chain_view(
    get_object(Foo),
    template('foo_detail.html'),
    render,
)

Now these views alone are rather bland and do not show off the flexibility of the chainview, but let us now assume that the creator of a foo object has special privileges. We can easily modify the above to reflect this

from chainviews.views import chain_view, get_object, if_, template, render

def creator(request, c):
    return c['obj'].creator == request.user

def special_foo(request, c):
    # do special stuff here
    return request, c

foo_detail = chain_view(
    get_object(Foo),
    if_(creator, special_foo),
    template('foo_detail.html'),
    render,
)

This is still only a very simple example. Other potential uses may include:
-Using a different templating engine or orm
-Generic, object level permission handling

