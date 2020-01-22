# -*- coding: utf-8 -*-
"""
RGB Colourspace Chromatically Adapted Primaries Application
===========================================================
"""

from __future__ import division, unicode_literals

import sys
import urllib.parse
from dash.dependencies import Input, Output
from dash_core_components import Dropdown, Link, Markdown, Slider
from dash_html_components import A, Code, Div, H3, H5, Li, Pre, Ul

import colour

from app import APP, SERVER_URL
from apps.common import (CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS,
                         ILLUMINANTS_OPTIONS, RGB_COLOURSPACES_OPTIONS)

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2018-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'APP_NAME', 'APP_PATH', 'APP_DESCRIPTION', 'APP_UID', 'LAYOUT',
    'set_primaries_output'
]

APP_NAME = 'RGB Colourspace Chromatically Adapted Primaries'
"""
App name.

APP_NAME : unicode
"""

APP_PATH = '/apps/{0}'.format(__name__.split('.')[-1])
"""
App path, i.e. app url.

APP_PATH : unicode
"""

APP_DESCRIPTION = ('This app computes the '
                   '*Chromatically Adapted Primaries* of the given '
                   '*RGB Colourspace* to the given *Illuminant* using the '
                   'given *Chromatic Adaptation Transform*.')
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
        H5(children='Colourspace'),
        Dropdown(
            id='colourspace-{0}'.format(APP_UID),
            options=RGB_COLOURSPACES_OPTIONS,
            value=RGB_COLOURSPACES_OPTIONS[0]['value'],
            clearable=False,
            className='app-widget'),
        H5(children='Illuminant'),
        Dropdown(
            id='illuminant-{0}'.format(APP_UID),
            options=ILLUMINANTS_OPTIONS,
            value=ILLUMINANTS_OPTIONS[0]['value'],
            clearable=False,
            className='app-widget'),
        H5(children='Chromatic Adaptation Transform'),
        Dropdown(
            id='chromatic-adaptation-transform-{0}'.format(APP_UID),
            options=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS,
            value=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS[0]['value'],
            clearable=False,
            className='app-widget'),
        H5(children='Formatter'),
        Dropdown(
            id='formatter-{0}'.format(APP_UID),
            options=[{
                'label': 'str',
                'value': 'str'
            }, {
                'label': 'repr',
                'value': 'repr'
            }],
            value='str',
            clearable=False,
            className='app-widget'),
        H5(children='Decimals'),
        Slider(
            id='decimals-{0}'.format(APP_UID),
            min=1,
            max=15,
            step=1,
            value=10,
            marks={i + 1: str(i + 1)
                   for i in range(15)},
            className='app-widget'),
        Pre([Code(id='primaries-{0}'.format(APP_UID), className='code shell')],
            className='app-widget app-output'),
        Ul([
            Li([Link('Back to index...', href='/', className='app-link')],
               className='list-inline-item'),
            Li([
                A('Permalink',
                  href=urllib.parse.urljoin(SERVER_URL, APP_PATH),
                  target='_blank')
            ],
               className='list-inline-item'),
            Li([
                A('colour-science.org',
                  href='https://www.colour-science.org',
                  target='_blank')
            ],
               className='list-inline-item'),
        ],
           className='list-inline text-center'),
    ],
        className='col-6 mx-auto')
])
"""
App layout, i.e. :class:`Div` class instance.

LAYOUT : Div
"""


@APP.callback(
    Output(
        component_id='primaries-{0}'.format(APP_UID),
        component_property='children'),
    [
        Input('colourspace-{0}'.format(APP_UID), 'value'),
        Input('illuminant-{0}'.format(APP_UID), 'value'),
        Input('chromatic-adaptation-transform-{0}'.format(APP_UID), 'value'),
        Input('formatter-{0}'.format(APP_UID), 'value'),
        Input('decimals-{0}'.format(APP_UID), 'value')
    ])
def set_primaries_output(colourspace, illuminant,
                         chromatic_adaptation_transform, formatter, decimals):
    """
    Computes and writes the chromatically adapted *primaries *of the given
    *RGB* colourspace to the given *illuminant* using the given
    *chromatic adaptation transform*to into the output :class:`Pre` class
    instance.

    Parameters
    ----------
    colourspace : unicode
        *RGB* colourspace to chromatically adapt the *primaries*.
    illuminant : unicode
        *CIE 1931 2 Degree Standard Observer* illuminant to adapt the
        *primaries* to.
    chromatic_adaptation_transform : unicode
        *Chromatic adaptation transform* to use.
    formatter : unicode
        Formatter to use, :func:`str` or :func:`repr`.
    decimals : int
        Decimals to use when formatting the chromatically adapted *primaries*.

    Returns
    -------
    unicode
        Chromatically adapted *primaries*.
    """

    P = colour.chromatically_adapted_primaries(
        colour.RGB_COLOURSPACES[colourspace].primaries,
        colour.RGB_COLOURSPACES[colourspace].whitepoint,
        colour.ILLUMINANTS['CIE 1931 2 Degree Standard Observer'][illuminant],
        chromatic_adaptation_transform)

    with colour.utilities.numpy_print_options(
            formatter={'float': ('{{: 0.{0}f}}'.format(decimals)).format},
            threshold=sys.maxsize):
        if formatter == 'str':
            P = str(P)
        elif formatter == 'repr':
            P = repr(P)

        return P
