import pathlib

from .build_config import get_or_create_build_config, init_build_config


def init(project_root: pathlib.Path):
    existing, build_config = get_or_create_build_config(project_root)
    if not existing:
        init_build_config(project_root, build_config=build_config)
