import click
from pyucc import console, colors
import pathlib

color_grey = colors.chex("#AAAAAA", "foreground")


@click.command()
@click.option(
    "-r", "--reference", "ref", required=False, default="./ff_nginx.conf", help=""
)
@click.option(
    "-o", "--output", "out", required=False, default="C:/nginx/conf/nginx.conf", help=""
)
def dump(ref: str, out: str):
    """
    dumps a windows-safe nginx configuration to a specified path

    Arguments:\n
    \t[ref] Reference file, which will be converted into a windows-safe object
    \t[out] Where the file will be dumped
    """

    reference_file: pathlib.Path = pathlib.Path(ref)
    payload = reference_file.read_text().rstrip()

    # SSL START =============================
    # Change ssl_certificate
    payload = payload.replace(
        "ssl_certificate /etc/ssl/com/.cert",
        "ssl_certificate C:/nginx/ssl/com-dev-trelta/.cert",
    )

    # Change ssl_certificate_key
    payload = payload.replace(
        "ssl_certificate_key /etc/ssl/com/.key",
        "ssl_certificate_key C:/nginx/ssl/com-dev-trelta/.key",
    )
    # SSL END ===============================

    # PROXY_PASS START ======================
    payload = payload.replace(
        "proxy_pass https://backend", "proxy_pass https://localhost:4000"
    )
    payload = payload.replace(
        "proxy_pass http://frontend", "proxy_pass http://localhost:3000"
    )
    # PROXY_PASS END ========================

    # UPSTREAM START ========================
    payload = payload.replace(
        """upstream backend {
        server backend:4000;
    }""",
        "",
    )
    payload = payload.replace(
        """upstream frontend {
        server frontend:3000;
    }""",
        "",
    )
    # UPSTREAM END ==========================

    # Dump to output file
    pathlib.Path(out).write_text(payload)

    console.done(
        f"{color_grey}Dumped windows-safe nginx configuration to {colors.vibrant_blue}{out}"
    )
