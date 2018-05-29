# -*- coding: utf-8 -*-
"""
Widgets
=======
"""

from __future__ import division, unicode_literals

import numpy as np
from dash.dependencies import Input, Output
from dash_core_components import Dropdown, Markdown, Slider, Textarea
from dash_html_components import Code, Div, H3, H5, Pre

import colour

from common import NUKE_COLORMATRIX_NODE_TEMPLATE, nuke_format_matrix

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'RGB_COLOURSPACES_OPTIONS', 'CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS',
    'ILLUMINANTS_OPTIONS',
    'RGB_colourspace_models_transformation_matrix_widget',
    'RGB_colourspace_models_chromatically_adapted_primaries_widget'
]

RGB_COLOURSPACES_OPTIONS = [{
    'label': key,
    'value': key
} for key in sorted(colour.RGB_COLOURSPACES.keys())]

CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS = [{
    'label': key,
    'value': key
} for key in sorted(colour.CHROMATIC_ADAPTATION_TRANSFORMS.keys())]

ILLUMINANTS_OPTIONS = [{
    'label': key,
    'value': key
} for key in sorted(colour.ILLUMINANTS['CIE 1931 2 Degree Standard Observer']
                    .keys())]


def RGB_colourspace_models_transformation_matrix_widget(application):
    div = Div(
        [
            H3(children='RGB Colourspace Models Transformation Matrix',
               className='text-center'),
            Markdown('This widget computes the colour transformation '
                     'matrix from the *Input RGB Colourspace* to the '
                     '*Output RGB Colourspace* using the given '
                     '*Chromatic Adaptation Transform*.'),
            H5(children='Input Colourspace'),
            Dropdown(
                id='input-colourspace-w1',
                options=RGB_COLOURSPACES_OPTIONS,
                value=RGB_COLOURSPACES_OPTIONS[0]['value'],
                clearable=False),
            H5(children='Output Colourspace'),
            Dropdown(
                id='output-colourspace-w1',
                options=RGB_COLOURSPACES_OPTIONS,
                value=RGB_COLOURSPACES_OPTIONS[0]['value'],
                clearable=False),
            H5(children='Chromatic Adaptation Transform'),
            Dropdown(
                id='chromatic-adaptation-transform-w1',
                options=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS,
                value=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS[0]['value'],
                clearable=False),
            H5(children='Formatter'),
            Dropdown(
                id='formatter-w1',
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
            Slider(id='decimals-w1', min=1, max=15, step=1, value=10),
            Pre([
                Code(
                    id='RGB-transformation-matrix-w1', className='code shell')
            ]),
        ],
        className='col-md-6')

    @application.callback(
        Output(
            component_id='RGB-transformation-matrix-w1',
            component_property='children'), [
                Input('input-colourspace-w1', 'value'),
                Input('output-colourspace-w1', 'value'),
                Input('chromatic-adaptation-transform-w1', 'value'),
                Input('formatter-w1', 'value'),
                Input('decimals-w1', 'value')
            ])
    def set_RGB_to_RGB_matrix_Textarea(input_colourspace, output_colourspace,
                                       chromatic_adaptation_transform,
                                       formatter, decimals):
        M = colour.RGB_to_RGB_matrix(
            colour.RGB_COLOURSPACES[input_colourspace],
            colour.RGB_COLOURSPACES[output_colourspace],
            chromatic_adaptation_transform)

        with colour.utilities.numpy_print_options(
                formatter={'float': ('{{:0.{0}f}}'.format(decimals)).format},
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

    return div


def RGB_colourspace_models_chromatically_adapted_primaries_widget(application):
    div = Div(
        [
            H3(children=
               'RGB Colourspace Models Chromatically Adapted Primaries',
               className='text-center'),
            Markdown('This widget computes the '
                     '*Chromatically Adapted Primaries* of the given '
                     '*RGB Colourspace Model* to the given *Illuminant*'
                     ' using the given *Chromatic Adaptation Transform*.'),
            H5(children='Input Colourspace'),
            Dropdown(
                id='input-colourspace-w2',
                options=RGB_COLOURSPACES_OPTIONS,
                value=RGB_COLOURSPACES_OPTIONS[0]['value'],
                clearable=False),
            H5(children='Illuminant'),
            Dropdown(
                id='illuminant-w2',
                options=ILLUMINANTS_OPTIONS,
                value=ILLUMINANTS_OPTIONS[0]['value'],
                clearable=False),
            H5(children='Chromatic Adaptation Transform'),
            Dropdown(
                id='chromatic-adaptation-transform-w2',
                options=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS,
                value=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS[0]['value'],
                clearable=False),
            H5(children='Formatter'),
            Dropdown(
                id='formatter-w2',
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
            Slider(id='decimals-w2', min=1, max=15, step=1, value=10),
            Pre([Code(id='primaries-w2', className='code shell')]),
        ],
        className='col-md-6')

    @application.callback(
        Output(component_id='primaries-w2', component_property='children'), [
            Input('input-colourspace-w2', 'value'),
            Input('illuminant-w2', 'value'),
            Input('chromatic-adaptation-transform-w2', 'value'),
            Input('formatter-w2', 'value'),
            Input('decimals-w2', 'value')
        ])
    def set_Primaries_Textarea(input_colourspace, illuminant,
                               chromatic_adaptation_transform, formatter,
                               decimals):
        P = colour.chromatically_adapted_primaries(
            colour.RGB_COLOURSPACES[input_colourspace].primaries,
            colour.RGB_COLOURSPACES[input_colourspace].whitepoint,
            colour.ILLUMINANTS['CIE 1931 2 Degree Standard Observer'][
                illuminant], chromatic_adaptation_transform)

        with colour.utilities.numpy_print_options(
                formatter={'float': ('{{:0.{0}f}}'.format(decimals)).format},
                threshold=np.nan):
            if formatter == 'str':
                P = str(P)
            elif formatter == 'repr':
                P = repr(P)

            return P

    return div
