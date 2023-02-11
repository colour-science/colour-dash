"""
Invoke - Tasks
==============
"""

import contextlib
import platform
from invoke.exceptions import Failure

from colour.utilities import message_box

import app

import inspect

if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec  # pyright: ignore

from invoke import Context, task

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
    "docker_push",
]

APPLICATION_NAME: str = app.__application_name__

ORG: str = "colourscience"

CONTAINER: str = APPLICATION_NAME.replace(" ", "").lower()


@task
def clean(ctx: Context, bytecode: bool = False):
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
    pyright: bool = True,
):
    """
    Check the codebase with *Pyright*.

    Parameters
    ----------
    ctx
        Context.
    pyright
        Whether to check the codebase with *Pyright*.
    """

    if pyright:
        message_box('Checking codebase with "Pyright"...')
        ctx.run("pyright --skipunannotated --level warning")


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

    for architecture in ("arm64", "amd64"):
        ctx.run(
            f"docker build --platform=linux/{architecture} "
            f"-t {ORG}/{CONTAINER}:latest "
            f"-t {ORG}/{CONTAINER}:latest-{architecture} "
            f"-t {ORG}/{CONTAINER}:v{app.__version__}-{architecture} ."
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
    with contextlib.suppress(Failure):
        ctx.run(f"docker stop {CONTAINER}")

    message_box('Removing "docker" container...')
    with contextlib.suppress(Failure):
        ctx.run(f"docker rm {CONTAINER}")


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
        f"-p 8010:8000 {ORG}/{CONTAINER}:latest-{platform.uname()[4].lower()}"
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
