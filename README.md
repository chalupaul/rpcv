
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