from functools import partial, wraps
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from monzo.authentication import Authentication
from monzo.handlers.filesystem import FileSystem
from monzo.exceptions import MonzoAuthenticationError, MonzoPermissionsError
import time

from monzo.endpoints.account import Account
from monzo.endpoints.pot import Pot


class MonzoAuthHTTPServer(BaseHTTPRequestHandler):
    def __init__(self, auth: Authentication, *args) -> None:
        self.auth = auth
        super().__init__(*args)

    def do_GET(self):
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        if not ("code" in params and "state" in params):
            raise ValueError("url missing state and code params")
        code = params["code"][0]
        state = params["state"][0]
        self.auth.authenticate(code, state)
        self.send_response(200, "auth succ")
        self.end_headers()

class AuthedApi:
    def __init__(self, auth: Authentication) -> None:
        self.auth = auth


    @classmethod
    def from_file(cls, path: str, client_id: str, client_secret: str, redirect_url: str) -> "AuthedApi":
        handler = FileSystem(".creds")
        creds = handler.fetch()

        auth = Authentication(
            client_id=client_id,
            client_secret=client_secret,
            redirect_url=redirect_url,
            access_token=creds.get("access_token", ""), # type: ignore
            access_token_expiry=creds.get("expiry", 0), # type: ignore
            refresh_token=creds.get("refresh_token", ""), # type: ignore
        )
        auth.register_callback_handler(handler)

        return cls(auth)

    def aquire_new_token(self):
        print(f"\n\nplease visit this url to auth: {self.auth.authentication_url}")

        server_address = ("", 8000)
        httpd = HTTPServer(server_address, partial(MonzoAuthHTTPServer, self.auth))
        httpd.handle_request()

    @staticmethod
    def auth_handler(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            while 1:
                try:
                    return func(self, *args, **kwargs)
                    break
                except MonzoAuthenticationError:
                    try:
                        self.auth.refresh_access()
                    except MonzoAuthenticationError:
                        self.aquire_new_token()

                except MonzoPermissionsError:
                    print("allow this script to access in monzo")
                    time.sleep(30)
        return wrapper

    @auth_handler
    def fetch_accounts(self) -> list[Account]:
        return Account.fetch(self.auth)

    @auth_handler
    def fetch_pots(self,account: Account):
        return Pot.fetch(self.auth, account.account_id)

