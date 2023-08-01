[![Version](https://img.shields.io/pypi/v/libre-chat)](https://pypi.org/project/libre-chat) [![Python versions](https://img.shields.io/pypi/pyversions/libre-chat)](https://pypi.org/project/libre-chat) [![Image size](https://ghcr-badge.egpl.dev/vemonet/libre-chat/size)](https://github.com/vemonet/libre-chat/pkgs/container/libre-chat) [![Pull requests welcome](https://img.shields.io/badge/pull%20requests-welcome-brightgreen)](https://github.com/vemonet/libre-chat/fork)

[![Publish package](https://github.com/vemonet/libre-chat/actions/workflows/publish.yml/badge.svg)](https://github.com/vemonet/libre-chat/actions/workflows/publish.yml) [![Test package](https://github.com/vemonet/libre-chat/actions/workflows/test.yml/badge.svg)](https://github.com/vemonet/libre-chat/actions/workflows/test.yml) [![Coverage Status](https://coveralls.io/repos/github/vemonet/libre-chat/badge.svg?branch=main)](https://coveralls.io/github/vemonet/libre-chat?branch=main)

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg){ loading=lazy .off-glb }](https://github.com/pypa/hatch) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json){ loading=lazy .off-glb }](https://github.com/astral-sh/ruff) [![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg){ loading=lazy .off-glb }](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg){ loading=lazy .off-glb }](https://github.com/python/mypy)


## 📥 Install for development

Clone the repository and go to the project folder:

```bash
git clone https://github.com/vemonet/libre-chat
cd libre-chat
```

For development we use [Hatch](https://hatch.pypa.io), it will automatically handle virtual environments, and make sure all dependencies are installed when you run a script in the project. Install it with `pipx` or `pip`:

```bash
pipx install hatch
```

??? info "Optionally you can enable `hatch` terminal completion"

    See the [official documentation](https://hatch.pypa.io/latest/cli/about/#tab-completion) for more details. For ZSH you can run these commands:

    ```bash
    _HATCH_COMPLETE=zsh_source hatch > ~/.hatch-complete.zsh
    echo ". ~/.hatch-complete.zsh" >> ~/.zshrc
    ```


## 🧑‍💻 Development workflow

Start a conversational chat web service, without vectorstore:

```bash
hatch run dev
```

Start a documents-based question answering service, using a vectorstore:

```bash
hatch run vector
```

Use the CLI to build a vectorstore at a specific path:

```bash
hatch run libre-llm build --documents documents2 --vector vectorstore/db2
```

## ✅ Run the tests

Make sure the existing tests still work by running the test suite, mypy, and linting checks. .

Run the tests locally:

```bash
hatch run test
```

Run only a specific test, and display all logs:

```bash
hatch run test tests/test_api.py::test_post_prompt_conversation -s
```

??? example "Run the tests on the different versions of python available on your machine"

    Not required as it is done by the GitHub Actions workflow, but can be useful for debugging:

    ```bash
    hatch run all:test
    ```

## 📖 Generate the docs

The documentation (this website) is automatically generated and published by a GitHub Actions workflow from the markdown files in the `docs/` folder, and python `docstring` comments.

To check the documentation website locally, serve it with:

```bash
hatch run docs
```

## ♻️ Reset the environment

In case you are facing issues with dependencies not updating properly you can easily reset the virtual environment with:

```bash
hatch env prune
```

Manually trigger the installation of dependencies in a local virtual environment (done automatically when you run any script):

```bash
hatch -v env create
```

Enter a new shell with the environment activated:

```bash
hatch shell
```

## 🏷️ Publish a new release

The deployment of new releases is done automatically by a GitHub Actions workflow when a new release is created on GitHub. To release a new version:

1. Make sure the `PYPI_TOKEN` secret has been defined in the GitHub repository (in Settings > Secrets > Actions). You can get an API token from PyPI at [pypi.org/manage/account](https://pypi.org/manage/account).

2. Increment the `version` number in the `src/libre_chat/__init__.py` file:

    ```bash
    hatch version 0.1.0
    # Or bump using semver: patch, minor, major
    hatch version patch
    ```

3. Commit, push, and create a new release on GitHub, which will automatically trigger a workflow to publish the new release to PyPI.

??? bug "Or perform the release locally"

    1. Update the version:

        ```bash
        hatch version 0.1.0
        # Or bump using semver: patch, minor, major
        hatch version patch
        ```

    2. Build and publish:

        ```bash
        hatch build
        hatch publish
        ```

    3. Create the release on GitHub, [manually](https://github.com/vemonet/libre-chat/releases/new) or with the [`gh` CLI](https://cli.github.com/):

        ```bash
        gh release create
        ```

<!-- Admonition blocks: https://squidfunk.github.io/mkdocs-material/reference/admonitions/#supported-types -->
