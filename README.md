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
- rename and move functions, methods, attributes, classes, modules and constants
- rename parameters
- change default values of parameters


## How does it work?

```python
# renaming a parameter

from futurepast import MovedParameter

def myfunc(still_here, MovedParameter(

```

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
The best work-aroud might be to rename the function and give the new function
the new behavior.

## Patterns to avoid
- Don't break API without letting the user adjust!
- Don't make the user change the code twice, once on deprecation and once on removal!
- Don't keep warning the user after they made the change!
