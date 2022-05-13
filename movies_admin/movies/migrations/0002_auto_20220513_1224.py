# Generated by Django 3.2 on 2022-05-13 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmwork',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='movie_images/', verbose_name='screenshots'),
        ),
        migrations.AddField(
            model_name='person',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='person_images/', verbose_name='photos'),
        ),
    ]