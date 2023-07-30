[![Version](https://img.shields.io/pypi/v/libre-chat)](https://pypi.org/project/libre-chat) [![Python versions](https://img.shields.io/pypi/pyversions/libre-chat)](https://pypi.org/project/libre-chat) [![Pull requests welcome](https://img.shields.io/badge/pull%20requests-welcome-brightgreen)](https://github.com/vemonet/libre-chat/fork)

[![Publish package](https://github.com/vemonet/libre-chat/actions/workflows/publish.yml/badge.svg)](https://github.com/vemonet/libre-chat/actions/workflows/publish.yml){:target="_blank"} [![Test package](https://github.com/vemonet/libre-chat/actions/workflows/test.yml/badge.svg)](https://github.com/vemonet/libre-chat/actions/workflows/test.yml){:target="_blank"} [![Coverage Status](https://coveralls.io/repos/github/vemonet/libre-chat/badge.svg?branch=main)](https://coveralls.io/github/vemonet/libre-chat?branch=main){:target="_blank"}

## 📥 Install for development

Clone the repository and go in the project folder:

```bash
git clone https://github.com/vemonet/libre-chat
cd libre-chat
```

To install the project for development you can either use [`venv`](https://docs.python.org/3/library/venv.html) to create a virtual environment yourself, or use [`hatch`](https://hatch.pypa.io) to automatically handle virtual environments for you.

=== "hatch"

    Install [Hatch](https://hatch.pypa.io), this will automatically handle virtual environments and make sure all dependencies are installed when you run a script in the project:

    ```bash
    pipx install hatch
    ```

    ??? note "Optionally you can improve `hatch` terminal completion"

        See the [official documentation](https://hatch.pypa.io/latest/cli/about/#tab-completion) for more details. For ZSH you can run these commands:

        ```bash
        _HATCH_COMPLETE=zsh_source hatch > ~/.hatch-complete.zsh
        echo ". ~/.hatch-complete.zsh" >> ~/.zshrc
        ```

=== "venv"

    Create the virtual environment in the project folder :

    ```bash
    python3 -m venv .venv
    ```

    Activate the virtual environment:

    ```bash
    source .venv/bin/activate
    ```

    Install all dependencies required for development:

    ```bash
    pip install -e ".[dev,doc,test]"
    ```

    Install `pre-commit` to enable automated formatting and linting of the code at each commit:

    ```bash
    pre-commit install
    ```


## 🧑‍💻 Development workflow

=== "hatch"

    Try to sign a nanopublication with the code defined in `scripts/dev.py` to test your changes:

    ```bash
    hatch run dev
    ```

    The code will be automatically formatted when you commit your changes using `pre-commit`. But you can also run the script to format the code yourself:

    ```bash
    hatch run fmt
    ```

=== "venv"

    Try to sign a nanopublication with the code defined in `scripts/dev.py` to test your changes:

    ```bash
    ./scripts/dev.sh
    ```

    The code will be automatically formatted when you commit your changes using `pre-commit`. But you can also run the script to format the code yourself:

    ```bash
    ./scripts/format.sh
    ```

    Check the code for errors, and if it is in accordance with the PEP8 style guide, by running `flake8` and `mypy`:

    ```bash
    ./scripts/lint.sh
    ```

## ✅ Run the tests

[![Test package](https://github.com/vemonet/libre-chat/actions/workflows/test.yml/badge.svg)](https://github.com/vemonet/libre-chat/actions/workflows/test.yml){:target="_blank"} [![Coverage Status](https://coveralls.io/repos/github/vemonet/libre-chat/badge.svg?branch=main)](https://coveralls.io/github/vemonet/libre-chat?branch=main){:target="_blank"}

Make sure the existing tests still work by running the test suite and linting checks. Note that any pull requests to the repository on github will automatically trigger running of the test suite.


###

=== "hatch"

	Run the tests locally:

	```bash
	hatch run test
	```

	To display all logs when debugging:

	```bash
	hatch run test -s
	```

	Run the tests on multiple python versions:

	```bash
	hatch run all:test
	```

	Run only a specific test:

	```bash
	hatch run test tests/test_api.py::test_post_prompt_conversational
	```

=== "venv"

	Run the tests locally:

	```bash
	./scripts/test.sh
	```

	You can also run only a specific test:

	```bash
	./scripts/test.sh tests/test_api.py::test_post_prompt_conversational
	```


## 📖 Generate docs

The documentation (this website) is automatically generated from the markdown files in the `docs` folder and python docstring comments, and published by a GitHub Actions workflow.

Serve the docs on [http://localhost:8001](http://localhost:8001){:target="_blank"}

=== "hatch"

    ```bash
    hatch run docs
    ```

=== "venv"

    ```bash
    ./scripts/docs.sh
    ```

### ♻️ Reset the environment

In case you are facing issues with dependencies not updating properly you can easily reset the virtual environment with:

```bash
hatch env prune
```

Manually trigger installing the dependencies in a local virtual environment:

```bash
hatch -v env create
```

## 🏷️ Publish a new release

[![Publish package](https://github.com/vemonet/libre-chat/actions/workflows/publish.yml/badge.svg)](https://github.com/vemonet/libre-chat/actions/workflows/publish.yml){:target="_blank"}

1. Make sure the `PYPI_TOKEN` secret has been defined in the GitHub repository (in Settings > Secrets > Actions). You can get an API token from PyPI at [pypi.org/manage/account](https://pypi.org/manage/account).
2. Increment the `__version__` in `libre_chat/__init__.py`
3. Push to GitHub
4. Create a new release on GitHub
5. A GitHub Action workflow will automatically publish the new version to PyPI
