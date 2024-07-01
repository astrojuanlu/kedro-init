import pytest
from kedro_init.modules import TEMPLATES_PATH, get_or_create_modules


@pytest.fixture
def project_setup(tmp_path):
    package_name = "test_package"
    src_dir = tmp_path / "src" / package_name
    src_dir.mkdir(parents=True)
    return tmp_path, package_name


def test_get_or_create_modules_gets_expected_result(project_setup):
    project_root, package_name = project_setup
    build_config = {"package_name": package_name}

    result = get_or_create_modules(project_root, build_config=build_config)

    assert result == {
        "pipeline_registry.py": (
            False,
            project_root / f"src/{package_name}/pipeline_registry.py",
            TEMPLATES_PATH / "pipeline_registry.py",
        ),
        "settings.py": (
            False,
            project_root / f"src/{package_name}/settings.py",
            TEMPLATES_PATH / "settings.py",
        ),
    }
