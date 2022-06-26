from rest_framework import routers
from django.urls import include, path, re_path
from api import views as api_views


router = routers.SimpleRouter(trailing_slash=False)
router.register('images', api_views.UploadViewSet)
router.register("images", api_views.ImageViewSet)
urlpatterns = [
    re_path(r'^images/(?P<pk>[^.]+)\.(?P<format>[a-z]+)$',
      api_views.transform_image, name='transform-image'),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
