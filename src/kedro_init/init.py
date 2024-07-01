import typing as t
from pathlib import Path

from .build_config import get_or_create_build_config, init_build_config
from .config_dirs import get_or_create_config_dirs, init_config_dir
from .modules import get_or_create_modules, init_module


def init_steps(project_root: Path) -> t.Generator[str, None, None]:
    yield "Looking for existing package directories"

    existing, build_config = get_or_create_build_config(project_root)
    if not existing:
        init_build_config(project_root, build_config=build_config)

    yield "Initialising config directories"

    config_dirs = get_or_create_config_dirs(project_root)
    for existing, target_config_dir in config_dirs.values():
        if not existing:
            init_config_dir(project_root, target_config_dir=target_config_dir)

    yield "Creating modules"

    modules = get_or_create_modules(project_root, build_config=build_config)
    for existing, target_module_path, module_contents_path in modules.values():
        if not existing:
            init_module(
                project_root,
                target_module_path=target_module_path,
                module_contents_path=module_contents_path,
            )


def init(project_root: Path) -> None:
    for _ in init_steps(project_root):
        pass
