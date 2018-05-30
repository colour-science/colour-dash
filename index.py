# -*- coding: utf-8 -*-
"""
Index
=====
"""

from __future__ import division, unicode_literals

from dash.dependencies import Input, Output
from dash_core_components import Link, Location, Markdown
from dash_html_components import Div, H2

from app import APP
from apps import (rgb_colourspace_models_chromatically_adapted_primaries,
                  rgb_colourspace_models_transformation_matrix)

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['load_app']

APP.layout = Div([
    Location(id='url', refresh=False),
    Div(id='page-content', className='row')
])


@APP.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def load_app(app):
    if app == '/apps/rgb_colourspace_models_transformation_matrix':
        return rgb_colourspace_models_transformation_matrix.LAYOUT
    elif app == '/apps/rgb_colourspace_models_chromatically_adapted_primaries':
        return rgb_colourspace_models_chromatically_adapted_primaries.LAYOUT
    else:
        return Div(
            [
                Div([
                    H2([
                        Link(
                            rgb_colourspace_models_transformation_matrix.
                            APP_NAME,
                            href=
                            '/apps/rgb_colourspace_models_transformation_matrix'
                        )
                    ]),
                    Markdown(rgb_colourspace_models_transformation_matrix.
                             APP_DESCRIPTION),
                    H2([
                        Link(
                            rgb_colourspace_models_chromatically_adapted_primaries.
                            APP_NAME,
                            href=
                            '/apps/rgb_colourspace_models_chromatically_adapted_primaries'
                        )
                    ]),
                    Markdown(
                        rgb_colourspace_models_chromatically_adapted_primaries.
                        APP_DESCRIPTION),
                ]),
            ],
            className='row')


if __name__ == '__main__':
    APP.run_server(host='0.0.0.0')
