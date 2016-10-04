from futurepast import remove, FutureDeprecationWarning
import pytest


def test_move_class():
    @remove(0.1, 0.2)
    class OldEmptyClass(object):
        pass

    with pytest.warns(FutureDeprecationWarning) as warnings:
        OldEmptyClass()

    assert len(warnings) == 1
    message = ('Class OldEmptyClass was scheduled for removal in '
               'version 0.1 and will be removed in version 0.2.')
    assert warnings[0].message.args[0] == message


def test_move_func():
    @remove(0.1, 0.2)
    def old_func(x):
        return x

    with pytest.warns(FutureDeprecationWarning) as warnings:
        old_func(10)

    assert len(warnings) == 1
    message = ('Function old_func was scheduled for removal in '
               'version 0.1 and will be removed in version 0.2.')
    assert warnings[0].message.args[0] == message
