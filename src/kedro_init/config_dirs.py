from pathlib import Path

CONFIG_DIRS = [
    Path("conf") / "base",
    Path("conf") / "local",
]


def get_or_create_config_dirs(project_root: Path, *, expected_config_dirs=None):
    if not expected_config_dirs:
        expected_config_dirs = CONFIG_DIRS

    config_dirs = {}
    for config_dir in expected_config_dirs:
        target_config_dir = project_root / config_dir
        if target_config_dir.is_dir():
            config_dirs[config_dir] = True, target_config_dir
        else:
            config_dirs[config_dir] = False, target_config_dir

    return config_dirs


def init_config_dir(project_root: Path, *, target_config_dir: Path):
    target_config_dir.mkdir(parents=True, exist_ok=True)
