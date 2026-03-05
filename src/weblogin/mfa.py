import getpass
import http.cookiejar
import os
import pickle
import re
import sys

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:
    raise ImportError(
        "weblogin.mfa requires Selenium. Install with: pip install weblogin[mfa]"
    )

import requests.cookies


def setup_browser():
    """Start a headless Chrome browser and return the driver."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=options)


def do_login(driver, username, password, trigger_url):
    """
    Navigate to trigger_url, fill credentials, handle MFA if needed.
    Raises RuntimeError on timeout.
    """
    driver.get(trigger_url)

    WebDriverWait(driver, 20).until(lambda d: "login.ug.kth.se" in d.current_url)

    uname = username if "@ug.kth.se" in username else username + "@ug.kth.se"
    driver.execute_script(
        "document.getElementById('userNameInput').value = arguments[0];", uname
    )
    driver.execute_script(
        "document.getElementById('passwordInput').value = arguments[0];", password
    )
    driver.execute_script("document.getElementById('submitButton').click();")

    def mfa_or_done(d):
        if not _on_login_page(d.current_url):
            return ("done", None)
        number = find_mfa_number(d)
        if number:
            return ("mfa", number)
        return None

    result = WebDriverWait(driver, 30).until(mfa_or_done)

    if result[0] == "mfa":
        number = result[1]
        print("\n" + "=" * 50)
        print("  Enter  {}  in Microsoft Authenticator".format(number))
        print("=" * 50 + "\n")
        WebDriverWait(driver, 120).until(lambda d: not _on_login_page(d.current_url))


def _on_login_page(url):
    return "login.ug.kth.se" in url or "microsoftonline.com" in url


_MFA_ELEMENT_IDS = [
    "idRichContext_DisplaySign",
    "displaySign",
    "idDiv_DisplaySign",
]


def find_mfa_number(driver):
    """
    Return the MFA number shown on the current page, or None if not present.
    """
    for eid in _MFA_ELEMENT_IDS:
        elems = driver.find_elements(By.ID, eid)
        if elems:
            txt = elems[0].text.strip()
            if txt:
                return txt
    body = driver.find_element(By.TAG_NAME, "body").text
    matches = re.findall(r"\b(\d{2})\b", body)
    return matches[0] if matches else None


def collect_cookies(driver, extra_urls=None):
    """
    Collect cookies from the browser and return a RequestsCookieJar.
    If extra_urls is given, also visit those URLs to pick up their cookies
    (useful when SSO spans multiple domains).
    """
    jar = requests.cookies.RequestsCookieJar()
    _add_driver_cookies(jar, driver)

    for url in extra_urls or []:
        driver.get(url)
        WebDriverWait(driver, 30).until(lambda d: not _on_login_page(d.current_url))
        _add_driver_cookies(jar, driver)

    return jar


def _add_driver_cookies(jar, driver):
    for c in driver.get_cookies():
        domain = c.get("domain", "")
        cookie = http.cookiejar.Cookie(
            version=0,
            name=c["name"],
            value=c["value"],
            port=None,
            port_specified=False,
            domain=domain,
            domain_specified=bool(domain),
            domain_initial_dot=domain.startswith("."),
            path=c.get("path", "/"),
            path_specified=bool(c.get("path")),
            secure=c.get("secure", False),
            expires=c.get("expiry"),
            discard=False,
            comment=None,
            comment_url=None,
            rest={"HttpOnly": ""} if c.get("httpOnly") else {},
        )
        jar.set_cookie(cookie)


def save_cookies(jar, cookie_file):
    """Save a RequestsCookieJar to cookie_file using pickle."""
    os.makedirs(os.path.dirname(os.path.abspath(cookie_file)), exist_ok=True)
    with open(cookie_file, "wb") as f:
        pickle.dump(jar, f)


def main():
    """
    Perform a KTH MFA login and save cookies to a file.

    Usage: python -m weblogin.mfa <trigger_url> <cookie_file>
    """
    if len(sys.argv) < 3:
        print(
            "Usage: python -m weblogin.mfa <trigger_url> <cookie_file>", file=sys.stderr
        )
        sys.exit(1)

    trigger_url = sys.argv[1]
    cookie_file = sys.argv[2]

    username = input("KTH username: ")
    password = getpass.getpass("KTH password: ")

    driver = setup_browser()
    try:
        do_login(driver, username, password, trigger_url)
        jar = collect_cookies(driver)
        save_cookies(jar, cookie_file)
        print("Cookies saved to {}".format(cookie_file))
    except Exception as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        sys.exit(1)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
