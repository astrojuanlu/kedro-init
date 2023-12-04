import typing as t
from pathlib import Path

try:
    from importlib.metadata import PackageNotFoundError, version
except ModuleNotFoundError:
    from importlib_metadata import PackageNotFoundError, version

import tomli
import tomli_w
from pygetimportables import get_top_importables
from validate_pyproject import api, errors, plugins


def kedro_pyproject(tool_name: str) -> dict:
    return {
        "$id": "https://docs.kedro.org/en/latest/",
        "type": "object",
        "description": "Kedro project metadata",
        "properties": {
            "package_name": {"type": "string"},
            "project_name": {"type": "string", "format": "pep508-identifier"},
            "kedro_init_version": {"type": "string", "format": "pep440"},
        },
        "required": ["package_name", "project_name", "kedro_init_version"],
        "additionalProperties": False,
    }


def get_or_create_build_config(project_root: Path) -> tuple[bool, t.Any]:
    try:
        kedro_version = version("kedro")
    except PackageNotFoundError as exc:
        raise ValueError("Kedro is not installed") from exc

    available_plugins = [
        *plugins.list_from_entry_points(),
        plugins.PluginWrapper("kedro", kedro_pyproject),
    ]
    validator = api.Validator(available_plugins)

    with (project_root / "pyproject.toml").open("rb") as fh:
        pyproject_toml = tomli.load(fh)

    if not pyproject_toml.get("tool", {}).get("kedro", {}):
        # Kedro build config not present, generate it
        package_names = get_top_importables(project_root)
        if len(package_names) == 1:
            package_name = package_names.pop()
        else:
            raise ValueError("More than one package found in project root")

        project_name = pyproject_toml["project"]["name"]
        return False, {
            "project_name": project_name,
            "package_name": package_name,
            "kedro_init_version": kedro_version,
        }

    # Kedro build config might be present, return it if valid
    try:
        validator(pyproject_toml)
    except errors.ValidationError as exc:
        raise ValueError("Kedro build configuration is invalid") from exc
    else:
        return True, pyproject_toml["tool"]["kedro"]


def init_build_config(project_root: Path, *, build_config: dict[str, str]):
    with (project_root / "pyproject.toml").open("rb") as fh:
        pyproject_toml = tomli.load(fh)

    pyproject_toml.setdefault("tool", {})["kedro"] = build_config

    with (project_root / "pyproject.toml").open("wb") as fh:
        tomli_w.dump(pyproject_toml, fh)
