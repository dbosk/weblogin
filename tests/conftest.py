import copy
import os

import pytest

import weblogin
from weblogin import microsoft
from weblogin.kth import UGlogin


def make_kth_live_session(trigger_url):
    return weblogin.AutologinSession(
        [
            UGlogin(
                os.environ["KTH_LOGIN"],
                os.environ["KTH_PASSWD"],
                trigger_url,
            ),
            microsoft.AzureMFA(
                url="https://login.ug.kth.se",
                notification_cmd="notify-send",
            ),
        ]
    )


@pytest.fixture(scope="session")
def kth_live_session():
    session = make_kth_live_session("https://app.kth.se/ug-gruppeditor/")
    return session


@pytest.fixture(scope="session")
def kth_form_live_session(kth_live_session):
    session = make_kth_live_session("https://www.kth.se/form/admin/")
    session.cookies.update(copy.copy(kth_live_session.cookies))
    return session
