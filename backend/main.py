import sys
import uvicorn
from utils.logger import Logger
from utils.types import Severity
from utils.package.cloakquart.Quart import app
from pyucc import colors

Logger(defined_level="Info", **{"show_timestamp_by_default": True})
Logger.__log__("Server Starting...", severity=Severity.Info)

app.register_blueprints()
app.determine_environment()

if not __name__ == "__main__":
  Logger.__log__(f"__name__ must be __main__, instead is \"{__name__}\". Consider the command {colors.vibrant_blue}`siblink run ./backend`", Severity.Fatal)
  quit()


uvicorn.run(app, **app.uvicorn_config)