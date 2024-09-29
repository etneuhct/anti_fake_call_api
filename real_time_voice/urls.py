from django.urls import path

from rest_framework.routers import DefaultRouter

from real_time_voice.views import voice_call

urlpatterns = [
    path('call', voice_call.incoming_voice_call, name='incoming_voice_call')
]
