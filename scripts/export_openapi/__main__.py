import json
import importlib
from pathlib import Path

import typer


app = typer.Typer()


@app.command()
def export_openapi(
    fastapi_app_module: str,
    json_output_path: Path = Path("openapi.json"),
) -> None:
    """
    Write the application's OpenAPI schema to disk.
    """

    app = importlib.import_module(fastapi_app_module).app
    openapi = app.openapi()
    with open(json_output_path, "w") as file:
        json.dump(openapi, file, indent=2)


def main():
    app()


if __name__ == "__main__":
    app()
