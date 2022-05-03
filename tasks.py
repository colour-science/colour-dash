"""
Invoke - Tasks
==============
"""

from invoke import Context, task
from invoke.exceptions import Failure

from colour.hints import Boolean

from colour.utilities import message_box

import app

__author__ = "Colour Developers"
__copyright__ = "Copyright 2018 Colour Developers"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "APPLICATION_NAME",
    "ORG",
    "CONTAINER",
    "clean",
    "quality",
    "precommit",
    "requirements",
    "docker_build",
    "docker_remove",
    "docker_run",
]

APPLICATION_NAME: str = app.__application_name__

ORG: str = "colourscience"

CONTAINER: str = APPLICATION_NAME.replace(" ", "").lower()


def _patch_invoke_annotations_support():
    """See https://github.com/pyinvoke/invoke/issues/357."""

    import invoke
    from unittest.mock import patch
    from inspect import getfullargspec, ArgSpec

    def patched_inspect_getargspec(function):
        spec = getfullargspec(function)
        return ArgSpec(*spec[0:4])

    org_task_argspec = invoke.tasks.Task.argspec

    def patched_task_argspec(*args, **kwargs):
        with patch(
            target="inspect.getargspec", new=patched_inspect_getargspec
        ):
            return org_task_argspec(*args, **kwargs)

    invoke.tasks.Task.argspec = patched_task_argspec


_patch_invoke_annotations_support()


@task
def clean(ctx, bytecode=False):
    """
    Clean the project.

    Parameters
    ----------
    bytecode : bool, optional
        Whether to clean the bytecode files, e.g. *.pyc* files.
    """

    message_box("Cleaning project...")

    patterns = []

    if bytecode:
        patterns.append("**/__pycache__")
        patterns.append("**/*.pyc")

    for pattern in patterns:
        ctx.run(f"rm -rf {pattern}")


@task
def quality(
    ctx: Context,
    mypy: Boolean = True,
):
    """
    Check the codebase with *Mypy* and lints various *restructuredText* files
    with *rst-lint*.

    Parameters
    ----------
    ctx
        Context.
    mypy
        Whether to check the codebase with *Mypy*.
    """

    if mypy:
        message_box('Checking codebase with "Mypy"...')
        ctx.run(
            "mypy "
            "--install-types "
            "--non-interactive "
            "--show-error-codes "
            "--warn-unused-ignores "
            "--warn-redundant-casts "
            "app.py index.py apps"
            "|| true"
        )


@task
def precommit(ctx: Context):
    """
    Run the "pre-commit" hooks on the codebase.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box('Running "pre-commit" hooks on the codebase...')
    ctx.run("pre-commit run --all-files")


@task
def requirements(ctx: Context):
    """
    Export the *requirements.txt* file.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box('Exporting "requirements.txt" file...')
    ctx.run(
        "poetry run pip list --format=freeze | "
        'egrep -v "github.com/colour-science" '
        "> requirements.txt"
    )


@task(requirements)
def docker_build(ctx: Context):
    """
    Build the *docker* image.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box('Building "docker" image...')

    for platform in ("arm64", "amd64"):
        ctx.run(
            f"docker build --platform=linux/{platform} "
            f"-t {ORG}/{CONTAINER}:latest "
            f"-t {ORG}/{CONTAINER}:latest-{platform} "
            f"-t {ORG}/{CONTAINER}:v{app.__version__}-{platform} ."
        )


@task
def docker_remove(ctx: Context):
    """
    Stop and remove the *docker* container.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box('Stopping "docker" container...')
    try:
        ctx.run(f"docker stop {CONTAINER}")
    except Failure:
        pass

    message_box('Removing "docker" container...')
    try:
        ctx.run(f"docker rm {CONTAINER}")
    except Failure:
        pass


@task(docker_remove, docker_build)
def docker_run(ctx: Context):
    """
    Run the *docker* container.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box('Running "docker" container...')
    ctx.run(
        "docker run -d "
        f"--name={CONTAINER} "
        "-e COLOUR_DASH_SERVER=https://www.colour-science.org:8010/ "
        "-e COLOUR_DASH_CSS="
        "https://www.colour-science.org/assets/css/all-nocdn.css "
        "-e COLOUR_DASH_JS="
        "https://www.colour-science.org/assets/js/analytics.js,"
        "https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/3.6.1/"
        "iframeResizer.contentWindow.min.js "
        f"-p 8010:8000 {ORG}/{CONTAINER}"
    )


@task(clean, quality, precommit, docker_run)
def docker_push(ctx: Context):
    """
    Push the *docker* container.

    Parameters
    ----------
    ctx
        Context.
    """

    message_box('Pushing "docker" container...')
    ctx.run(f"docker push --all-tags {ORG}/{CONTAINER}")
