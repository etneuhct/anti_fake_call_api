# Generated by Django 5.0 on 2024-09-22 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConversationAnalyser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conversation', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SpeechToText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(max_length=10)),
                ('conversation', models.CharField(max_length=10)),
            ],
        ),
    ]
