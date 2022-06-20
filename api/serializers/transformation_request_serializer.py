from attr import validate
from rest_framework import serializers
from api.models import TransformedImage, TransformationRequest
from api.serializers import TransformedImageSerializer

class TransformationRequestSerializer(serializers.ModelSerializer):
    images = TransformedImageSerializer(read_only=True, many=True)
    images_id = serializers.PrimaryKeyRelatedField(write_only=True, many=True, queryset=TransformedImage.objects.all())    

    class Meta:
        model = TransformationRequest
        fields = ('id', 'images', 'images_id', 'last_modified')

    def create(self, validated_data):
        images_id = validated_data.pop('images_id', None)
        print('images_id data ', images_id)
        transformation_request = super(TransformationRequestSerializer, self).create(validated_data)
        transformation_request.images.add(*images_id)
        return transformation_request
        