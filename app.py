# -*- coding: utf-8 -*-
"""
Application
===========
"""

from __future__ import division, unicode_literals

import dash
from flask import Flask

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__application_name__ = 'Colour - Dash'

__major_version__ = '0'
__minor_version__ = '1'
__change_version__ = '0'
__version__ = '.'.join(
    (__major_version__,
     __minor_version__,
     __change_version__))  # yapf: disable

__all__ = ['SERVER', 'APP']

SERVER = Flask(__name__)
"""
*Flask* server hosting the *Dash* app.

SERVER : Flask 
"""

APP = dash.Dash(__application_name__, server=SERVER)
"""
*Dash* app.

APP : Dash 
"""

APP.config['suppress_callback_exceptions'] = True

APP.css.append_css({
    'external_url': [
        'http://colour-science.org/assets/css/all-nocdn.css',
        'http://colour-science.org/assets/css/custom.css',
        'http://colour-science.org/assets/css/font-awesome.css'
    ]
})

APP.scripts.append_script({
    'external_url':
    [('https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/3.6.1/'
      'iframeResizer.contentWindow.min.js')]
})
