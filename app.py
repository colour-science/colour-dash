# -*- coding: utf-8 -*-
"""
Application
===========
"""

from __future__ import division, unicode_literals

import dash
import os
from flask import Flask

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2018-2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__application_name__ = 'Colour - Dash'

__major_version__ = '0'
__minor_version__ = '1'
__change_version__ = '11'
__version__ = '.'.join(
    (__major_version__,
     __minor_version__,
     __change_version__))  # yapf: disable

__all__ = ['SERVER', 'SERVER_URL', 'APP']

SERVER = Flask(__name__)
"""
*Flask* server hosting the *Dash* app.

SERVER : Flask
"""

SERVER_URL = os.environ.get('COLOUR_DASH_SERVER')
"""
Server url used to construct permanent links for the individual apps.

SERVER_URL : unicode
"""

APP = dash.Dash(
    __application_name__,
    external_scripts=os.environ.get('COLOUR_DASH_JS', '').split(','),
    external_stylesheets=os.environ.get('COLOUR_DASH_CSS', '').split(','),
    server=SERVER)
"""
*Dash* app.

APP : Dash
"""

APP.config['suppress_callback_exceptions'] = True
