import pytest
from futurepast import (rename_parameter, change_default,
                        FutureDeprecationWarning)


def test_rename_parameter():
    @rename_parameter(old="old_parameter", new="new_parameter", past=2.3,
                      future=10)
    def myfunc(new_parameter="default_value"):
        return new_parameter

    with pytest.warns(FutureDeprecationWarning) as warnings:
        result = myfunc(old_parameter="not default")

    assert result == "not default"
    assert len(warnings) == 1
    message = ('Parameter old_parameter was renamed to new_parameter in '
               'version 2.3 and will be removed in version 10.')
    assert warnings[0].message.args[0] == message


def test_change_default():

    @change_default(parameter="myparam", old="old_value", past=23, future=42)
    def myfunc(myparam="new_value", another_param="value"):
        return myparam

    # if we set the param, no warning
    with pytest.warns(FutureDeprecationWarning) as warnings:
        result = myfunc(myparam="not default")

    assert result == "not default"
    assert len(warnings) == 0

    # don't set the param, get old behavior and warning
    with pytest.warns(FutureDeprecationWarning) as warnings:
        result = myfunc(another_param="not default")

    assert result == "old_value"
    assert len(warnings) == 1
    message = ('Parameter old_parameter was renamed to new_parameter in '
               'version 2.3 and will be removed in version 10.')
    assert warnings[0].message.args[0] == message
