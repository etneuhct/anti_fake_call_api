import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from conversation.constants import UserVirtualPhoneNumberStatus, ConversationHistoryCallingStatus, \
    ConversationHistoryAnalysisStatus

UserModel = get_user_model()


class VirtualPhoneNumber(models.Model):
    """
    Twillio's phone numbers are stored here
    """
    phone_number = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)


class UserPhoneNumber(models.Model):
    phone_number = models.CharField(max_length=30)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "phone_number")


class Contact(models.Model):
    phone_number = models.CharField(max_length=30, unique=True)
    whitelisted = models.BooleanField(default=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    first_name = models.CharField(null=True, blank=True, max_length=40)
    last_name = models.CharField(null=True, blank=True, max_length=40)

    class Meta:
        unique_together = ('user', 'phone_number')


class UserVirtualPhoneNumber(models.Model):
    status = models.IntegerField(default=UserVirtualPhoneNumberStatus.pending)
    created_at = models.DateTimeField(default=now)

    user_phone_number = models.ForeignKey("UserPhoneNumber", on_delete=models.CASCADE)
    virtual_phone_number = models.ForeignKey("VirtualPhoneNumber", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user_phone_number", "virtual_phone_number")


class ConversationHistory(models.Model):
    """
    Every conversation handled by the service should be recorded
    So the user can see what we do for him
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    calling_status = models.IntegerField(default=ConversationHistoryCallingStatus.pending)
    analysis_status = models.IntegerField(default=ConversationHistoryAnalysisStatus.pending)

    created_at = models.DateTimeField(default=now)
    started_at = models.DateTimeField(default=now)
    ended_at = models.DateTimeField(null=True, blank=True)

    conversations = models.JSONField(default=list)
    insights = models.JSONField(default=list)

    user_virtual_phone_number = models.ForeignKey("UserVirtualPhoneNumber", on_delete=models.CASCADE)
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE)


class PhoneNumberVerification(models.Model):
    user_phone_number = models.ForeignKey("UserPhoneNumber", on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=now)
