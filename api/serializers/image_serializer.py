from rest_framework import serializers
from api.models import UploadImage
from api.utils.helpers import Base64ImageField


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    source_path = serializers.URLField(allow_null=True, allow_blank=True)
    original_file = Base64ImageField(required=True)
    transformed_file = Base64ImageField(allow_null=True)
    class Meta:
        model = UploadImage
        fields = ('id', 'source_path', 'original_file', \
          'transformed_file', 'last_modified')