# Generated by Django 5.0 on 2024-09-22 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('third_parties', '0002_rename_speechtotext_thirdparty_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ThirdParty',
        ),
    ]
