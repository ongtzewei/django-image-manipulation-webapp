from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api import views as api_views

router = routers.DefaultRouter()
router.register('images', api_views.TransformedImageViewSet)
router.register('transform-images', api_views.TransformationRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
