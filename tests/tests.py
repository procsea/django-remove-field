import logging
import os
import unittest
from io import StringIO

from django.core.exceptions import FieldError
from django.core.management import call_command
from django.test import TestCase

from tests import models


@unittest.skipIf(
    bool(os.environ.get("DJANGO_REMOVE_FIELD_DISABLED")),
    reason="django_remove_field disabled",
)
class DeprecatedFieldTests(TestCase):
    def test_init_generate_log(self):
        with self.assertLogs(level=logging.WARNING):
            models.ModelWithDeprecatedField(name="test", is_active=True)

    def test_setattr_generate_log(self):
        _ = models.ModelWithDeprecatedField(name="test")
        with self.assertLogs(level=logging.WARNING):
            _.is_active = False
        with self.assertLogs(level=logging.WARNING):
            _ = models.ModelWithDeprecatedField(name="test", is_active=True)

    def test_getattr_generate_log(self):
        _ = models.ModelWithDeprecatedField(name="test")
        with self.assertLogs(level=logging.WARNING):
            _.is_active

    def test_create_in_db_generate_log(self):
        with self.assertLogs(level=logging.WARNING):
            models.ModelWithDeprecatedField.objects.create(name="test", is_active=True)

        bulk = [models.ModelWithDeprecatedField(name="test", is_active=True)]
        with self.assertLogs(level=logging.WARNING):
            models.ModelWithDeprecatedField.objects.bulk_create(bulk)


@unittest.skipIf(
    bool(os.environ.get("DJANGO_REMOVE_FIELD_DISABLED")),
    reason="django_remove_field disabled",
)
class RemovedFieldTests(TestCase):
    def test_save_in_db(self):
        models.ModelWithRemovedField(name="test").save()
        self.assertEqual(models.ModelWithRemovedField.objects.count(), 1)

    def test_create_in_db(self):
        models.ModelWithRemovedField.objects.create(name="test")
        self.assertEqual(models.ModelWithRemovedField.objects.count(), 1)

    def test_querying_removed_field_raise(self):
        models.ModelWithRemovedField.objects.create(name="test")
        with self.assertRaises(FieldError):
            models.ModelWithRemovedField.objects.filter(is_active=True)

    def test_init_raise(self):
        with self.subTest("on new instance"):
            with self.assertRaises(AttributeError):
                models.ModelWithRemovedField(name="test", is_active=True)

    def test_setattr_raise(self):
        _ = models.ModelWithRemovedField(name="test")
        with self.assertRaises(AttributeError):
            _.is_active = False


@unittest.skipIf(
    bool(os.environ.get("DJANGO_REMOVE_FIELD_DISABLED")),
    reason="django_remove_field disabled",
)
class ManagementCommandTest(TestCase):
    def test_makemigrations_generate_remove_field_migration(self):
        out = StringIO()
        call_command(
            "makemigrations",
            *["--dry-run", "-v3"],
            stdout=out,
        )
        self.assertIn("migrations.RemoveField", out.getvalue())


@unittest.skipIf(
    not bool(os.environ.get("DJANGO_REMOVE_FIELD_DISABLED")),
    reason="django_remove_field enabled",
)
class ManagementCommandWhenDisabledTest(TestCase):
    def test_makemigrations_generate_nothing(self):
        out = StringIO()
        call_command(
            "makemigrations",
            *["--dry-run", "-v3"],
            stdout=out,
        )
        self.assertEqual("No changes detected\n", out.getvalue())
