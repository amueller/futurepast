import pytest
from futurepast import rename_parameter, FutureDeprecationWarning


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
