from django.forms.fields import Field

class TagField(Field):
    """
    A basic "hold-all" field that represents a tag/value combination to attach to an object
    """
    def __init__(self, tag_path, *args, **kwargs):
        self.tag_path = tag_path
        super(TagField, self).__init__(*args, **kwargs)
