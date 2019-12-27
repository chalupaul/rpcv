import os
import awsgi
from pathlib import Path
from flask import Flask
from flask_dotenv import DotEnv
from flask_rebar import Rebar

from typing import Any, Dict

rebar = Rebar()
registry = rebar.create_handler_registry(prefix="/api")


def create_app() -> Flask:

    app = Flask(__name__)
    dot_env = DotEnv()
    env_path = Path(os.path.abspath(__file__)).parent.parent.parent
    stage = os.environ.get("stage", "dev")
    env_file = os.path.join(env_path, f".env.{stage}")
    dot_env.init_app(app, env_file=env_file, verbose_mode=True)

    rebar.init_app(app)
    return app


def run_app() -> None:
    create_app().run()


def handler(event: Dict[str, Any], context: Dict[str, Any]) -> Any:
    app = create_app()
    base64_types = {"image/png"}
    return awsgi.response(app, event, context, base64_content_types=base64_types)


if __name__ == "__main__":
    run_app()
