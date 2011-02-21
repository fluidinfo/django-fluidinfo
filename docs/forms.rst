=====
Forms
=====

As with the models and related classes django-fluidinfo attempts to keep things
familiar regarding forms from the Django developer's point of view.

Django provides a powerful mechanism to allow developers to map models to forms
for adding and/or editing data. As they point out in their documentation, "you
might have a ``BlogComment`` model and you want to create a form that lets
people submit comments. In this case, it would be redundant to define the field
types in your form, because you've already defined the fields in your model".

To base a form upon a model developers define a class in the ``forms.py`` module
that inherits from ModelForm::

    from django.forms import ModelForm

    class BlogCommentForm(ModelForm):
        class Meta:
            model = BlogComment

The new ``BlogCommentForm`` would then contain fields based upon those defined
in the ``BlogComment`` model class - including appropriate validation.

Forms in djang-fluidinfo
------------------------

This same functionality has been built into django-fluidinfo. Developers should
add something like the following to their ``forms.py`` module::

    from django_fluidinfo.forms import ModelForm
    from fi_models.py import Person # taken from the previous models example

    class PersonForm(ModelForm):
        class Meta:
            model = Person

Notice that the form's class inherits from ``django_fluidinfo.forms.ModelForm``.

Since django-fluidinfo's ModelForm inherits from Django's own BaseForm it is
possible to bespoke the form in the usual ways::

    from django import forms as django_forms
    from django_fluidinfo.forms import ModelForm
    from fi_models.py import Person

    class BespokePersonForm(ModelForm):
        """
        A ModelForm with some weird modifications
        """
        def __init__(self, *args, **kwargs):
            super(BespokePersonForm, self).__init__(*args, **kwargs)
            self.fields['last_name'].widget = django_forms.SelectMultiple()
            self.fields['last_name'].choices = [('smith', 'Smith'), ('jones', 'Jones'), ('brown', 'Brown')]
            self.fields['first_name'].required = False

        class Meta:
            model = Person

        def clean_last_name(self):
            """
            A silly validation for a specific field
            """
            data = self.cleaned_data['last_name']
            if 'smith' not in data:
                raise django_forms.ValidationError("Only Smith is allowed!")
            return data

        def clean(self):
            """
            A silly validation for the whole form
            """
            cleaned_data = self.cleaned_data
            first_name = cleaned_data.get('first_name').lower()
            last_name = cleaned_data.get('last_name')
            if first_name == 'john' and last_name == 'smith':
                raise django_forms.ValidationError("Your name is too common")
            return cleaned_data

To use the form in an app's ``views.py`` developers should do something
like this::

    p = Person()
    p.create()
    f = PersonForm(request.POST, instance=p)
    if f.is_valid():
        f.save()

Notice how this basically matches what one should do with Django's own
ModelForm class: an instance of the model is created, it is passed into the
form's __init__ function along with POST data, validated and then saved to
Fluidinfo. Simple!
