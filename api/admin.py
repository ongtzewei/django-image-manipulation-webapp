from django.contrib import admin
from api.models import UploadImage, UploadRequest


class UploadImageAdmin(admin.ModelAdmin):
  list_display = ['id', 'source', 'transformed_file', 'created_on', 'last_modified']


class UploadRequestAdmin(admin.ModelAdmin):
  filter_horizontal = ('images',)
  list_display = ['id', 'created_on', 'last_modified']


# Register your models here.
admin.site.register(UploadImage, UploadImageAdmin)
admin.site.register(UploadRequest, UploadRequestAdmin)
