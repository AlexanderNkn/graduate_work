from typing import Type, Union

from django.db.models import Q
from django.db.models.signals import pre_delete
from django.utils import timezone

from .models import Filmwork, Genre, Person

T = Union[Genre, Person]


def update_filmwork(sender: Type[T], instance: T, *args, **kwargs) -> None:
    filter_params = Q(genres=instance) if isinstance(instance, Genre) else Q(persons=instance)
    Filmwork.objects.filter(filter_params).update(updated_at=timezone.now())


models_for_trigger = (Genre, Person)
for sender in models_for_trigger:
    pre_delete.connect(receiver=update_filmwork, sender=sender)
