django-fluidinfo
================

(c) FluidInfo 2011
dev@fluidinfo.com

License: New BSD License

Bridging Django to Fluidinfo with FOM
-------------------------------------

The purpose of this package is to make it easy to use
`FOM <http://launchpad.net/fom>`_ to define models for
Django based applications that need to make use of
`Fluidinfo <http://fluidinfo.com>`_ as their database backend (instead of a
traditional relational database).

To read the full documentation make sure you have
`Sphinx <http://sphinx.pocoo.org/>`_ installed, change to the doc directory and
type::

        make html

Alternatively, you can view the documentation online here:

`http://packages.python.org/django-fluidinfo/ <http://packages.python.org/django-fluidinfo/>`_

How..?
-------

It works by wrapping the FOM based classes in Django-esque classes so you can
do the following::

        from django_fluidinfo import models
        
        class foo(models.Model):
            bar = models.CharField('test/namespace/bar_tag')
            baz = models.IntegerField('test/namespace/baz_tag')

These models can then be used with specially created ModelForms that
function in a similar fashion to the traditional Django ModelForms::

        from django_fluidinfo.forms import ModelForm

        class FooForm(ModelForm):
            class Meta:
                    model = Foo

Take a look in the django_fluidinfo/tests.py file for example usage. Expect
more comprehensive documentation very soon.

While this doesn't reflect the dynamic nature of Fluidinfo's schema I'd like to
point out that my aim is to give Djangonaughts a familiar "no brainer" route
to using Fluidinfo.

I expect them to dig into FOM once they grok what Fluidinfo is about. ;-)

Comments and feedback most welcome!
