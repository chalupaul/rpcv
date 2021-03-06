import os
import toml
import subprocess
from typing import Dict, List

app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
home_dir = os.path.expanduser("~")
deps_file_name = "lambda-layer-requirements.txt"
target_deps_file = os.path.join(home_dir, deps_file_name)


def get_toml_requirements() -> List[str]:
    toml_file = os.path.join(app_dir, "pyproject.toml")
    toml_config = toml.load(toml_file)
    toml_deps = toml_config["tool"]["poetry"]["dependencies"].keys()
    deps = [k for k in toml_deps if k != "python"]
    return deps


def get_pip_requirements() -> Dict[str, str]:
    """This assumes it was generated with pip freeze, i.e, all lines are =="""
    output = subprocess.check_output("pip freeze", shell=True, text=True)
    cleaned_packages: Dict[str, str] = {}
    for row in output.split("\n"):
        if "==" not in row:
            continue
        segments = row.split("==")
        cleaned_packages[segments[0]] = segments[1]
    return cleaned_packages


def make_prod_requirements(target_file: str) -> None:
    """
    Word to the wise: Often - and _ are interchangeable.
    Also upper/lower casing must match. Watch your imports to poetry.
    """
    toml_deps = get_toml_requirements()
    pip_deps = get_pip_requirements()
    pip_keys = pip_deps.keys()
    real_deps: List[str] = []
    for d in toml_deps:
        if d in pip_keys:
            line_contents = f"{d}=={pip_deps[d]}"
            real_deps.append(line_contents.strip())
    deps_baked = os.linesep.join(real_deps)
    if len(real_deps) != len(toml_deps):
        print(
            (
                "WARNING!! You have deps defined in pyproject.toml"
                " that arent included. Check -/_ and casing!"
            )
        )
    with open(target_file, "w") as fd:
        fd.write(deps_baked)


def poetry_wrapper() -> None:
    make_prod_requirements(target_deps_file)


def get_last_coverage_run() -> int:
    try:
        output = subprocess.check_output(
            "coverage report", shell=True, text=True, cwd=app_dir
        )
        total_line = output.split("\n")[-2]
        total_fields = [x for x in total_line.split(" ") if x != ""]
        return total_fields[-1][:-1]
    except subprocess.CalledProcessError:
        return 10


def poetry_wrapper_coverage() -> None:
    print(get_last_coverage_run())
