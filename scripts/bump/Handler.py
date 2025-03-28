from bump import logic
from typing import Callable, List
from pyucc import colors, symbols, console
import sys
import json
import pathlib
import toml


class Handler:
    secs: dict = {}

    @classmethod
    def register(cls, name):
        """
        Registers a package type name to update for advanced functionality
        """

        def decorator(f: Callable, **options):
            cls.secs[name] = f
            # console.info(f"Stored \"{name}\" to: {f}")
            return f
        return decorator

    @classmethod
    def get(cls, name) -> None | Callable:
        """
        Returns a function relating to name
        """
        return cls.secs.get(name, None)

    @classmethod
    def gather(cls) -> List[str]:
        return cls.secs.keys()

    @classmethod
    def analyze(cls, *r_args, **r_kwargs):
        """
        Analyzes user input, checks for any mistakes
        """
        def decorator(f: Callable):
            """
            Ran @ Register
            """
            def inner(*args, **kwargs):
                """
                Ran with function
                """

                _level: str = kwargs["level"]

                _level = _level.lower()  # Lower

                # Get File if needed
                if (r_kwargs["file"]):
                    _file = logic.find(
                        file=r_kwargs["file"], dir=r_kwargs["dir"])
                    if not _file:
                        raise FileNotFoundError(
                            f"\"{r_kwargs['file']}\" not found")
                    kwargs["file"] = _file

                # Check level is valid
                if _level not in ["major", "minor", "patch"]:
                    try:
                        major, minor, patch = _level.strip("v").split(".")
                        int(major)
                        int(minor)
                        int(patch)
                    except:
                        console.fail(
                            f"Level \"{_level}\" must be either {colors.chex('#030303', 'foreground')}major, minor, patch, or a format-able string such as {colors.vibrant_yellow}v5.1.2{symbols.reset}")
                        console.fail(
                            f"Try {colors.chex('#030303', 'foreground')}siblink run -- scripts/bump {sys.argv[1]} {colors.vibrant_violet}major{symbols.reset} instead")
                        quit()

                kwargs["level"] = _level
                f(**kwargs)

            return inner
        return decorator


def bump_toml(sections: List[str] | str, **r_kwargs):
    if isinstance(sections, str):
        sections = [sections]

    def decorator(f: Callable):
        def inner(**kwargs):
            for section in sections:
                file: pathlib.Path = kwargs["file"]
                print(file)
                tm = toml.loads(file.read_text())
                old = tm[section]["version"]
                new = logic.update(old, kwargs["level"])
                tm[section]["version"] = new
                file.write_text(toml.dumps(tm))
                console.done(
                    f"Bumped {section}, {colors.vibrant_violet}{tm[section]['name']} {colors.vibrant_blue}v{old} {symbols.reset}=> {colors.vibrant_green}v{new}{symbols.reset}")

            f(**kwargs)
        return inner
    return decorator


@Handler.register("sync")
@Handler.analyze(file="project.toml", dir=[None])
@bump_toml("sync")
def sync(*args, **kwargs):
    pass


@Handler.register("backend")
@Handler.analyze(file="project.toml", dir=[None])
@bump_toml("backend")
def backend(*args, **kwargs):
    pass


@Handler.register("frontend")
@Handler.analyze(file="project.toml", dir=[None])
@bump_toml("frontend")
@Handler.analyze(file="package.json", dir="frontend")
def frontend(*args, **kwargs):
    file: pathlib.Path = kwargs["file"]
    js = json.loads(file.read_text())
    old = js['version']
    new = logic.update(old, kwargs["level"])
    js['version'] = new
    file.write_text(json.dumps(js, indent=2))
