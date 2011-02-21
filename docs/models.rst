======
Models
======

The "traditional" model in Django essentially describes a table within an
application's relational database backend. These definitions are stored in an
app's ``models.py`` file. Django model definitions generally look something like
this (taken from Django's own quick example)::

    from django.db import models

    class Person(models.Model):
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)

``first_name`` and ``last_name`` are *fields* of the model. Each field is
specified as a class attribute, and each attribute maps to a database
column. Such attributes can be used to define type (notice that these are
CharFields for storing strings of text), label, help text, maximum
length (30 in this case) and other information about a database column.

Running the ``syncdb`` management command creates an appropriate table in the
database where the fields of the model are used to generate columns in the
table.

Within a Django application an instantiation of a particular model class is
used to represent the data stored in a row in the table that was generated from
that model.

Defining Models with django-fluidinfo
-------------------------------------

Due to the schema-less and *fluid* nature of Fluidinfo things are a bit
different in django-fluidinfo's models. Definitions generally look something
like this::

    from django_fluidinfo import models

    class Person(models.Model):
        first_name = models.CharField('my_app/contacts/first_name')
        last_name = models.CharField('my_app/contacts/last_name')

...and are stored in an app's ``fi_models.py`` file.

Just as with Django, ``first_name`` and ``last_name`` are fields specified as
class attributes. Notice also that each field has a specified type - in this
case they're both CharFields.

This is where the similarity with Django's models ends.

Each model basically represents **potential** tags that may be attached to
objects within Fluidinfo. In fact, the ``Model`` class is itself a rather thin
layer around FOM's ``Object`` class (used to represent / define an Object and
it's tags within Fluidinfo) and the fields inherit from FOM's ``tag_value``
class.

When declaring a field one may *only* specify the full tag path to be used to
link data with an object. Why can't you specify other things such as a label
(used in forms), help text and maximum length..? Well, the label is in fact the
name of the field, in future versions the help text of a field will be the
description of the related tag in Fluidinfo and since Fluidinfo doesn't impose
restrictions such as type or max-length then django-fluidinfo doesn't either.

But what about the field types given in the example above..? Since a Fluidinfo
tag is dynamically typed then django-fluidinfo doesn't impose a value type *but*
by using a typed field (as above) any ModelForms that make use of this model
will use this information to display the fields with the correct widget and
impose appropriate validation.

Here are the list of available field types (this will change / grow):

* **TagField** - a catch all, defaults to a text input element
* **CharField** - for textual data, defaults to a text input element
* **IntegerField** - for whole numbers, defaults to a text element with appropriate validation
* **FloatField** - for floating point numbers, defaults to a text element with appropriate validation
* **BooleanField** - for True/False values, defaults to a CheckBox input element

Once the django_fluidinfo models have been defined in fi_models.py you should
run ``python manage.py syncfluidinfo`` to check that the required tags and
namespaces either exist or are created for you.

Querying Fluidinfo
------------------

Once you've created your models you can use them to create, retrieve, update
and delete information.

It is important to remember that **all** objects in Fluidinfo are public and
writeable. It is the tags, namespaces and tag-values that have permissions
associated with them. Permissions can be set using FOM and a section on this
will be added soon.

To create an object onto which you want to add tags (fields) defined in a
model you simply do something like this::

    p = Person(about='An object representing the person Fred Blogs')
    p.create()

Notice that you can *optionally* set an ``about`` tag. This is just a convention
to help indicate what the object might be about. It is a unique and public
tag controlled by Fluidinfo itself (so you can't change the visibility or
permissions on it).

To create or update information / data tagged to an object simply do::

    p.first_name = 'Fred'
    p.last_name = 'Blogs'
    p.save()

It is important to realise that a call is made to Fluidinfo *only at the
point* when ``save()`` is called. Such a call is blocking too.

There are several ways to query and extract objects / information from Fluidinfo.

Instantiate a model and pass in the object's uuid::

    uid = u'f6d78cab-21dd-4cc6-98aa-6dd076d1f0e8' # example object uid
    p = Person(uid)

Instantiate a model and pass in the object's ``about`` tag value::

    about_value = 'An object representing the person Fred Blogs'
    p = Person(about=about_value)

Query Fluidinfo to return objects that match search criteria::

    results = Person.filter('my_app/contacts/first_name = "Fred" and my_app/contacts/last_name = "Blogs"')

In the case of the third method you pass in a query that uses Fluidinfo's
uber-minimalist query language (see below).

The result will be a list of instantiations of the model that match the query.

It is important to note, depending on what you query, you might get objects
that do **not** have the tags defined in the model class. Should you attempt
to get the value of such non-existent tags an exception will be thrown::

    >>> p = Person(about="foo")
    >>> p.first_name
    Traceback (most recent call last):
    ... 
    fom.errors.Fluid404Error: <TNoInstanceOnObject (404 Not Found)>

To discover what tags *are* associated with an object you can use the ``tags`` and
``tag_paths`` attributes to get a list of FOM Tag instances or tag paths respectively::

    >>> p.tags
    [<fom.mapping.Tag object at 0xb7562fcc>, <fom.mapping.Tag object at 0xb754f7cc>, <fom.mapping.Tag object at 0xb754f44c>]
    >>> p.tag_paths
    [u'myapp/contacts/first_name', u'fluiddb/about', u'myapp/contacts/last_name']

You can get at the values of these tags by calling the ``get`` method on the
object::

    >>> p.get('myapp/contacts/first_name')
    (u'Fred', 'application/vnd.fluiddb.value+json')

(These tags do **not** have to be defined as fields in the model class)

Fluidinfo's Query Language
--------------------------

Fluidinfo provides a simple query language that allows applications to search
for objects based on their tags' values. The following kinds of queries are
possible:

* **Numeric:** To find objects based on the numeric value of tags. For example, ``tim/rating > 5``.
* **Textual:** To find objects based on text matching of their tag values, e.g., ``sally/opinion matches fantastic``. Text matching is done with `Lucene <http://lucene.apache.org/java/docs/>`_, meaning that Lucene matching capabilities and style will be available [#matching]_.
* **Presence:** Use ``has`` to request objects that have a given tag. For example, ``has sally/opinion``.
* **Set contents:** A tag on an object can hold a set of strings. For example, a tag called ``mary/product-reviews/keywords`` might be on an object with a value of ``[ "cool", "kids", "adventure" ]``. The ``contains`` operator can be used to select objects with a matching value. The query ``mary/product-reviews/keywords contains "kids"`` would match the object in this example.
* **Exclusion:** You can exclude objects with the ``except`` keyword. For example ``has nytimes.com/appeared except has james/seen``. The ``except`` operator performs a set difference.
* **Logic:** Query components can be combined with ``and`` and ``or``. For example, ``has sara/rating and tim/rating > 5``.
* **Grouping:** Parentheses can be used to group query components. For example, ``has sara/rating and (tim/rating > 5 or mike/rating > 7)``.

That's it!

Query result limits
-------------------

The main current limit is that queries may only return up to 1 million
objects.  If a query generates more than this, an error status is returned.
If you need a higher limit, please `email us <info@fluidinfo.com>`_.

Notes
-----

.. [#matching] Text matching has not been implemented for the launch of the Fluidinfo private alpha. About tag values *are* indexed and full text indexing will be switched on soon.
