# -*- coding: utf-8 -*-
"""
Invoke - Tasks
==============
"""

from __future__ import print_function, unicode_literals

from invoke import task

from colour.utilities import message_box

import app

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'APPLICATION_NAME', 'ORG', 'CONTAINER', 'clean', 'formatting',
    'docker_build', 'docker_remove', 'docker_run'
]

APPLICATION_NAME = app.__application_name__

ORG = 'colourscience'

CONTAINER = APPLICATION_NAME.replace(' ', '').lower()


@task
def clean(ctx, bytecode=False):
    """
    Cleans the project.

    Parameters
    ----------
    bytecode : bool, optional
        Whether to clean the bytecode files, e.g. *.pyc* files.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Cleaning project...')

    patterns = []

    if bytecode:
        patterns.append('**/*.pyc')

    for pattern in patterns:
        ctx.run("rm -rf {}".format(pattern))


@task
def formatting(ctx, yapf=False):
    """
    Formats the codebase with *Yapf*.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.
    yapf : bool, optional
        Whether to format the codebase with *Yapf*.

    Returns
    -------
    bool
        Task success.
    """

    if yapf:
        message_box('Formatting codebase with "Yapf"...')
        ctx.run('yapf -p -i -r .')


@task
def docker_build(ctx):
    """
    Builds the *docker* image.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Building "docker" image...')

    ctx.run('docker build -t {0}/{1}:latest -t {0}/{1}:v{2} .'.format(
        ORG, CONTAINER, app.__version__))


@task
def docker_remove(ctx):
    """
    Stops and remove the *docker* container.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Stopping "docker" container...')
    ctx.run('docker stop {0}'.format(CONTAINER))

    message_box('Removing "docker" container...')
    ctx.run('docker rm {0}'.format(CONTAINER))


@task(docker_remove, docker_build)
def docker_run(ctx):
    """
    Runs the *docker* container.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Running "docker" container...')
    ctx.run('docker run -d '
            '--name={1} '
            '-e COLOUR_DASH_SERVER=http://colour-science.org:8010/'
            ' -p 8010:8000 {0}/{1}'.format(ORG, CONTAINER))


@task
def docker_push(ctx):
    """
    Pushes the *docker* container.

    Parameters
    ----------
    ctx : invoke.context.Context
        Context.

    Returns
    -------
    bool
        Task success.
    """

    message_box('Pushing "docker" container...')
    ctx.run('docker push {0}/{1}'.format(ORG, CONTAINER))