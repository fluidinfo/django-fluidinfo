"""
Wraps and inherits from Ali Afshar's FOM classes so they appear more
Django-esque.

Djangonaughts are used to defining models like this:

from django.db import models

class foo(models.Model):
    bar = models.CharField(_('A Bar'), help_text=_('Some help text'))
    baz = models.IntField(_('Some Baz'), help_text=_('Enter a number'))

I'm aiming for something familiar like this:

from django_fluidinfo import models

class foo(models.Model):
    bar = models.TagField('test/namespace/bar_tag')
    baz = models.TagField('test/namespace/baz_tag')

The "name" of the field on the forms will be the name of the attribute, the
help_text will be the referenced tag's "description" from within Fluidinfo (to
be implemented).

These "models" can then be used with the ModelForms defined in forms.py so
they work like the classic Django models.ModelForm:

from django_fluidinfo.forms import ModelForm

class FooForm(ModelForm):
    class Meta:
        model = Foo

Yeah, I know this doesn't reflect the dynamic nature of Fluidinfo's schema *but*
my aim is to give Djangonaughts a familiar "no brainer" route to using
Fluidinfo.

I expect them to dig into FOM once they grok what Fluidinfo is about. ;-)
"""


try:
    from fom.mapping import Object, tag_value
except ImportError:
    raise ImportError("FOM must be in your Python path. See http://launchpad.net/fom for more information")


class ModelBase(type):
    """
    Metaclass for the Model object.
    """

    def __new__(cls, name, bases, attrs):
        super_new = super(ModelBase, cls).__new__
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            # if this isn't a subclass of Model then don't do anything special
            return super_new(cls, name, bases, attrs)

        # We want to be able to store away the field names and tags so the form
        # class can make use of them later
        fields = {}
        ordered_fields = []
        for field, tag in attrs.items():
            if isinstance(tag, tag_value):
                fields[field] = tag
                ordered_fields.append(field)
        ordered_fields.reverse()

        # dictionary of tag names : tag values
        attrs['fields'] = fields
        # ordered list of the fields - in order they're declared in code
        attrs['ordered_fields'] = ordered_fields

        # Create the new class
        new_class = super_new(cls, name, bases, attrs)
        return new_class


class Model(Object):
    """
    Represents a data "model" that can be applied to objects within Fluidinfo
    (i.e. it specifies a collection of tags that *might* appear on an object)
    """
    __metaclass__ = ModelBase


# TagFields defined below just make it "nice" for djangonaughts to grok how
# a tag attribute *should* behave in terms of type. It isn't enforced but it
# means that the forms classes can work out how to display the related fields.


class TagField(tag_value):
    """
    Represents a generic tag with no specifically pre-defined type
    """
    @property
    def field_type(self):
        # Default
        return unicode


class CharField(tag_value):
    """
    A tag that should contain a Fluidinfo "string" primitive type
    """
    @property
    def field_type(self):
        return unicode


class IntegerField(tag_value):
    """
    A tag that should contain a Fluidinfo integer primitive type
    """
    @property
    def field_type(self):
        return int


class FloatField(tag_value):
    """
    A tag that should contain a Fluidinfo float primitive type
    """
    @property
    def field_type(self):
        return float


class BooleanField(tag_value):
    """
    A tag that should contain a Fluidinfo boolean primitive type
    """
    @property
    def field_type(self):
        return bool
