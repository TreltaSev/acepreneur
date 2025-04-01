import sys
import uvicorn
from siblink import Config
import pathlib
from utils.logger import Logger
from utils.types import Severity
from utils.package.cloakquart.Quart import app
from pyucc import colors
from quart_cors import cors

Logger(defined_level="Info", **{"show_timestamp_by_default": True})
Logger.__log__("Server Starting...", severity=Severity.Info)

app.register_blueprints()
app.determine_environment()

app = cors(app, allow_origin="*")

# Validate Config
try:

    if not Config.backend.ssl.active:
        Logger.__log__("Unsecure Hosting: HTTP (ssl inactive)",
                       severity=Severity.Warning)
    else:
        Logger.__log__("Secure Hosting: HTTPS (ssl active)",
                       severity=Severity.Info)

    if Config.backend.ssl.active:
        cert_file = Config.backend.ssl["cert"].replace(
            "$", Config.backend.ssl["$parent"])
        key_file = Config.backend.ssl["key"].replace(
            "$", Config.backend.ssl["$parent"])

        if not pathlib.Path(cert_file).exists():
            Logger.__log__(
                f'Missing Certification File, have: {cert_file} as path', severity=Severity.Fatal)
            raise AttributeError('Certificate File')

        if not pathlib.Path(key_file).exists():
            Logger.__log__(
                f'Missing Key File, have: {key_file} as path', severity=Severity.Fatal)
            raise AttributeError('Key File')

    if Config.admin.active:
        if Config.admin.secret == "YOUR SECRET HERE":
            Logger.__log__(
                f"Admin Secret Unchanged, Maybe change it to something that isn't \"{Config.admin.secret}\"?", Severity.Warning)


except AttributeError as e:
    print("You seem to be missing some keys in your config.\n", e)
    quit()


if not __name__ == "__main__":
    Logger.__log__(
        f"__name__ must be __main__, instead is \"{__name__}\". Consider the command {colors.vibrant_blue}`siblink run ./backend`", Severity.Fatal)
    quit()


uvicorn.run(app, **app.uvicorn_config)
