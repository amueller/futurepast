# futurepast
Deprecation tools for Python (and humans)

## What are deprecations?

Past me is often sloppy and makes bad decisions. Like giving functions or
classes bad names, putting them in the wrong module, or choosing bad default
values.

Present me likes to fix this.
But if someone else is actually using my code, any change to the user-facing
API will break their code, make them unhappy, and in the end maybe even make
them stop using my code.

Some API changes can be dealt with in a way that doesn't break user code,
though, through deprecations. Here is what I want from a deprecations:

- If the user is relying on the old API, warn them that this API will be
  changed / removed in the future, and tell them how to fix it.
- Allow the user to change the code so they can make use of the new API.
- Make sure the user never has to worry about this ever again.
- Drop the old behavior at some point in the future, when all users had a
  chance to change their code.

The key idea is to allow users to choose when to go from the old API to the new
API. The user is bugged with warnings until they take action and change their
code.  After the user took action, they shouldn't be bugged any more, though.
When the old API is finally removed, the user shouldn't need to take any
further action.

## What does futurepast do?
The futurepast library is meant to make deprecations as pain-free for
developers as possible, and help you to make sure no API is broken
accidentally.

It provides helpers to
- rename, move and remove functions, methods, attributes, classes, modules and constants
- rename and remove parameters
- change default values of parameters


## How does it work?

Let's say we are in version ``old_version`` and we want to remove the old
API in ``new_version``.

```python

# remove a class
from futurepast import remove

@remove(past=old_version, future=new_version)
class MyClass(object):
    pass


# remove a method

class MyClass(object):
    @remove(past=old_version, future=new_version)
    def my_method(self):
        pass


# renamed a class from OldClass to NewClass
from futurepast import move

@move(old="OldClass", past=old_version, future=new_version)
class NewClass(object):
    pass


# renaming parameter old_parameter to new_parameter

from futurepast import rename_parameter

@rename_parameter(old="old_parameter", new="new_parameter", past=old_version, future=new_version)
def myfunc(new_parameter=default_value):
    pass


# changing default value of parameter

from futurepast import changed_default

@change_default(old=old_default, past=old_version, future=new_version)
def myfunc(parameter=new_default)
    pass

```

To make it easy for the developer, any deprecation from ``futurepast`` will
raise an error once ``future`` (that is ``new_version``) arrives, so you know
when to get rid of the old code.

Once the future arrives, it is enough to simply remove the ``futurepast``
decorator.

## Assumptions on deprecations

There are some assumptions that are made here for this to work, in particular:

- Your users update frequently enough (which is the same as you wait long
  enough between deprecation and removal) that they will at some point use
  the version with the deprecation warning.
- Someone looks at the output of the code and sees the warning.
- They will actually take action.

The first one is the most tricky one, because it's the one you have to worry
about. The second and third are somewhat on the users of your code.

## So is all good?

Given the requirements on deprecations given above, some things can not be
handled nicely. For example changing the return value of a function is not
possible in this way, which is something I want to do A LOT.
The best work-around might be to rename the function and give the new function
the new behavior.
There also currently no way to move anything into a different module automatically
(because I haven't figured out how).

## Patterns to avoid
- Avoid deprecations at all cost! Even if they are safe, they are still a hassle for the user!
- Don't break API without letting the user adjust!
- Don't make the user change the code twice, once on deprecation and once on removal!
- Don't keep warning the user after they made the change!
