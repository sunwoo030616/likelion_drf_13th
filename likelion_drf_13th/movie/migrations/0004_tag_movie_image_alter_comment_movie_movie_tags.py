# Generated by Django 4.2.23 on 2025-07-26 11:54

from django.db import migrations, models
import django.db.models.deletion
import movie.models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=movie.models.image_upload_path),
        ),
        migrations.AlterField(
            model_name='comment',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='movie.movie'),
        ),
        migrations.AddField(
            model_name='movie',
            name='tags',
            field=models.ManyToManyField(blank=True, to='movie.tag'),
        ),
    ]
