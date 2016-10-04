import types


class _BaseDecorator(object):
    def __init__(self, past, future):
        self.past = past
        self.future = future

    def __call__(self, obj):
        if isinstance(obj, type):
            return self._decorate_class(obj)
        elif isinstance(obj, types.FunctionType):
            return self._decorate_function(obj)
        else:
            raise ValueError("Unsupported type for {}: {}".format(
                self.__class__.__name__, type(obj)))
