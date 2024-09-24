from django.contrib import admin
from .models import VirtualPhoneNumber, UserVirtualPhoneNumber, Contact, UserPhoneNumber, ConversationHistory

# Register your models here.

for element in [VirtualPhoneNumber, UserVirtualPhoneNumber, Contact, UserPhoneNumber, ConversationHistory]:
    admin.site.register(element)
