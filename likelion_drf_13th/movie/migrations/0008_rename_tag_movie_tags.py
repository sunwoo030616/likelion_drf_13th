# Generated by Django 4.2.23 on 2025-07-26 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_rename_tags_movie_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='tag',
            new_name='tags',
        ),
    ]
