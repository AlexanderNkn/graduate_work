# Generated by Django 3.2 on 2022-05-10 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20220510_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmwork',
            name='duration',
            field=models.IntegerField(blank=True, default=0, verbose_name='duration'),
        ),
    ]
