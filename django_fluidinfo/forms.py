"""
Helper functions and classes required for creating ModelForm classes from FOM
Objects and tag_values (aliased as Models and *Fields)

I've attempted to keep things as similar to what is found in django.forms.

To use the forms you should first define a model that inherits from
django_fluidinfo.models.Model. Then, in forms.py:

from django_fluidinfo.forms import ModelForm

class MyFluidinfoModelForm(ModelForm):
    class Meta:
        model = MyFluidinfoModelClass

In fact, since the django_fluidinfo.forms.ModelForm class inherits from Django's
BaseForm class you can bespoke it like the regular ModelForm class.
"""
from django import forms
from django.utils.datastructures import SortedDict
from django.forms.forms import BaseForm, get_declared_fields
from django.forms.util import ErrorList
from fom.errors import Fluid404Error


# This dictionary defines how each type should be displayed in a form
FORM_TYPES = {
    bool: forms.BooleanField,
    int: forms.IntegerField,
    float: forms.FloatField,
    str: forms.CharField,
    unicode: forms.CharField
}


def save_instance(form, instance, fields=None, fail_message='saved',
                  commit=True, exclude=None):
    """
    Iterates through the fields and saves them as tag-values against the
    instance object representing an object in Fluidinfo and then pushes the
    changes to Fluidinfo.
    """
    if form.errors:
        raise ValueError("The %s could not be %s because the data didn't"\
            " validate." % ('object', fail_message))

    cleaned_data = form.cleaned_data

    for field_name in instance.ordered_fields:
        if fields and field_name not in fields:
            continue
        if exclude and field_name not in exclude:
            continue
        setattr(instance, field_name, cleaned_data[field_name])
    instance.save()
    return instance


def model_to_dict(instance, fields=None, exclude=None):
    """
    Returns a dict containing the data in "instance" suitable for passing as
    a Form's "initial" keyword argument.

    "fields" is an optional list of field names. If provided, only the named
    fields will be included in the returned dict

    "exclude" is an optional list of field names. If provided, the name fields
    will be excluded from the returned dict, even if they are listed in the
    "fields" argument.
    """
    data = {}
    for f in instance.ordered_fields:
        if fields and not f in fields:
            continue
        if exclude and f in exclude:
            continue
        else:
            field = instance.fields[f]
            try:
                raw_data = instance.get(instance.fields[f].tagpath)
                if raw_data:
                    clean_data = raw_data[0]
            except Fluid404Error:
                clean_data = ''
            data[f] = instance.get(instance.fields[f].tagpath)[0]
    return data


def formfield_for_model_field(instance, field_name,
        form_class=forms.FileField, **kwargs):
    """
    Returns the appropriate form field type for a named field in an instance
    """
    field_type = instance.fields[field_name].field_type
    # Use FileField to represent the (default) opaque value on a form
    FormField = form_class
    if FORM_TYPES.has_key(field_type):
        FormField = FORM_TYPES[field_type]
    formfield = FormField()
    return formfield


def fields_for_model(instance, fields=None, exclude=None,
    formfield_callback=None):
    """
    Returns a "SortedDict" containing form fields for the given fom_object.

    ``fields`` is an optional list of field names. If provided, only the named
    fields will be included in the returned fields.

    ``exclude`` is an optional list of field names. If provided, the named
    fields will be excluded from the returned fields, even if they are listed
    in the ``fields`` argument.
    """
    field_list = []
    ignored = []
    for f in instance.ordered_fields:
        if fields and not f in fields:
            continue
        if exclude and not f in exclude:
            continue

        formfield = formfield_for_model_field(instance, f)
        if formfield:
            field_list.append((f, formfield))

    field_dict = SortedDict(field_list)
    if fields:
        field_dict = SortedDict(
            [(f, field_dict.get(f)) for f in fields
            if ((not exclude) or (exclude and f not in exclude))]
            )
    return field_dict


class ModelFormOptions(object):
    """
    Basis for the _meta attribute
    """
    def __init__(self, options=None):
        self.model = getattr(options, 'model', None)
        self.fields = getattr(options, 'fields', None)
        self.exclude = getattr(options, 'exclude', None)


class ModelFormMetaclass(type):
    """
    Used to build a Form from a fom Object
    """
    def __new__(cls, name, bases, attrs):
        formfield_callback = attrs.pop('formfield_callback', None)
        try:
            parents = [b for b in bases if issubclass(b, ModelForm)]
        except NameError:
            # defining ModelForm itself
            parents = None
        declared_fields = get_declared_fields(bases, attrs, False)
        new_class = super(ModelFormMetaclass, cls).__new__(cls, name, bases,
            attrs)
        if not parents:
            return new_class
        opts = new_class._meta = ModelFormOptions(getattr(new_class, 'Meta',
            None))
        if opts.model:
            # if model is defined then extract the fields from the associated
            # FOM Object
            fields = fields_for_model(opts.model, opts.fields, opts.exclude,
                formfield_callback)
            # override default FOM Object's fields with any custom declared ones
            fields.update(declared_fields)
        new_class.declared_fields = declared_fields
        new_class.base_fields = fields
        return new_class


class BaseModelForm(BaseForm):
    """
    All django-fluidinfo model forms inherit capabilities from this class
    """
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=True, instance=None):
        opts = self._meta
        if instance is None:
            # best create one then...
            self.instance = opts.model() # it's anonymous for now
            object_data = {}
        else:
            self.instance = instance
            object_data = model_to_dict(instance, opts.fields, opts.exclude)
        # if initial is provided then override values from the instance
        if initial is not None:
            object_data.update(initial)
        super(BaseModelForm, self).__init__(data, files, auto_id, prefix,
            object_data, error_class, label_suffix, empty_permitted)

    def save(self, commit=True):
        return save_instance(self, self.instance, self._meta.fields, 'saved',
                             commit, exclude=self._meta.exclude)


class ModelForm(BaseModelForm):
    """
    All model forms must inherit from this class
    """
    __metaclass__ = ModelFormMetaclass
