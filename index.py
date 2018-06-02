# -*- coding: utf-8 -*-
"""
Index
=====
"""

from __future__ import division, unicode_literals

from dash.dependencies import Input, Output
from dash_core_components import Link, Location, Markdown
from dash_html_components import Div, H2

import apps.rgb_colourspace_models_transformation_matrix as app_1
import apps.rgb_colourspace_models_chromatically_adapted_primaries as app_2
from app import SERVER, APP

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['load_app']

APP.layout = Div(
    [Location(id='url', refresh=False),
     Div(id='apps', className='row')])


@APP.callback(Output('apps', 'children'), [Input('url', 'pathname')])
def load_app(app):
    if app == app_1.APP_PATH:
        return app_1.LAYOUT
    elif app == app_2.APP_PATH:
        return app_2.LAYOUT
    else:
        return Div(
            [
                Div([
                    H2([Link(app_1.APP_NAME, href=app_1.APP_PATH)]),
                    Markdown(app_1.APP_DESCRIPTION.replace('This app c', 'C')),
                    H2([Link(app_2.APP_NAME, href=app_2.APP_PATH)]),
                    Markdown(app_2.APP_DESCRIPTION.replace('This app c', 'C')),
                ]),
            ],
            className='row')


if __name__ == '__main__':
    APP.run_server(debug=True)
