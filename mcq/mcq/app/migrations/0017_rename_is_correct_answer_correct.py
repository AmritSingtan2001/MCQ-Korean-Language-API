# Generated by Django 4.2.7 on 2023-12-05 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_categories_short_descriptions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='is_correct',
            new_name='correct',
        ),
    ]
