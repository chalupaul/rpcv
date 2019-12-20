
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

Running Tests
-------------

Unit tests can be run via poetry as well:
`poetry run pytest test/`

Before pushing code, you should run the whole test suite (this is what is run in CI):
`poetry run tox`