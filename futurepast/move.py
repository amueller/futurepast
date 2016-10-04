import inspect

from .deprecate import _attach_class_warning, _attach_function_warning
from .base import _BaseDecorator

# like functools.WRAPPER_ASSIGNMENTS but without __name__
WRAPPER_ASSIGNMENTS = ['__doc__', '__module__', '__annotations__']


class move(_BaseDecorator):
    def __init__(self, old, past, future):
        self.old = old
        self.past = past
        self.future = future

    def _make_message(self, obj):
        if isinstance(obj, type):
            name = "Class"
        else:
            name = "Function"

        return ("{} {} was renamed to {} in version {} and will "
                "be removed in version {}.".format(
                    name, self.old, obj.__name__, self.past,
                    self.future))

    def _decorate_class(self, obj):
        OldClass = type(self.old, (obj,), {})
        for attr in WRAPPER_ASSIGNMENTS:
            setattr(OldClass, attr, getattr(obj, attr, None))
        DeprecatedOldClass = _attach_class_warning(
            OldClass, self._make_message(obj))

        # insert into name namespace of object
        module = inspect.getmodule(obj)
        module.__dict__[self.old] = DeprecatedOldClass
        return obj

    def _decorate_function(self, obj):

        old_function = _attach_function_warning(
            obj, self._make_message(obj))

        old_function.__name__ = self.old

        module = inspect.getmodule(obj)
        module.__dict__[self.old] = old_function
