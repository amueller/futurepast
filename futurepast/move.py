import types
import inspect
import functools
import warnings

from .deprecate import _attach_class_warning, FutureDeprecationWarning

# like functools.WRAPPER_ASSIGNMENTS but without __name__
WRAPPER_ASSIGNMENTS = ['__doc__', '__module__', '__annotations__']


class move(object):
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

    def __call__(self, obj):
        if isinstance(obj, type):
            return self._move_class(obj)
        elif isinstance(obj, types.FunctionType):
            return self._move_function(obj)
        else:
            raise ValueError("Unsupported type for move: {}".format(type(obj)))

    def _move_class(self, obj):
        OldClass = type(self.old, (obj,), {})
        for attr in WRAPPER_ASSIGNMENTS:
            setattr(OldClass, attr, getattr(obj, attr, None))
        DeprecatedOldClass = _attach_class_warning(
            OldClass, self._make_message(obj))

        # insert into name namespace of object
        module = inspect.getmodule(obj)
        module.__dict__[self.old] = DeprecatedOldClass
        return obj

    def _move_function(self, obj):

        @functools.wraps(obj)
        def old_function(*args, **kwargs):
            warnings.warn(self._make_message(obj),
                          category=FutureDeprecationWarning)
            return obj(*args, **kwargs)

        old_function.__name__ = self.old

        module = inspect.getmodule(obj)
        module.__dict__[self.old] = old_function
