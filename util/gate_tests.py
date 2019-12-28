import os
from typing import List, Dict, Any

app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
code_root = os.path.join(app_dir, "rpcv")


def _build_action(actions: List[str] = [], verbosity: int = 2) -> Dict[str, Any]:
    return {"verbosity": verbosity, "actions": actions}


def _find_modules() -> List[str]:
    modules = []
    for folder_name in os.listdir(code_root):
        if not folder_name.startswith("_") and folder_name not in ["tests"]:
            modules.append(os.path.join(code_root, folder_name))
    return modules


code_dirs = " ".join(_find_modules())
test_dir = os.path.join(code_root, "tests")
template_file = os.path.join(app_dir, "template.yaml")


def task_flake8():
    # line length of 88 to match black
    return _build_action(
        [
            (
                "poetry run flake8"
                " --max-line-length=88"
                " --count"
                " --statistics"
                f" {code_dirs} {test_dir}"
            )
        ]
    )


def task_mypy():
    return _build_action(
        [
            (
                "poetry run mypy"
                " --strict "
                " --ignore-missing-imports"
                " --allow-subclassing-any"
                " --allow-untyped-decorators"
                f" {code_dirs}"
            )
        ]
    )


def task_black():
    return _build_action([f"poetry run black {code_dirs} {test_dir}"])


def task_bandit():
    return _build_action([f"poetry run bandit -r {code_dirs}"])


def task_pyproject_lint():
    return _build_action(["poetry check"])


def task_cfn_lint():
    # Currently E3038 is disabled becaues sam auto-inflates the template.
    return _build_action([f"poetry run cfn-lint -i E3038 -t {template_file}"])


def task_sam_lint():
    stagename = os.environ.get("STAGE", "dev")
    region = os.environ.get("REGION", "us-west-2")
    template_file = os.path.join(app_dir, "template.yaml")
    return _build_action(
        [
            (
                "poetry run sam validate"
                f" --profile vdo-rpcv-{stagename}"
                f" --region {region}"
                f" --template {template_file}"
            )
        ]
    )
