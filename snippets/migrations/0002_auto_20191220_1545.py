# Generated by Django 2.2.7 on 2019-12-20 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snippet',
            old_name='owner',
            new_name='user',
        ),
    ]
