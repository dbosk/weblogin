We want to use APIs from web UIs that require login. What we want to do
is to set up a session, login and then use the API of the page. The
reason we want to do this is to use existing APIs. For instance, the
user group management service at KTH, see
[1](#UGEditor){reference-type="ref" reference="UGEditor"}. We can then
use the service, track the requests in the browser's developer tools.
Then we can simply make the same requests from Python.

![Screenshot of the KTH UG Editor with Firefox's Developer Tools open,
showing network requests made.](https://github.com/dbosk/weblogin/raw/main/doc/figs/ug.png){#UGEditor width="\\columnwidth"}

For instance, we can redo the request in
[1](#UGEditor){reference-type="ref" reference="UGEditor"} like this:

``` {.python}
from weblogin.kth import AutologinSession
import os

ug = AutologinSession(os.environ["KTH_LOGIN"],
                      os.environ["KTH_PASSWD"],
                      "https://app.kth.se/ug-gruppeditor/")

response = ug.get("https://app.kth.se/ug-gruppeditor/api/ug/users"
                  "?filter=memberOf eq 'u26yk1i3'")
```

The code above will access the API used by the KTH UG group editor
service. It will automatically sign in when needed. The API URLs don't
trigger a redirect to log in, they just give a 401 unauthorized error.
However, we can use the main URL to the UI to trigger such an event, log
in and then access the API. All this happens automatically in the
background.

The way we do this is to subclass the `requests.Session` class to
intercept all requests of a session to check for signs indicating that
we must log in. When we detect such sign, we log in and resume as if
nothing ever happened.
