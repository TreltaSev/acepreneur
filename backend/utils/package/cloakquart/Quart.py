import asyncio
import quart
import siblink
from siblink import Config

import importlib.util
import importlib.machinery

from pathlib import Path

import os
from utils.logger import Logger
from utils.types import Severity
from utils.exception import HighLevelException
from utils.package.cloakquart.Blueprint import Blueprint

from typing import Callable

from pyucc import colors

import traceback


class Quart(quart.Quart):
    """
    Inherited `quart.Quart` class, allows for easier access of customized loading, managing, and resolving of methods.
    can handle websocket/http or https requests through the quart.Quart framework. This class can be used as a regular quart object.
    """

    def __init__(
        self,
        import_name: str,
        static_url_path: str | None = None,
        static_folder: str | None = "static",
        static_host: str | None = None,
        host_matching: bool = False,
        subdomain_matching: bool = False,
        template_folder: str | None = "templates",
        instance_path: str | None = None,
        instance_relative_config: bool = False,
        root_path: str | None = None,
    ) -> None:
        self.blueprints: dict[str, quart.Quart] = {}

        super().__init__(
            import_name,
            static_url_path,
            static_folder,
            static_host,
            host_matching,
            subdomain_matching,
            template_folder,
            instance_path,
            instance_relative_config,
            root_path,
        )

    def load(self, spec: importlib.machinery.ModuleSpec | str) -> None:
        """
        Attempts to obtain a blueprint variable from the inputted `spec` object.
        uses importlib's `importlib.util.module_from_spec` method, throws errors if a blueprint variable is not available within the file.

        :arg spec: importlib.machinery.ModuleSpec: string format of library path separated by "."
        """

        if isinstance(spec, str):
            spec: importlib.machinery.ModuleSpec | None = importlib.util.find_spec(
                self.resolve_name(spec, package=None)
            )

        if spec is None:
            # ;; Logger.__log__(f"spec value is None")
            return None

        library = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(library)
        except Exception as error:
            raise error

        if not hasattr(library, "blueprint"):
            raise HighLevelException(
                f"No Blueprint Variable found in {library}", severity=Severity.Fatal
            )

        external_blueprint = getattr(library, "blueprint")

        self.__cache_blueprint__(blueprint=external_blueprint)

    def __cache_blueprint__(self, blueprint: quart.Blueprint) -> None:
        """
        Caches a blueprint into cls.blueprints and registers it while also checking if the blueprint has already been cached.
        :arg blueprint: :class:`quart.Blueprint`: Blueprint object which inherits or is a `quart.blueprint` object ex: :class:`cloakquart.Blueprint`
        """
        if blueprint.name in self.blueprints:
            raise HighLevelException(f"CloakQUart already contains `{blueprint}`")
        self.register_blueprint(blueprint)
        self.blueprints[blueprint.name] = blueprint
        Logger.__log__(
            f"Cached and registered blueprint: {blueprint.name}", severity=Severity.Info
        )

    @classmethod
    def resolve_name(cls, name: str, package: str | None = None) -> str | None:
        """
        Uses the builtin `importlib` module's `util.resolve_name` method, just a more concise way of using it, if the return value
        of importlib.util.resolve_name results in an error, this method returns `None`
        :arg name: str: Relative Path of package, uses "." as separator
        :arg package: Optional[str]: Module with `__path__` attribute
        :returns: Union[str, None]: Returns either an absolute module name or None: import error
        """
        try:
            return importlib.util.resolve_name(name, package)
        except ImportError as e:
            Logger.__log__(
                f"Import Error (name:str): {name} && (package: str | None): {package}, Error: ({e})",
                Severity.Fatal,
            )
            return None

    def register_blueprints(self) -> None:
        """
        Set of methods run in tangent to find, resolve, and register quart blueprints
        """
        for bp in Blueprint.__get_blueprints__():
            self.load(bp)

    @staticmethod
    def determine_environment() -> None:
        Config.BASE_URL = os.getenv("BASE_URL") or "https://localhost"

    @property
    @siblink.Config.load_config
    def uvicorn_config(self) -> None:
        """
        Gets required configuration options for uvicorn from siblink.config.json
        """
        # Initiate out
        outConfig = {}

        # Handle Host, Port, and log level
        outConfig.update(
            {
                "host": Config.backend.host,
                "port": Config.backend.port,
                "log_level": "info",
            }
        )

        # Handle SSL
        ssl = Config.backend.ssl
        if ssl.active:
            parent: str = str(Path(getattr(ssl, "$parent")).absolute())
            cert: str = str(Path(ssl.cert.replace("$", parent)).absolute())
            key: str = str(Path(ssl.key.replace("$", parent)).absolute())

            outConfig.update({"ssl_certfile": cert, "ssl_keyfile": key})

        return outConfig

    def register_task(
        self, name, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0
    ):
        """
        Registers a background task to be ran.

        ### Usage
        ```
        @app.register_task("income_stream_runner", days=1, hours=16, seconds=32)
        def some_task(*args, **kwargs):
            print("im a task")
        ```
        """

        interval: int = 0

        interval += seconds
        interval += minutes * 60
        interval += hours * 60**2
        interval += days * 24 * 60**2

        def decorator(f: Callable) -> Callable:
            """
            Add task
            """

            async def _wrapper() -> None:

                async def modified():
                    while True:
                        try:
                            await f()
                            Logger.__log__(
                                f"Ran Task {colors.vibrant_blue}{name}",
                                severity=Severity.Info,
                            )
                        except Exception as e:
                            Logger.__log__(
                                f'Task {colors.vibrant_blue}{name}{colors.vibrant_red} FAILED {colors.vibrant_orange}"{e}"',
                                severity=Severity.Warning,
                            )
                            traceback.print_exc()
                        await asyncio.sleep(interval)

                Logger.__log__(
                    f"Registered Task {colors.vibrant_blue}{name}",
                    severity=Severity.Info,
                )

                asyncio.get_running_loop().create_task(modified())

            self.before_serving(_wrapper)

        return decorator


app = Quart(__name__)
