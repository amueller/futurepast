import pytest
from futurepast import (rename_parameter, change_default, remove_parameter,
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


def test_remove_param():
    @remove_parameter(old="old_parameter", past=2.3, future=10)
    def myfunc(old_parameter="default_value", new_parameter=42):
        return old_parameter

    with pytest.warns(FutureDeprecationWarning) as warnings:
        result = myfunc(old_parameter="not default")

    assert result == "not default"
    assert len(warnings) == 1
    message = ('Parameter old_parameter was scheduled for removal in version '
               '2.3 and will be removed in version 10.')
    assert warnings[0].message.args[0] == message


def test_change_default():

    @change_default(parameter="myparam", old="old_value", past=23, future=42)
    def myfunc(myparam="new_value", another_param="value"):
        return myparam

    # if we set the param, no warning
    result = myfunc(myparam="not default")

    assert result == "not default"

    # don't set the param, get old behavior and warning
    with pytest.warns(FutureDeprecationWarning) as warnings:
        result = myfunc(another_param="not default")

    assert result == "old_value"
    assert len(warnings) == 1
    message = ('The default value of parameter myparam was schedule to change'
               ' from old_value to new_value in version 23. The change will '
               'happen in version 42.')
    assert warnings[0].message.args[0] == message
