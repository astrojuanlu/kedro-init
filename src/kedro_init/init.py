import pathlib

from .build_config import get_or_create_build_config, init_build_config
from .modules import get_or_create_modules, init_module


def init(project_root: pathlib.Path):
    existing, build_config = get_or_create_build_config(project_root)
    if not existing:
        init_build_config(project_root, build_config=build_config)

    modules = get_or_create_modules(project_root, build_config=build_config)
    for existing, target_module_path, module_contents_path in modules.values():
        if not existing:
            init_module(
                project_root,
                target_module_path=target_module_path,
                module_contents_path=module_contents_path,
            )
