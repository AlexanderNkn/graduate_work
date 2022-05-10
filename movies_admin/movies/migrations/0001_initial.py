# Generated by Django 3.2 on 2022-05-10 09:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('creation_year', models.TextField(blank=True, verbose_name='creation date')),
                ('creation_date', models.DateField(blank=True, verbose_name='creation date')),
                ('certificate', models.TextField(blank=True, verbose_name='certificate')),
                ('kinopoisk_id', models.TextField(blank=True, verbose_name='certificate')),
                ('file_path', models.FileField(blank=True, upload_to='film_works/', verbose_name='file')),
                ('rating', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='rating')),
                ('type', models.CharField(choices=[('movie', 'movie'), ('tv_show', 'TV Show'), ('unknown', 'unknown')], max_length=20, verbose_name='type')),
            ],
            options={
                'verbose_name': 'filmwork',
                'verbose_name_plural': 'filmworks',
                'db_table': 'content\".\"film_work',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='FilmworkGenre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'content\".\"genre_film_work',
            },
        ),
        migrations.CreateModel(
            name='FilmworkPerson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[
                    ('actor', 'actor'),
                    ('director', 'director'),
                    ('writer', 'writer'),
                    ('operator', 'operator'),
                    ('editor', 'editor'),
                    ('composer', 'composer'),
                    ('producer_ussr', 'producer_ussr'),
                    ('translator', 'translator'),
                    ('design', 'design'),
                    ('producer', 'producer'),
                    ('voice_director', 'voice_director'),
                    ('unknown', 'unknown')
                ], max_length=20, verbose_name='role')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'content\".\"person_film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'content\".\"genre',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255, verbose_name='full name')),
                ('birth_date', models.DateField(blank=True, verbose_name='birth date')),
                ('kinopoisk_id', models.TextField(blank=True, verbose_name='certificate')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
                'db_table': 'content\".\"person',
                'ordering': ('full_name',),
            },
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['updated_at'], name='person_updated_at_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['birth_date'], name='person_birth_date_idx'),
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['updated_at'], name='genre_updated_at_idx'),
        ),
        migrations.AddField(
            model_name='filmworkperson',
            name='film_work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork'),
        ),
        migrations.AddField(
            model_name='filmworkperson',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.person'),
        ),
        migrations.AddField(
            model_name='filmworkgenre',
            name='film_work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork'),
        ),
        migrations.AddField(
            model_name='filmworkgenre',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.FilmworkGenre', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.FilmworkPerson', to='movies.Person'),
        ),
        migrations.AddConstraint(
            model_name='filmworkperson',
            constraint=models.UniqueConstraint(fields=('film_work', 'person'), name='person_film_work_film_work_id_person_id_uniq'),
        ),
        migrations.AddConstraint(
            model_name='filmworkgenre',
            constraint=models.UniqueConstraint(fields=('film_work', 'genre'), name='genre_film_work_film_work_id_genre_id_uniq'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['updated_at'], name='film_work_updated_at_idx'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
        ),
    ]
