from pathlib import Path


def get_project_root() -> Path:
    root_path = Path(__file__).resolve()
    while not (root_path / "pyproject.toml").exists() and root_path.parent != root_path:
        root_path = root_path.parent
    return root_path


def get_plugin_root() -> Path:
    root_path = Path(__file__).resolve()
    while not (root_path / "_manifest.json").exists() and root_path.parent != root_path:
        root_path = root_path.parent
    return root_path


def calculate_module_name_by_path(file_path: Path, root: Path) -> str:
    relative_path = file_path.relative_to(root)
    return ".".join(relative_path.with_suffix("").parts)

def subtract_module_name(full_module: str, sub_module: str) -> str:
    """
    Subtract the sub_module name from the full_module name.
    """
    if full_module.endswith(f".{sub_module}"):
        return full_module.replace(f".{sub_module}", "")
    else:
        raise ValueError(f"{sub_module} is not a suffix of {full_module}")