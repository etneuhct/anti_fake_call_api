from third_parties.views.third_party_views import ThirdPartyViewSet
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('third-party', ThirdPartyViewSet, basename='third-party')
# registration

urlpatterns = [
    path('', include(router.urls))
]