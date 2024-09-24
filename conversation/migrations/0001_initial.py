# Generated by Django 5.0 on 2024-09-24 20:05

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualPhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=30, unique=True)),
                ('whitelisted', models.BooleanField(default=False)),
                ('first_name', models.CharField(blank=True, max_length=40, null=True)),
                ('last_name', models.CharField(blank=True, max_length=40, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'phone_number')},
            },
        ),
        migrations.CreateModel(
            name='UserPhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=30)),
                ('verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'phone_number')},
            },
        ),
        migrations.CreateModel(
            name='PhoneNumberVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_phone_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conversation.userphonenumber')),
            ],
        ),
        migrations.CreateModel(
            name='UserVirtualPhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_phone_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conversation.userphonenumber')),
                ('virtual_phone_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conversation.virtualphonenumber')),
            ],
            options={
                'unique_together': {('user_phone_number', 'virtual_phone_number')},
            },
        ),
        migrations.CreateModel(
            name='ConversationHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('calling_status', models.IntegerField(default=0)),
                ('analysis_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('started_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('conversations', models.JSONField(default=list)),
                ('insights', models.JSONField(default=list)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conversation.contact')),
                ('user_virtual_phone_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conversation.uservirtualphonenumber')),
            ],
        ),
    ]
