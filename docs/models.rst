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

Models in django-fluiddb
------------------------

Due to the schema-less and *fluid* nature of FluidDB things are a bit different
in django-fluiddb's models. Definitions generally look something like this::

    from django_fluiddb import models

    class Person(models.Model):
        first_name = models.CharField('my_app/contacts/first_name')
        last_name = models.CharField('my_app/contacts/last_name')

...and are stored in an app's ``fdb_models.py`` file. 

Just as with Django, ``first_name`` and ``last_name`` are fields specified as
class attributes. Notice also that each field has a specified type - in this
case they're both CharFields. 

This is where the similarity with Django's models ends. 

Each model basically represents **potential** tags that may be attached to 
objects within FluidDB. In fact, the ``Model`` class is itself a rather thin
layer around FOM's ``Object`` class (used to represent / define an Object and
it's tags within FluidDB) and the fields inherit from FOM's ``tag_value`` class.

When declaring a field one may *only* specify the full tag path to be used to 
link data with an object. Why can't you specify other things such as a label
(used in forms), help text and maximum length..? Well, the label is in fact the
name of the field, in future versions the help text of a field will be the
description of the related tag in FluidDB and since FluidDB doesn't impose
restrictions such as type or max-length then django-fluiddb doesn't either.

But what about the field types given in the example above..? Since a FluidDB 
tag is dynamically typed then django-fluiddb doesn't impose a value type *but*
by using a typed field (as above) any ModelForms that make use of this model
will use this information to display the fields with the correct widget and 
impose appropriate validation.

Here are the list of available field types (this will change / grow):

* **TagField** - a catch all, defaults to a text input element
* **CharDield** - for textual data, defaults to a text input element 
* **IntegerField** - for whole numbers, defaults to a text element with appropriate validation
* **FloatField** - for floating point numbers, defaults to a text element with appropriate validation
* **BooleanField** - for True/False values, defaults to a CheckBox input element

Once the django_fluiddb models have been defined in fdb_models.py you should
run ``python manage.py syncfluiddb`` to check that the required tags and 
namespaces either exist or are created for you.
