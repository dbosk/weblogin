# weblogin

`weblogin` is a Python package that allows transparent logging in to web UIs to 
access their unofficial APIs.

`/doc` contains the source for the documented source code.

`/src` contains the literate package source. Must be compiled to Python code 
using NOWEB. Simply run `make`.

`/tests` contains tests. Run `make` in that directory to run them.

## Debug logging

`weblogin` uses Python's `logging` module for debug output, but does not
configure logging handlers itself.

In a normal program that imports `weblogin`, you typically configure logging
once in your own main module using `logging.basicConfig(...)`.

If you want debug output from everything, including `weblogin`, this is enough:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

If you only want debug output from `weblogin`, keep your application's general
log level higher and enable `weblogin` separately:

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("weblogin").setLevel(logging.DEBUG)
```

This works because `weblogin` uses loggers named from its module names, such as
`weblogin`, `weblogin.kth`, and `weblogin.microsoft`, and those follow the
standard Python logging hierarchy.

If your application already configures logging elsewhere, enabling debug
logging for `weblogin` can be just:

```python
import logging

logging.getLogger("weblogin").setLevel(logging.DEBUG)
```

This enables debug logs for `weblogin` and its submodules.
