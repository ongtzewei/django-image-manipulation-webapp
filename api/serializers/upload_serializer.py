from rest_framework import serializers
from api.models import UploadImage, UploadRequest
from api.serializers import ImageSerializer


class UploadSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    images_id = serializers.PrimaryKeyRelatedField(write_only=True, many=True, \
      queryset=UploadImage.objects.all())    

    class Meta:
        model = UploadRequest
        fields = ('id', 'images', 'images_id', 'last_modified')

    def create(self, validated_data):
        images_id = validated_data.pop('images_id', None)
        transformation_request = super(UploadSerializer, self).create(validated_data)
        transformation_request.images.add(*images_id)
        return transformation_request
        