import tempfile
import typing as t
import zipfile
from pathlib import Path

from installer.sources import WheelFile
from installer.utils import parse_metadata_file

try:
    from importlib.metadata import PackageNotFoundError, version
except ModuleNotFoundError:
    from importlib_metadata import PackageNotFoundError, version

import tomlkit
from pygetimportables import _simple_build_wheel, get_top_importables_from_wheel
from validate_pyproject import api, errors, plugins


def _get_importables_and_project_name(project_root, outdir):
    wheel_path = _simple_build_wheel(project_root, outdir)

    with zipfile.ZipFile(wheel_path, "r") as zf:
        wheel_file = WheelFile(zf)
        metadata = parse_metadata_file(wheel_file.read_dist_info("METADATA"))

    package_names = get_top_importables_from_wheel(wheel_path)
    project_name = metadata["Name"]
    return package_names, project_name


def kedro_pyproject(tool_name: str) -> dict:
    return {
        "$id": "https://docs.kedro.org/en/latest/",
        "type": "object",
        "description": "Kedro project metadata",
        "properties": {
            "package_name": {"type": "string"},
            "project_name": {"type": "string", "format": "pep508-identifier"},
            "kedro_init_version": {"type": "string", "format": "pep440"},
            "source_dir": {"type": "string"},
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

    with (project_root / "pyproject.toml").open("r") as fh:
        pyproject_toml = tomlkit.load(fh)

    if not pyproject_toml.get("tool", {}).get("kedro", {}):
        with tempfile.TemporaryDirectory() as outdir:
            package_names, project_name = _get_importables_and_project_name(
                project_root, outdir
            )
        if len(package_names) == 1:
            package_name = package_names.pop()
        else:
            raise ValueError("More than one package found in project root")

        kedro_config = {
            "project_name": project_name,
            "package_name": package_name,
            "kedro_init_version": kedro_version,
        }
        if (project_root / package_name).is_dir():
            kedro_config["source_dir"] = ""
        else:
            package_dir = next(project_root.glob(f"*/{package_name}"), None)
            source_dir = package_dir.parent.name if package_dir is not None else None
            if package_dir is not None and source_dir != "src":
                kedro_config["source_dir"] = source_dir
        return False, kedro_config

    # Kedro build config might be present, return it if valid
    try:
        validator(pyproject_toml)
    except errors.ValidationError as exc:
        raise ValueError("Kedro build configuration is invalid") from exc
    else:
        return True, pyproject_toml["tool"]["kedro"]


def init_build_config(project_root: Path, *, build_config: dict[str, str]):
    with (project_root / "pyproject.toml").open("r") as fh:
        pyproject_toml = tomlkit.load(fh)

    pyproject_toml.setdefault("tool", {})["kedro"] = build_config

    with (project_root / "pyproject.toml").open("w") as fh:
        tomlkit.dump(pyproject_toml, fh)
