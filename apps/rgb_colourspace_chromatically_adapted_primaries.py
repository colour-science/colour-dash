"""
RGB Colourspace Chromatically Adapted Primaries Application
===========================================================
"""

import sys
import urllib.parse
from dash.dcc import Dropdown, Link, Markdown, Slider
from dash.dependencies import Input, Output
from dash.html import A, Code, Div, H3, H5, Li, Pre, Ul

from colour.colorimetry import CCS_ILLUMINANTS
from colour.models import RGB_COLOURSPACES, chromatically_adapted_primaries
from colour.utilities import numpy_print_options

from app import APP, SERVER_URL
from apps.common import (
    CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS,
    ILLUMINANTS_OPTIONS,
    RGB_COLOURSPACE_OPTIONS,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2018 Colour Developers"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "APP_NAME",
    "APP_PATH",
    "APP_DESCRIPTION",
    "APP_UID",
    "LAYOUT",
    "set_primaries_output",
]

APP_NAME: str = "RGB Colourspace Chromatically Adapted Primaries"
"""
App name.
"""

APP_PATH: str = f"/apps/{__name__.split('.')[-1]}"
"""
App path, i.e. app url.
"""

APP_DESCRIPTION: str = (
    "This app computes the "
    "*Chromatically Adapted Primaries* of the given "
    "*RGB Colourspace* to the given *Illuminant* using the "
    "given *Chromatic Adaptation Transform*."
)
"""
App description.
"""

APP_UID: int = hash(APP_NAME)
"""
App unique id.
"""

LAYOUT: Div = Div(
    [
        H3([Link(APP_NAME, href=APP_PATH)], className="text-center"),
        Div(
            [
                Markdown(APP_DESCRIPTION),
                H5(children="Colourspace"),
                Dropdown(
                    id=f"colourspace-{APP_UID}",
                    options=RGB_COLOURSPACE_OPTIONS,
                    value=RGB_COLOURSPACE_OPTIONS[0]["value"],
                    clearable=False,
                    className="app-widget",
                ),
                H5(children="Illuminant"),
                Dropdown(
                    id=f"illuminant-{APP_UID}",
                    options=ILLUMINANTS_OPTIONS,
                    value=ILLUMINANTS_OPTIONS[0]["value"],
                    clearable=False,
                    className="app-widget",
                ),
                H5(children="Chromatic Adaptation Transform"),
                Dropdown(
                    id=f"chromatic-adaptation-transform-{APP_UID}",
                    options=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS,
                    value=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS[0]["value"],
                    clearable=False,
                    className="app-widget",
                ),
                H5(children="Formatter"),
                Dropdown(
                    id=f"formatter-{APP_UID}",
                    options=[
                        {"label": "str", "value": "str"},
                        {"label": "repr", "value": "repr"},
                    ],
                    value="str",
                    clearable=False,
                    className="app-widget",
                ),
                H5(children="Decimals"),
                Slider(
                    id=f"decimals-{APP_UID}",
                    min=1,
                    max=15,
                    step=1,
                    value=10,
                    marks={i + 1: str(i + 1) for i in range(15)},
                    className="app-widget",
                ),
                Pre(
                    [Code(id=f"primaries-{APP_UID}", className="code shell")],
                    className="app-widget app-output",
                ),
                Ul(
                    [
                        Li(
                            [
                                Link(
                                    "Back to index...",
                                    href="/",
                                    className="app-link",
                                )
                            ],
                            className="list-inline-item",
                        ),
                        Li(
                            [
                                A(
                                    "Permalink",
                                    href=urllib.parse.urljoin(
                                        str(SERVER_URL), APP_PATH
                                    ),
                                    target="_blank",
                                )
                            ],
                            className="list-inline-item",
                        ),
                        Li(
                            [
                                A(
                                    "colour-science.org",
                                    href="https://www.colour-science.org",
                                    target="_blank",
                                )
                            ],
                            className="list-inline-item",
                        ),
                    ],
                    className="list-inline text-center",
                ),
            ],
            className="col-6 mx-auto",
        ),
    ]
)
"""
App layout, i.e. :class:`Div` class instance.

LAYOUT : Div
"""


@APP.callback(
    Output(component_id=f"primaries-{APP_UID}", component_property="children"),
    [
        Input(f"colourspace-{APP_UID}", "value"),
        Input(f"illuminant-{APP_UID}", "value"),
        Input(f"chromatic-adaptation-transform-{APP_UID}", "value"),
        Input(f"formatter-{APP_UID}", "value"),
        Input(f"decimals-{APP_UID}", "value"),
    ],
)
def set_primaries_output(
    colourspace: str,
    illuminant: str,
    chromatic_adaptation_transform: str,
    formatter: str,
    decimals: int,
) -> str:
    """
    Compute and write the chromatically adapted *primaries *of the given
    *RGB* colourspace to the given *illuminant* using the given
    *chromatic adaptation transform* into the output :class:`Pre` class
    instance.

    Parameters
    ----------
    colourspace
        *RGB* colourspace to chromatically adapt the *primaries*.
    illuminant
        *CIE 1931 2 Degree Standard Observer* illuminant to adapt the
        *primaries* to.
    chromatic_adaptation_transform
        *Chromatic adaptation transform* to use.
    formatter
        Formatter to use, :func:`str` or :func:`repr`.
    decimals
        Decimals to use when formatting the chromatically adapted *primaries*.

    Returns
    -------
    :class:`str`
        Chromatically adapted *primaries*.
    """

    P = chromatically_adapted_primaries(
        RGB_COLOURSPACES[colourspace].primaries,
        RGB_COLOURSPACES[colourspace].whitepoint,
        CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"][illuminant],
        chromatic_adaptation_transform,
    )

    with numpy_print_options(
        formatter={"float": f"{{: 0.{decimals}f}}".format},
        threshold=sys.maxsize,
    ):
        if formatter == "str":
            P_f = str(P)
        elif formatter == "repr":
            P_f = repr(P)

        return P_f
