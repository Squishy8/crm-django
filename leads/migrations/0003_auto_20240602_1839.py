# Generated by Django 3.1.4 on 2024-06-03 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_auto_20240602_1745'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agent',
            old_name='organization',
            new_name='organisation',
        ),
    ]
