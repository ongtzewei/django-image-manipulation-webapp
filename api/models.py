import uuid
from django.db import models
from api.utils import image_upload_path


class TransformedImage(models.Model):

  class ImageSource(models.IntegerChoices):
    Upload = 1, 'Upload'
    Remote = 2, 'Remote'

  id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  source = models.PositiveSmallIntegerField(choices=ImageSource.choices, default=ImageSource.Upload)
  # original_file is either an image uploaded via a POST request or retrieved from a URL
  source_path = models.URLField(null=True, blank=True)
  original_file = models.ImageField(upload_to=image_upload_path, max_length=255)
  transformed_file = models.ImageField(upload_to=image_upload_path, max_length=255)
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

  class Meta:
    app_label = 'api'
    db_table = 'transformed_image'


class TransformationRequest(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  images = models.ManyToManyField(TransformedImage, related_name='process_requests')
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)

  class Meta:
    app_label = 'api'
    db_table = 'transformation_request'