import unittest
import models
import forms
from django import forms as django_forms

from fom.dev import sandbox_fluid
from fom.mapping import Namespace
fluid = sandbox_fluid()
fluid.login('test', 'test')


def createTag(parent, name, description, indexed=False):
    """
    Creates a new tag under the given namespace
    """
    try:
        tag = parent.create_tag(name, description, indexed)
    except Fluid412Error:
        # 412 simply means the tag already exists
        pass
    return tag

# make sure the correct tags exist in the sandbox
test_ns = Namespace('test')
createTag(test_ns, 'description', 'A tag created for the purposes of testing.')
createTag(test_ns, 'timestamp', 'A tag created for the purposes of testing.')


class Meeting(models.Model):
    """
    A test 'model' definition
    """
    description = models.CharField('test/description')
    timestamp = models.IntegerField('test/timestamp')


class MeetingForm(forms.ModelForm):
    """
    A test ModelForm definition
    """
    class Meta:
        model = Meeting


class BespokeMeetingForm(forms.ModelForm):
    """
    A test ModelForm with some weird modifications
    """
    def __init__(self, *args, **kwargs):
        super(BespokeMeetingForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = django_forms.SelectMultiple()
        self.fields['description'].choices = [('foo', 'FOO'), ('bar', 'BAR'),
            ('baz', 'BAZ')]

    class Meta:
        model = Meeting

    def clean_description(self):
        """
        A silly validation for a specific field
        """
        data = self.cleaned_data['description']
        if 'foo' not in data:
            raise django_forms.ValidationError("foo!")
        return data

    def clean(self):
        """
        A silly validation for the whole form
        """
        cleaned_data = self.cleaned_data
        description = cleaned_data.get('description')
        timestamp = cleaned_data.get('timestamp')
        if ('foo' != description) and timestamp < 1000:
            raise django_forms.ValidationError("form foo!")
        return cleaned_data


class ModelTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_object_with_model(self):
        """
        Make sure we can create a new Fluidinfo object based upon the
        template provided by the model class
        """
        m = Meeting(about="django_fluidinfo test object")
        m.description = "this is the django_fluidinfo test object"
        m.timestamp = 123456
        m.save()
        # check we have an appropriate fields dictionary and ordered_fields list
        self.assertEqual(2, len(m.fields))
        self.assertEqual(['description', 'timestamp'], m.ordered_fields)
        # lets check we can extract the new values from Fluidinfo
        twin = Meeting(m.uid)
        self.assertEqual(m.description, twin.description)
        self.assertEqual(m.timestamp, twin.timestamp)

    def test_field_types(self):
        """
        Just like Django we provide fields types (but these map to Fluidinfo's
        primitive types).

        Although we don't enforce the "type" that can be set against these
        fields (I feel this runs against the grain of Fluidinfo's dynamic
        nature)
        it is used by the forms classes to work out how to display the field
        (i.e. which of Django's widget to use)
        """
        default = models.TagField('dummy/path')
        self.assertEqual(unicode, default.field_type)
        c = models.CharField('dummy/path')
        self.assertEqual(unicode, c.field_type)
        i = models.IntegerField('dummy/path')
        self.assertEqual(int, i.field_type)
        f = models.FloatField('dummy/path')
        self.assertEqual(float, f.field_type)
        b = models.BooleanField('dummy/path')
        self.assertEqual(bool, b.field_type)

    def test_form_has_fields(self):
        """
        Make sure we can instantiate a form from a model instance
        """
        m = Meeting(about="django_fluidinfo test object")
        m.description = "this is the django_fluidinfo test object"
        m.timestamp = 123456
        m.save()
        f = MeetingForm(instance=m)
        # test the fields made it from the model to the form correctly
        self.assertEqual(True, f.fields.has_key('description'))
        self.assertEqual(True, f.fields.has_key('timestamp'))

    def test_form_saves_tags(self):
        """
        Make sure that all the tag/values are updated when the form's save
        method is called
        """
        m = Meeting(about="django_fluidinfo test object")
        m.description = "this is the django_fluidinfo test object"
        m.timestamp = 123456
        m.save()
        data = {'description': 'new description', 'timestamp': 654321 }
        f = MeetingForm(data, instance=m)
        self.assertEqual(True, f.is_valid())
        f.save()
        self.assertEqual('new description', m.description)
        self.assertEqual(654321, m.timestamp)

    def test_form_bespoke_validation(self):
        """
        Make sure django-fluidinfo plays nicely with Django's own validation
        framework in the forms
        """
        m = Meeting(about="django_fluidinfo test object")
        m.description = "this is the django_fluidinfo test object"
        m.timestamp = 123456
        m.save()
        data = {'description': 'foo', 'timestamp': 1000}
        f = BespokeMeetingForm(data)
        self.assertEqual(True, isinstance(f.fields['description'].widget,
            django_forms.widgets.SelectMultiple))
        self.assertEqual([('foo', 'FOO'), ('bar', 'BAR'), ('baz', 'BAZ')],
            f.fields['description'].choices)
        self.assertEqual(True, f.is_valid())
        data['description'] = 'bar'
        f = BespokeMeetingForm(data)
        self.assertEqual(False, f.is_valid())
        self.assertEqual(True, f.errors['description'] == [u'foo!'])
        data['timestamp'] = 999
        f = BespokeMeetingForm(data)
        self.assertEqual(False, f.is_valid())
        self.assertEqual(True, f.errors['__all__'] == [u'form foo!'])

if __name__ == '__main__':
    unittest.main()
