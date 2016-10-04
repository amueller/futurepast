import types
import inspect

from .deprecate import _attach_class_warning

# like functools.WRAPPER_ASSIGNMENTS but without __name__
WRAPPER_ASSIGNMENTS = ['__doc__', '__module__', '__annotations__']


class move(object):
    def __init__(self, old, past, future):
        self.old = old
        self.past = past
        self.future = future

    def __call__(self, obj):
        if isinstance(obj, type):
            return self._move_class(obj)
        elif isinstance(obj, types.FunctionType):
            return self._move_function(obj)
        else:
            raise ValueError("Unsupported type for move: {}".format(type(obj)))

    def _move_class(self, obj):
        module = inspect.getmodule(obj)
        OldClass = type(self.old, (obj,), {})
        for attr in WRAPPER_ASSIGNMENTS:
            setattr(OldClass, attr, getattr(obj, attr, None))
        DeprecatedOldClass = _attach_class_warning(
            OldClass, "Class {} was renamed to {} in version {} and will "
            "be removed in version {}.".format(
                self.old, obj.__name__, self.past, self.future))
        module.__dict__[self.old] = DeprecatedOldClass
        return obj
