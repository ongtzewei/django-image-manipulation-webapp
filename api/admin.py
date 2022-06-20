from django.contrib import admin
from api.models import TransformedImage, TransformationRequest

class TransformationRequestAdmin(admin.ModelAdmin):
  filter_horizontal = ('images',)

# Register your models here.
admin.site.register(TransformedImage)
admin.site.register(TransformationRequest, TransformationRequestAdmin)
