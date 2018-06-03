# -*- coding: utf-8 -*-
"""
RGB Colourspace Models Transformation Matrix Application
========================================================
"""

from __future__ import division, unicode_literals

import numpy as np
import urlparse
from dash.dependencies import Input, Output
from dash_core_components import Dropdown, Link, Markdown, Slider, Textarea
from dash_html_components import A, Code, Div, H3, H5, Li, Pre, Ul

import colour

from app import APP, SERVER_URL
from apps.common import (CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS,
                         NUKE_COLORMATRIX_NODE_TEMPLATE,
                         RGB_COLOURSPACES_OPTIONS, nuke_format_matrix)

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'APP_NAME', 'APP_NAME', 'APP_DESCRIPTION', 'APP_UID', 'LAYOUT',
    'set_RGB_to_RGB_matrix_output'
]

APP_NAME = 'RGB Colourspace Models Transformation Matrix'
"""
App name.

APP_NAME : unicode
"""

APP_PATH = '/apps/{0}'.format(__name__.split('.')[-1])
"""
App path, i.e. app url.

APP_PATH : unicode
"""

APP_DESCRIPTION = ('This app computes the colour transformation '
                   'matrix from the *Input RGB Colourspace* to the '
                   '*Output RGB Colourspace* using the given '
                   '*Chromatic Adaptation Transform*.')
"""
App description.

APP_DESCRIPTION : unicode
"""

APP_UID = hash(APP_NAME)
"""
App unique id.

APP_UID : unicode
"""

LAYOUT = Div([
    H3([Link(APP_NAME, href=APP_PATH)], className='text-center'),
    Div([
        Markdown(APP_DESCRIPTION),
        H5(children='Input Colourspace'),
        Dropdown(
            id='input-colourspace-{0}'.format(APP_UID),
            options=RGB_COLOURSPACES_OPTIONS,
            value=RGB_COLOURSPACES_OPTIONS[0]['value'],
            clearable=False),
        H5(children='Output Colourspace'),
        Dropdown(
            id='output-colourspace-{0}'.format(APP_UID),
            options=RGB_COLOURSPACES_OPTIONS,
            value=RGB_COLOURSPACES_OPTIONS[0]['value'],
            clearable=False),
        H5(children='Chromatic Adaptation Transform'),
        Dropdown(
            id='chromatic-adaptation-transform-{0}'.format(APP_UID),
            options=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS,
            value=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS[0]['value'],
            clearable=False),
        H5(children='Formatter'),
        Dropdown(
            id='formatter-{0}'.format(APP_UID),
            options=[{
                'label': 'str',
                'value': 'str'
            }, {
                'label': 'repr',
                'value': 'repr'
            }, {
                'label': 'Nuke',
                'value': 'Nuke'
            }],
            value='str',
            clearable=False),
        H5(children='Decimals'),
        Slider(
            id='decimals-{0}'.format(APP_UID),
            min=1,
            max=15,
            step=1,
            value=10,
            marks={i + 1: str(i + 1)
                   for i in range(15)}),
        Pre([
            Code(
                id='RGB-transformation-matrix-{0}'.format(APP_UID),
                className='code shell')
        ],
            className='app-output'),
        Ul([
            Li([Link('Back to index...', href='/')]),
            Li([A('Permalink', href=urlparse.urljoin(SERVER_URL, APP_PATH))]),
            Li([A('colour-science.org', href='http://colour-science.org')]),
        ],
           className='list-inline text-center'),
    ],
        className='col-md-6 col-md-offset-3')
])
"""
App layout, i.e. :class:`Div` class instance.

LAYOUT : Div
"""


@APP.callback(
    Output(
        component_id='RGB-transformation-matrix-{0}'.format(APP_UID),
        component_property='children'),
    [
        Input('input-colourspace-{0}'.format(APP_UID), 'value'),
        Input('output-colourspace-{0}'.format(APP_UID), 'value'),
        Input('chromatic-adaptation-transform-{0}'.format(APP_UID), 'value'),
        Input('formatter-{0}'.format(APP_UID), 'value'),
        Input('decimals-{0}'.format(APP_UID), 'value')
    ])
def set_RGB_to_RGB_matrix_output(input_colourspace, output_colourspace,
                                 chromatic_adaptation_transform, formatter,
                                 decimals):
    """
    Computes and writes the colour transformation matrix from given input *RGB*
    colourspace to the output *RGB* colourspace using given
    *chromatic adaptation transform* into the output :class:`Pre` class
    instance.

    Parameters
    ----------
    input_colourspace : unicode
        Input *RGB* colourspace.
    output_colourspace : unicode
        Output *RGB* colourspace.
    chromatic_adaptation_transform : unicode
        *Chromatic adaptation transform* to use.
    formatter : unicode
        Formatter to use, :func:`str`, :func:`repr` or *Nuke*.
    decimals : int
        Decimals to use when formatting the colour transformation matrix.

    Returns
    -------
    unicode
        Colour transformation matrix.
    """

    M = colour.RGB_to_RGB_matrix(colour.RGB_COLOURSPACES[input_colourspace],
                                 colour.RGB_COLOURSPACES[output_colourspace],
                                 chromatic_adaptation_transform)

    with colour.utilities.numpy_print_options(
            formatter={'float': ('{{: 0.{0}f}}'.format(decimals)).format},
            threshold=np.nan):
        if formatter == 'str':
            M = str(M)
        elif formatter == 'repr':
            M = repr(M)
        else:
            M = NUKE_COLORMATRIX_NODE_TEMPLATE.format(
                nuke_format_matrix(M, decimals), '{0}_to_{1}'.format(
                    input_colourspace.replace(' ', '_'),
                    output_colourspace.replace(' ', '_')))
        return M
