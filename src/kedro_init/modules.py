from __future__ import annotations

from pathlib import Path

TEMPLATES_PATH = Path(__file__).parent / "templates"
MODULE_TEMPLATES = {
    "pipeline_registry.py": TEMPLATES_PATH / "pipeline_registry.py",
    "settings.py": TEMPLATES_PATH / "settings.py",
}


def get_or_create_modules(
    project_root: Path,
    *,
    build_config: dict[str, str],
    module_templates: dict[str, Path] | None = None,
) -> dict[str, tuple[bool, Path, Path]]:
    if module_templates:
        module_templates_l = module_templates
    else:
        module_templates_l = MODULE_TEMPLATES

    package_name = build_config["package_name"]
    package_dir = project_root / package_name
    if not package_dir.is_dir():
        package_dir = next(project_root.glob(f"*/{package_name}"), None)  # type: ignore

    if package_dir is None:
        raise ValueError(
            f"No suitable directory found for package name '{package_name}'"
        )

    modules = {}
    for module_name in module_templates_l:
        target_module = package_dir / module_name
        if target_module.exists():
            modules[module_name] = True, target_module, target_module
        else:
            modules[module_name] = False, target_module, module_templates_l[module_name]

    return modules


def init_module(
    project_root: Path, *, target_module_path: Path, module_contents_path: Path
) -> None:
    with target_module_path.open("w") as fh:
        fh.write(module_contents_path.read_text())
