import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = "content\".\"genre"
        ordering = ('name',)
        indexes = [
            models.Index(fields=('updated_at',), name='genre_updated_at_idx'),
        ]

    def __str__(self) -> str:
        return self.name


class FilmworkGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'genre'],
                name='genre_film_work_film_work_id_genre_id_uniq'
            ),
        ]

    def __str__(self) -> str:
        return ''


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV Show')
    UNKNOWN = 'unknown', _('unknown')


class Filmwork(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_year = models.CharField(_('creation year'), max_length=20, blank=True, null=True)
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    certificate = models.TextField(_('certificate'), blank=True, null=True)
    kinopoisk_id = models.CharField(_('kinopoisk_id'), max_length=20, blank=True, null=True)
    file_path = models.FileField(_('file'), upload_to='film_works/', blank=True, null=True)
    rating = models.FloatField(_('rating'), validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True)
    duration = models.IntegerField(_('duration'), default=0, blank=True)
    type = models.CharField(_('type'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through=FilmworkGenre)
    persons = models.ManyToManyField('Person', through='FilmworkPerson')

    class Meta:
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = "content\".\"film_work"
        ordering = ('title',)
        indexes = [
            models.Index(fields=('updated_at',), name='film_work_updated_at_idx'),
            models.Index(fields=('creation_date',), name='film_work_creation_date_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['kinopoisk_id'],
                name='film_work_kinopoisk_id_uniq'
            ),
        ]

    def __str__(self) -> str:
        return self.title


class Person(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(_('full name'), max_length=255)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    kinopoisk_id = models.TextField(_('kinopoisk_id'), blank=True, null=True)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        db_table = "content\".\"person"
        ordering = ('full_name',)
        indexes = [
            models.Index(fields=('updated_at',), name='person_updated_at_idx'),
            models.Index(fields=('birth_date',), name='person_birth_date_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['kinopoisk_id'],
                name='person_kinopoisk_id_uniq'
            ),
        ]

    def __str__(self) -> str:
        return self.full_name


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('actor')
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')
    OPERATOR = 'operator', _('operator')
    EDITOR = 'editor', _('editor')
    COMPOSER = 'composer', _('composer')
    PRODUCER_USSR = 'producer_ussr', _('producer_ussr')
    TRANSLATOR = 'translator', _('translator')
    DESIGN = 'design', _('design')
    PRODUCER = 'producer', _('producer')
    VOICE_DIRECTOR = 'voice_director', _('voice_director')
    UNKNOWN = 'unknown', _('unknown')


class FilmworkPerson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=20, choices=RoleType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person'],
                name='person_film_work_film_work_id_person_id_uniq'
            ),
        ]

    def __str__(self) -> str:
        return ''
