from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = ROOT / "pyproject.toml"
UV_LOCK = ROOT / "uv.lock"


def load_pyproject() -> dict:
    assert PYPROJECT.exists(), "pyproject.toml must exist"
    return tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))


def test_project_metadata_and_dependencies() -> None:
    pyproject = load_pyproject()
    project = pyproject["project"]

    assert project["name"] == "agent-on-claude-sdk"
    assert project["requires-python"] == ">=3.12"

    dependencies = project["dependencies"]
    assert any(dep.startswith("anthropic") for dep in dependencies)
    assert any(dep.startswith("tavily-python") for dep in dependencies)
    assert any(dep.startswith("python-dotenv") for dep in dependencies)

    dev_dependencies = project["optional-dependencies"]["dev"]
    assert any(dep.startswith("pytest") for dep in dev_dependencies)
    assert any(dep.startswith("ruff") for dep in dev_dependencies)

    assert UV_LOCK.exists(), "uv.lock must exist"
