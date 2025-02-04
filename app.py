"""
Application
===========
"""

import os

import dash
from flask import Flask

__author__ = "Colour Developers"
__copyright__ = "Copyright 2018 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__application_name__ = "Colour - Dash"

__major_version__ = "0"
__minor_version__ = "2"
__change_version__ = "8"
__version__ = f"{__major_version__}.{__minor_version__}.{__change_version__}"

__all__ = ["SERVER", "SERVER_URL", "APP"]

SERVER: Flask = Flask(__name__)
"""
*Flask* server hosting the *Dash* app.
"""

SERVER_URL: str | None = os.environ.get("COLOUR_DASH_SERVER")
"""
Server url used to construct permanent links for the individual apps.
"""

APP: dash.Dash = dash.Dash(
    __application_name__,
    external_scripts=os.environ.get("COLOUR_DASH_JS", "").split(","),  # pyright: ignore
    external_stylesheets=os.environ.get("COLOUR_DASH_CSS", "").split(","),  # pyright: ignore
    server=SERVER,
)
"""
*Dash* app.
"""

APP.config["suppress_callback_exceptions"] = True
