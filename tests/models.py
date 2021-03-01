from django.db import models

from django_remove_field import deprecated_fields, removed_fields


@deprecated_fields(["is_active"])
class ModelWithDeprecatedField(models.Model):
    name = models.CharField(max_length=64)
    is_active = models.BooleanField()


@removed_fields(["is_active"])
class ModelWithRemovedField(models.Model):
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(null=True)
