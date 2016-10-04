from futurepast import move, FutureDeprecationWarning
import pytest


def test_move_class():
    @move("OldEmptyClass", 0.1, 0.2)
    class EmptyClass(object):
        pass

    with pytest.warns(FutureDeprecationWarning) as warnings:
        OldEmptyClass()

    assert len(warnings) == 1
    message = ('Class OldEmptyClass was renamed to EmptyClass in '
               'version 0.1 and will be removed in version 0.2.')
    assert warnings[0].message.args[0] == message


def test_move_func():
    @move("old_func", 0.1, 0.2)
    def func(x):
        return x

    with pytest.warns(FutureDeprecationWarning) as warnings:
        old_func(10)

    assert len(warnings) == 1
    message = ('Function old_func was renamed to func in '
               'version 0.1 and will be removed in version 0.2.')
    assert warnings[0].message.args[0] == message
