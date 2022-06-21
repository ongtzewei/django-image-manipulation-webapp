from django.contrib import admin
from api.models import UploadImage, UploadRequest


class UploadRequestAdmin(admin.ModelAdmin):
  filter_horizontal = ('images',)


# Register your models here.
admin.site.register(UploadImage)
admin.site.register(UploadRequest, UploadRequestAdmin)
