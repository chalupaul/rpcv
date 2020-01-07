
RPC-V API
=========

An api to do rpc-v things.

Installing
----------

1. Install [poetry](https://pypi.org/project/poetry/)
2. Checkout the code in this repo.
3. Once in your repo directory, use poetry to install everything else:
	`poetry install`
4. Start a shell with your poetry virtualenv setup:
    `poetry shell`
5. Start an editor of your choice:
	`atom .` or `code .`
	
VSCODE Hints
-----------

I'm assuming you're using the [New Windows Terminal](https://github.com/microsoft/terminal).

I don't have many vscode plugins, just Python and IntelliCode. When you start up vscode, make sure you change your python interpreter to the poetry venv. Once you do it the first time, it's written to your settings file so you're good for subsequent runs.

All services in the monorepo can be added to your pythonpath so vscode can find class definitions. Create a `.env` file in the project root with the following paths:

`PYTHONPATH="<PATH_TO_REPO>rpcv\api;<PATH_TO_REPO>\rpcv\api_authorizer"`

And here are some helpful settings for `.vscode/settings.json`:

```
{
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--max-line-length=88"
    ],
    "python.linting.enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestArgs": [
        "rpcv"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestEnabled": true,
}
```


Running the API Locally
--------------------

Not sure how practical this given stepfunctions, but for now you can run flask:

`cd rpcv/api && poetry run rpcvapi`

When I get unlazy, I'll take a look at `sam local` (no promises)

Running Tests
-------------

Unit tests can be run via poetry as well:
`poetry run pytest ./rpcv/tests/`

If you want to save some heartage before pushing code, 
you can lint everything:
`poetry run doit -n 4 -f ./util/gate_tests.py`
