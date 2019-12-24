import os

app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

code_dir = os.path.join(app_dir, "rpcv")
test_dir = os.path.join(app_dir, "tests")


def task_flake8():
    return {"actions": [f"poetry run flake8 {code_dir} {test_dir}"]}


def task_mypy():
    return {
        "actions": [
            f"poetry run mypy --strict --ignore-missing-imports --allow-subclassing-any {code_dir}"
        ]
    }


def task_black():
    return {"actions": [f"poetry run black {code_dir} {test_dir}"]}


def task_bandit():
    return {"actions": [f"poetry run bandit -r {code_dir}"]}
