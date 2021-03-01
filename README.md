[![Actions Status](https://github.com/procsea/django-remove-field/workflows/CI/badge.svg)](https://github.com/procsea/django-remove-field/actions)


# django_remove_field

Help to remove a django model fields without downtime.

## Soft deprecation

Use `@deprecated_fields(fieldnames=[])` to generate logs when one of the fieldnames is used:

```python
@deprecated_fields(["is_active"])
class ModelWithDeprecatedField(models.Model):
    name = models.CharField(max_length=64)
    is_active = models.BooleanField()
```

## Hard deprecation

Use `@removed_field(fieldnames=[])` to raise error when one of the fieldnames is used:

```python
@removed_fields(["is_active"])
class ModelWithRemovedField(models.Model):
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(null=True)
```

## DB migration

When you run migration (`makemigrations`, `migrate`, ...), set the environment variable `DJANGO_REMOVE_FIELD_DISABLED`
to not generate remove field migration.

## developers

Run all tests with `make test`

We need to run twice tests with different value for environment variable to be able
to test the both case (using the decorator and ignoring decorator)