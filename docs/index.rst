.. django-fluiddb documentation master file, created by
   sphinx-quickstart on Mon May  3 17:08:25 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introducing django-fluiddb
==========================

The purpose of this package is to make it easy to use 
`FOM <http://bitbucket.org/aafshar/fom-main/wiki/Home>`_ the *Fluid Object
Mapper* to define models for `Django <http://djangoproject.com>`_ based 
applications that need to make use of `FluidDB <http://fluidinfo.com>`_ as 
their database backend (instead of a traditional relational database).

Contents
--------

.. toctree::
   :maxdepth: 1

   configuration
   models
   forms
   syncfluiddb

Summary
-------

Django-fluiddb works by wrapping the FOM based classes in Django-esque classes so you can
do the following::

    from django_fluiddb import models

    class foo(models.Model):
        bar = models.CharField('test/namespace/bar_tag')
        baz = models.IntegerField('test/namespace/baz_tag')

These models can then be used with specially created ModelForms that
function in a similar fashion to the traditional Django ModelForms::

    from django_fluiddb.forms import ModelForm

    class FooForm(ModelForm):
        class Meta:
            model = Foo

ToDo
----

This work is unfinished. Here's what needs doing:

* Create the syncfluiddb management command
* Document the syncfluiddb management command
* Create patch to add query like capabilities to FOM models
* Document query language and query mechanism

What is FluidDB..?
------------------

FluidDB is a radical approach to creating, storing, sharing and finding 
information. There is only **one** instance of FluidDB that all users and 
applications share, so everyone's data is stored in the same place. However,
there is a unique yet powerful permissions system so everyone still has
control over the information they put into FluidDB. The important thing to
remember is that FluidDB makes it easy to *mash up*, share, annotate and 
create information in a sort of social-graph of data.

The important key concepts are:

* **Objects** - represent things [#]_
* **Tag** - define objects' attributes
* **Namespaces** - organise tags
* **Permissions** - control access

How does it work..?
-------------------

Access to FluidDB is provided by a `RESTful API <http://api.fluidinfo.com/fluidDB/api/*/*/*>`_
which `FOM <http://bitbucket.org/aafshar/fom-main/wiki/Home>`_ abstracts away 
into a Pythonic object-oriented API.

The intention of django-fluiddb is to add a thin layer and useful classes on 
top of FOM in order to make it as simple as possible to use FluidDB from 
within Django.

More information about FluidDB can be found at `Fluidinfo's 
website <http://fluidinfo.com>`_.

.. rubric:: Footnotes

.. [#] **NOT** instantiations of classes as in Object Oriented Programming, but simply "objects" in the common-sense use of the term.
