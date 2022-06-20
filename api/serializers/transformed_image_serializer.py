from django.forms import ChoiceField
from rest_framework import serializers
from api.models import TransformedImage
from api.serializers.helpers import SourceImageField, TransformedImageField

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class TransformedImageSerializer(serializers.HyperlinkedModelSerializer):
    #source = ChoiceField(choices=TransformedImage.ImageSource.choices)
    source_path = serializers.URLField(allow_null=True, allow_blank=True)
    original_file = SourceImageField(required=True)
    transformed_file = TransformedImageField(required=True)
    class Meta:
        model = TransformedImage
        fields = ('id', 'source', 'source_path', 'original_file', 'transformed_file', 'last_modified')
