import os

app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

code_dir = os.path.join(app_dir, "rpcv")
test_dir = os.path.join(app_dir, "tests")


def task_flake8():
    # line length of 88 to match black
    return {
        "actions": [
            (
                "poetry run flake8"
                " --max-line-length=88"
                " --count"
                " --statistics"
                f" {code_dir} {test_dir}"
            )
        ]
    }


def task_mypy():
    return {
        "actions": [
            (
                "poetry run mypy"
                " --strict "
                " --ignore-missing-imports"
                " --allow-subclassing-any"
                f" {code_dir}"
            )
        ]
    }


def task_black():
    return {"actions": [f"poetry run black {code_dir} {test_dir}"]}


def task_bandit():
    return {"actions": [f"poetry run bandit -r {code_dir}"]}
