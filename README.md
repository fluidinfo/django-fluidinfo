django-fluiddb
==============

(c) FluidInfo 2010
dev@fluidinfo.com

License: New BSD License

Bridging Django to FluidDB with FOM
-----------------------------------

The purpose of this package is to make it easy to use 
[FOM](http://bitbucket.org/aafshar/fom-main/wiki/Home) to define models for
Django based applications that need to make use of 
[FluidDB](http://fluidinfo.com) as their database backend (instead of a
traditional relational database). 

It works by wrapping the FOM based classes in Django-esque classes so you can
do the following:

        from django_fluiddb import models 
        
        class foo(models.Model):
            bar = models.CharField('test/namespace/bar_tag')
            baz = models.IntegerField('test/namespace/baz_tag') 

These models can then be used with specially created ModelForms that
function in a similar fashion to the traditional Django ModelForms:

        from django_fluiddb.forms import ModelForm

        class FooForm(ModelForm):
            class Meta:
                    model = Foo

Take a look in the django_fluiddb/tests.py file for example usage. Expect more 
comprehensive documentation very soon.

While this doesn't reflect the dynamic nature of FluidDB's schema I'd like to
point out that my aim is to give Djangonaughts a familiar "no brainer" route 
to using FluidDB.

I expect them to dig into FOM once they grok what FluidDB is about. ;-)

Comments and feedback most welcome!

(An introductory presentation can be 
[found here](http://www.slideshare.net/ntoll/an-introduction-to-fluiddb-a-social-database-in-the-cloud))
