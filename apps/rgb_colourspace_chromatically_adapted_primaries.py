"""
RGB Colourspace Chromatically Adapted Primaries Application
===========================================================
"""

import sys
import urllib.parse
from contextlib import suppress
from dash.dcc import Dropdown, Link, Location, Markdown, Slider
from dash.dependencies import Input, Output
from dash.html import A, Code, Div, H3, H5, Li, Pre, Ul
from urllib.parse import parse_qs, urlencode, urlparse

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
    "DEFAULT_STATE",
    "LAYOUT",
    "set_primaries_output",
    "update_state_on_url_query_change",
    "update_url_query_on_state_change",
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

DEFAULT_STATE = {
    "colourspace": RGB_COLOURSPACE_OPTIONS[0]["value"],
    "illuminant": ILLUMINANTS_OPTIONS[0]["value"],
    "chromatic_adaptation_transform": CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS[
        0
    ]["value"],
    "formatter": "str",
    "decimals": 10,
}
"""
Default App state.
"""

LAYOUT: Div = Div(
    [
        Location(id=f"url-{APP_UID}", refresh=False),
        H3([Link(APP_NAME, href=APP_PATH)], className="text-center"),
        Div(
            [
                Markdown(APP_DESCRIPTION),
                H5(children="Colourspace"),
                Dropdown(
                    id=f"colourspace-{APP_UID}",
                    options=RGB_COLOURSPACE_OPTIONS,
                    value=DEFAULT_STATE["colourspace"],
                    clearable=False,
                    className="app-widget",
                ),
                H5(children="Illuminant"),
                Dropdown(
                    id=f"illuminant-{APP_UID}",
                    options=ILLUMINANTS_OPTIONS,
                    value=DEFAULT_STATE["illuminant"],
                    clearable=False,
                    className="app-widget",
                ),
                H5(children="Chromatic Adaptation Transform"),
                Dropdown(
                    id=f"chromatic-adaptation-transform-{APP_UID}",
                    options=CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS,
                    value=DEFAULT_STATE["chromatic_adaptation_transform"],
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
                    value=DEFAULT_STATE["formatter"],
                    clearable=False,
                    className="app-widget",
                ),
                H5(children="Decimals"),
                Slider(
                    id=f"decimals-{APP_UID}",
                    min=1,
                    max=15,
                    step=1,
                    value=DEFAULT_STATE["decimals"],
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


@APP.callback(
    [
        Output(f"colourspace-{APP_UID}", "value"),
        Output(f"illuminant-{APP_UID}", "value"),
        Output(f"chromatic-adaptation-transform-{APP_UID}", "value"),
        Output(f"formatter-{APP_UID}", "value"),
        Output(f"decimals-{APP_UID}", "value"),
    ],
    [
        Input("url", "href"),
    ],
)
def update_state_on_url_query_change(href: str) -> tuple:
    """
    Update the App state on URL query change.

    Parameters
    ----------
    href
        URL.

    Returns
    -------
    :class:`tuple`
        App state.
    """

    parse_result = urlparse(href)

    query = parse_qs(parse_result.query)

    def value_from_query(value: str) -> str:
        """Return the given value from the query."""

        with suppress(KeyError):
            return query[value][0]

        return DEFAULT_STATE[value.replace("-", "_")]

    state = (
        value_from_query("colourspace"),
        value_from_query("illuminant"),
        value_from_query("chromatic-adaptation-transform"),
        value_from_query("formatter"),
        int(value_from_query("decimals")),
    )

    return state


@APP.callback(
    Output(f"url-{APP_UID}", "search"),
    [
        Input(f"colourspace-{APP_UID}", "value"),
        Input(f"illuminant-{APP_UID}", "value"),
        Input(f"chromatic-adaptation-transform-{APP_UID}", "value"),
        Input(f"formatter-{APP_UID}", "value"),
        Input(f"decimals-{APP_UID}", "value"),
    ],
)
def update_url_query_on_state_change(
    colourspace: str,
    illuminant: str,
    chromatic_adaptation_transform: str,
    formatter: str,
    decimals: int,
) -> str:
    """
    Update the URL query on App state change.

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
        Formatter to use, :func:`str`, :func:`repr` or *Nuke*.
    decimals
        Decimals to use when formatting the chromatically adapted *primaries*.

    Returns
    -------
    :class:`str`
        Url query.
    """

    query = urlencode(
        {
            "colourspace": colourspace,
            "illuminant": illuminant,
            "chromatic-adaptation-transform": chromatic_adaptation_transform,
            "formatter": formatter,
            "decimals": decimals,
        }
    )

    return f"?{query}"
