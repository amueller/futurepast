import inspect
import warnings
from functools import wraps
from .deprecate import FutureDeprecationWarning


class rename_parameter(object):
    def __init__(self, old, new, past, future):
        self.old = old
        self.new = new
        self.past = past
        self.future = future

    def __call__(self, func):
        parameters = inspect.signature(func).parameters
        if self.old in parameters.keys():
            raise ValueError(
                "Old parameter {} already exists in {} {}. The old "
                "parameter should be removed from the signature.".format(
                    self.old, type(func).__name__, func.__name__))
        if self.new not in parameters.keys():
            raise ValueError(
                "New parameter {} not present in {} {}. The new "
                "parameter needs to be added to the signature.".format(
                    self.new, type(func).__name__, func.__name__))

        message = ("Parameter {} was renamed to {} in version {} and will"
                   " be removed in version {}.".format(self.old, self.new,
                                                       self.past, self.future))

        @wraps(func)
        def func_with_both(*args, **kwargs):
            if self.old in kwargs.keys() and self.new in kwargs.keys():
                raise ValueError(
                    "Value passed for parameter {0} and parameter {1}."
                    "Parameter {1} replaces {0} and {0} should not be "
                    "set.".format(self.old, self.new))
            if self.old in kwargs.keys():
                warnings.warn(message, category=FutureDeprecationWarning)
                old_value = kwargs.pop(self.old)
                kwargs[self.new] = old_value
                return func(*args, **kwargs)
            return func(*args, **kwargs)

        return func_with_both
