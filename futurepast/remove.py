from .deprecate import _attach_class_warning


class remove(object):
    def __init__(self, past, future):
        self.past = past
        self.future = future

    def _make_message(self, obj):
        if isinstance(obj, type):
            name = "Class"
        else:
            name = "Function"

        return ("{} {} was scheduled for removal in version {} and will "
                "be removed in version {}.".format(
                    name, obj.__name__, self.past, self.future))

    def _decorate_class(self, obj):
        return _attach_class_warning(obj, self._make_message(obj))

    def _decorate_function(self, obj):
        pass
