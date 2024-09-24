from conversation.views.phone_number_verification_views import PhoneNumberVerificationViewSet
from conversation.views.conversation_history_views import ConversationHistoryViewSet
from conversation.views.user_virtual_phone_number_views import UserVirtualPhoneNumberViewSet
from conversation.views.contact_views import ContactViewSet
from conversation.views.user_phone_number_views import UserPhoneNumberViewSet
from conversation.views.virtual_phone_number_views import VirtualPhoneNumberViewSet
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('virtual-phone-number', VirtualPhoneNumberViewSet, basename='virtual-phone-number')
router.register('user-phone-number', UserPhoneNumberViewSet, basename='user-phone-number')
router.register('contact', ContactViewSet, basename='contact')
router.register('user-virtual-phone-number', UserVirtualPhoneNumberViewSet, basename='user-virtual-phone-number')
router.register('conversation-history', ConversationHistoryViewSet, basename='conversation-history')
router.register('phone-number-verification', PhoneNumberVerificationViewSet, basename='phone-number-verification')
# registration

urlpatterns = [
    path('', include(router.urls))
]