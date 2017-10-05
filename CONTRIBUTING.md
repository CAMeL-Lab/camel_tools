# Contributing

## Coding Style Guidelines
For the most part, contributers should adhere to the [pep8](https://www.python.org/dev/peps/pep-0008) style guide. Since pep8 is a bit ambiguous in some cases, we enforce the additional rules below.

### Source files:

All Python source files should be UTF-8 encoded with the UTF-8 header on top like so:
```python
# -*- coding: utf-8 -*-
```

Standalone scripts should also have a hashbang header like so:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
```

### Indentation:

* Each indentation level is 4 spaces (no tabs).
* Arguments should be aligned with the opening delimiter as in the first example [pep8 indentation section](https://www.python.org/dev/peps/pep-0008/#indentation).
* If arguments are to be split into multiple lines, there should only be one argument per line.

### Strings:

* Always using single-quoted strings except for docstrings (as per [pep8](https://www.python.org/dev/peps/pep-0008/#string-quotes)).
* Use the new string formatting API `'{}'.format(x)` instead of `'%s' % (x,)` ([see here for more information](https://pyformat.info/)).

### Naming Conventions:

* Classes are always in camel case (eg. `SomeClass`).
* Variables, functions, and methods are always mixed case (eg. `someVar`)

If we missed to mention a particular case, you should always follow the below procedure:

1. See how it's done in the codebase.
2. See what pep8 says and choose something that's close to the codebase.
3. If all else fails, ask :)


## Python 2 and 3 support

CAMeL tools should be able to run on Python 2 and 3.
[Here's a nice cheat-sheet](http://python-future.org/compatible_idioms.html) of how to do that.


## Submitting pull requests

* All commits should be signed ([see here](https://help.github.com/articles/signing-commits-using-gpg/) for more information).
