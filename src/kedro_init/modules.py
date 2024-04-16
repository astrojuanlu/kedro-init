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
    module_templates: dict[str, str] = None,
):
    if not module_templates:
        module_templates = MODULE_TEMPLATES

    package_name = build_config["package_name"]
    package_dir = next(project_root.glob(f"*/{package_name}"), None)
    if package_dir is None:
        package_dir = next(project_root.glob(f"{package_name}"), None)

    modules = {}
    for module_name in module_templates:
        target_module = package_dir / module_name
        if target_module.exists():
            modules[module_name] = True, target_module, target_module
        else:
            modules[module_name] = False, target_module, module_templates[module_name]

    return modules


def init_module(
    project_root: Path, *, target_module_path: Path, module_contents_path: Path
):
    with target_module_path.open("w") as fh:
        fh.write(module_contents_path.read_text())
