# -*- coding: utf-8 -*-
"""
RGB Colourspace Models Chromatically Adapted Primaries Application
==================================================================
"""

from __future__ import division, unicode_literals

import numpy as np
from dash.dependencies import Input, Output
from dash_core_components import Dropdown, Markdown, Slider, Textarea
from dash_html_components import Code, Div, H3, H5, Pre

import colour

from app import APP
from apps.common import (CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS,
                         ILLUMINANTS_OPTIONS, RGB_COLOURSPACES_OPTIONS)

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'APP_NAME', 'APP_DESCRIPTION', 'UID', 'LAYOUT', 'set_Primaries_Textarea'
]

APP_NAME = 'RGB Colourspace Models Chromatically Adapted Primaries'
APP_DESCRIPTION = ('This app computes the '
                   '*Chromatically Adapted Primaries* of the given '
                   '*RGB Colourspace Model* to the given *Illuminant*'
                   ' using the given *Chromatic Adaptation Transform*.')
UID = hash(APP_NAME)
LAYOUT = Div(
    [
        H3(children=APP_NAME, className='text-center'),
        Markdown(APP_DESCRIPTION),
        H5(children='Input Colourspace'),
        Dropdown(
            id='input-colourspace-{0}'.format(UID),
            options=RGB_COLOURSPACES_OPTIONS,
            value=RGB_COLOURSPACES_OPTIONS[0]['value'],
            clearable=False),
        H5(children='Illuminant'),
        Dropdown(
            id='illuminant-{0}'.format(UID),
            options=ILLUMINANTS_OPTIONS,
            value=ILLUMINANTS_OPTIONS[0]['value'],
            clearable=False),
        H5(children='Chromatic Adaptation Transform'),
        Dropdown(
            id='chromatic-adaptation-transform-{0}'.format(UID),
            options=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS,
            value=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS[0]['value'],
            clearable=False),
        H5(children='Formatter'),
        Dropdown(
            id='formatter-{0}'.format(UID),
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
        Slider(id='decimals-{0}'.format(UID), min=1, max=15, step=1, value=10),
        Pre([Code(id='primaries-{0}'.format(UID), className='code shell')]),
    ],
    className='col-md-6 col-md-offset-3')


@APP.callback(
    Output(
        component_id='primaries-{0}'.format(UID),
        component_property='children'), [
            Input('input-colourspace-{0}'.format(UID), 'value'),
            Input('illuminant-{0}'.format(UID), 'value'),
            Input('chromatic-adaptation-transform-{0}'.format(UID), 'value'),
            Input('formatter-{0}'.format(UID), 'value'),
            Input('decimals-{0}'.format(UID), 'value')
        ])
def set_Primaries_Textarea(input_colourspace, illuminant,
                           chromatic_adaptation_transform, formatter,
                           decimals):
    P = colour.chromatically_adapted_primaries(
        colour.RGB_COLOURSPACES[input_colourspace].primaries,
        colour.RGB_COLOURSPACES[input_colourspace].whitepoint,
        colour.ILLUMINANTS['CIE 1931 2 Degree Standard Observer'][illuminant],
        chromatic_adaptation_transform)

    with colour.utilities.numpy_print_options(
            formatter={'float': ('{{:0.{0}f}}'.format(decimals)).format},
            threshold=np.nan):
        if formatter == 'str':
            P = str(P)
        elif formatter == 'repr':
            P = repr(P)

        return P
