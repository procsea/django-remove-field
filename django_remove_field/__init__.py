import logging
import os
import warnings

logger = logging.getLogger(__file__)


class DeprecatedModelFieldsDecorator:
    def __init__(self, fieldnames):
        self.fieldnames = fieldnames

    def __call__(self, decorated):
        decorated__getattribute__ = decorated.__getattribute__
        decorated__setattr__ = decorated.__setattr__

        def __getattribute__(inner_self, name):
            if name in self.fieldnames:
                logger.warning("Calling deprecated field '%s'", name)
                warnings.warn(f"Calling deprecated field '{name}'")
            return decorated__getattribute__(inner_self, name)

        def __setattr__(inner_self, name, value):
            if name in self.fieldnames:
                logger.warning("Setting deprecated field '%s'", name)
                warnings.warn(f"Setting deprecated field '{name}'")
            return decorated__setattr__(inner_self, name, value)

        decorated.__getattribute__ = __getattribute__
        decorated.__setattr__ = __setattr__
        return decorated


class RemovedModelFieldsDecorator:
    def __init__(self, fieldnames):
        self.fieldnames = fieldnames

    def __call__(self, decorated):
        if os.environ.get("DJANGO_REMOVE_FIELD_DISABLED") is not None:
            return decorated
        decorated__init__ = decorated.__init__
        decorated__setattr__ = decorated.__setattr__

        def __setattr__(inner_self, name, value):
            if name in self.fieldnames:
                raise AttributeError(
                    f"Field '{name}' is deprecated and should not be called anymore"
                )
            return decorated__setattr__(inner_self, name, value)

        def __init__(innerself, *args, **kwargs):
            for fieldname, value in kwargs.items():
                if fieldname in self.fieldnames:
                    raise AttributeError(
                        f"Field '{fieldname}' is deprecated and should not be set anymore"
                    )

            decorated__init__(innerself, *args, **kwargs)

        decorated.__init__ = __init__
        decorated._meta.local_fields = [
            field
            for field in decorated._meta.local_fields
            if field.name not in self.fieldnames
        ]
        decorated.__setattr__ = __setattr__
        return decorated


deprecated_fields = DeprecatedModelFieldsDecorator
removed_fields = RemovedModelFieldsDecorator
