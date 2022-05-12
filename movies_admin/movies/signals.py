from typing import Type, Union

from django.db import models
from django.db.models.signals import pre_delete
from django.utils import timezone

from .models import Filmwork, Genre, Person

T = Union[Genre, Person]  # noqa: WPS111


def update_filmwork(sender: Type[T], instance: T, *args, **kwargs) -> None:
    filter_params = models.Q(genres=instance) if isinstance(instance, Genre) else models.Q(persons=instance)
    Filmwork.objects.filter(filter_params).update(updated_at=timezone.now())


models_for_trigger = (Genre, Person)
for sender in models_for_trigger:
    pre_delete.connect(receiver=update_filmwork, sender=sender)
