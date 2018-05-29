# -*- coding: utf-8 -*-
"""
Application
===========
"""

from __future__ import division, unicode_literals

import dash
from dash_html_components import A, Div, Footer, H1

from widgets import (
    RGB_colourspace_models_transformation_matrix_widget,
    RGB_colourspace_models_chromatically_adapted_primaries_widget)

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['main']


def main():
    application = dash.Dash('Colour Science')
    application.config['suppress_callback_exceptions'] = True

    application.layout = Div(
        [
            H1(children=[
                A('Colour - Dash', href='http://colour-science.org/')
            ],
               className='text-center'),
            Div([], className='row'),
            Footer(
                children=[
                    'Copyright © 2018 – Colour Developers – ',
                    A('colour-science@googlegroups.com',
                      href='mailto:colour-science@googlegroups.com')
                ],
                id='footer',
                className='text-center')
        ],
        className='container')
    application.layout.children[1].children.extend([
        RGB_colourspace_models_transformation_matrix_widget(application),
        RGB_colourspace_models_chromatically_adapted_primaries_widget(
            application)
    ])

    application.css.append_css({
        'external_url': [
            'http://colour-science.org/assets/css/all-nocdn.css',
            'http://colour-science.org/assets/css/font-awesome.css'
        ]
    })

    application.run_server()


if __name__ == '__main__':
    main()
