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


class remove_parameter(object):
    def __init__(self, old, past, future):
        self.old = old
        self.past = past
        self.future = future

    def __call__(self, func):
        parameters = inspect.signature(func).parameters
        if self.old not in parameters.keys():
            raise ValueError(
                "Old parameter {} not present in {} {}. The old "
                "parameter needs to be added to the signature.".format(
                    self.new, type(func).__name__, func.__name__))

        message = ("Parameter {} was scheduled for removal in version {} and"
                   " will be removed in version {}.".format(
                       self.old, self.past, self.future))

        @wraps(func)
        def func_with_both(*args, **kwargs):
            if self.old in kwargs.keys():
                warnings.warn(message, category=FutureDeprecationWarning)
            return func(*args, **kwargs)

        return func_with_both


class change_default(object):
    def __init__(self, parameter, old, past, future):
        self.parameter = parameter
        self.old = old
        self.past = past
        self.future = future

    def __call__(self, func):
        parameters = inspect.signature(func).parameters
        if self.parameter not in parameters.keys():
            raise ValueError(
                "Parameter {} not present in {} {}.".format(
                    self.parameter, type(func).__name__, func.__name__))

        new = parameters[self.parameter].default

        message = ("The default value of parameter {} was schedule to "
                   "change from {} to {} in version {}. The change will "
                   "happen in version {}.".format(self.parameter, self.old,
                                                  new, self.past, self.future))

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if self.parameter not in kwargs.keys():
                kwargs[self.parameter] = self.old
                warnings.warn(message, category=FutureDeprecationWarning)
            return func(*args, **kwargs)

        return wrapped_func
