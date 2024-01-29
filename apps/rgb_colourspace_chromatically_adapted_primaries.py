"""
RGB Colourspace Chromatically Adapted Primaries Application
===========================================================
"""

import sys
import urllib.parse
from contextlib import suppress
from urllib.parse import parse_qs, urlencode, urlparse

from colour.colorimetry import CCS_ILLUMINANTS
from colour.models import RGB_COLOURSPACES, chromatically_adapted_primaries
from colour.utilities import numpy_print_options
from dash.dcc import Dropdown, Link, Location, Markdown, Slider
from dash.dependencies import Input, Output
from dash.html import H3, H5, A, Button, Code, Div, Li, Pre, Ul

from app import APP, SERVER_URL
from apps.common import (
    OPTIONS_CHROMATIC_ADAPTATION_TRANSFORM,
    OPTIONS_ILLUMINANTS,
    OPTIONS_RGB_COLOURSPACE,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2018 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "APP_NAME",
    "APP_PATH",
    "APP_DESCRIPTION",
    "APP_UID",
    "STATE_DEFAULT",
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


def _uid(id_):
    """
    Generate a unique id for given id by appending the application *UID*.
    """

    return f"{id_}-{APP_UID}"


STATE_DEFAULT = {
    "colourspace": OPTIONS_RGB_COLOURSPACE[0]["value"],
    "illuminant": OPTIONS_ILLUMINANTS[0]["value"],
    "chromatic_adaptation_transform": OPTIONS_CHROMATIC_ADAPTATION_TRANSFORM[0][
        "value"
    ],
    "formatter": "str",
    "decimals": 10,
}
"""
Default App state.
"""

LAYOUT: Div = Div(
    [
        Div(className="col-2"),
        Div(
            [
                Location(id=_uid("url"), refresh=False),
                H3([Link(APP_NAME, href=APP_PATH)], className="text-center"),
                Div(
                    [
                        Markdown(APP_DESCRIPTION),
                        H5(children="Colourspace"),
                        Dropdown(
                            id=_uid("colourspace"),
                            options=OPTIONS_RGB_COLOURSPACE,
                            value=STATE_DEFAULT["colourspace"],
                            clearable=False,
                            className="app-widget",
                        ),
                        H5(children="Illuminant"),
                        Dropdown(
                            id=_uid("illuminant"),
                            options=OPTIONS_ILLUMINANTS,
                            value=STATE_DEFAULT["illuminant"],
                            clearable=False,
                            className="app-widget",
                        ),
                        H5(children="Chromatic Adaptation Transform"),
                        Dropdown(
                            id=_uid("chromatic-adaptation-transform"),
                            options=OPTIONS_CHROMATIC_ADAPTATION_TRANSFORM,
                            value=STATE_DEFAULT["chromatic_adaptation_transform"],
                            clearable=False,
                            className="app-widget",
                        ),
                        H5(children="Formatter"),
                        Dropdown(
                            id=_uid("formatter"),
                            options=[
                                {"label": "str", "value": "str"},
                                {"label": "repr", "value": "repr"},
                            ],
                            value=STATE_DEFAULT["formatter"],
                            clearable=False,
                            className="app-widget",
                        ),
                        H5(children="Decimals"),
                        Slider(
                            id=_uid("decimals"),
                            min=1,
                            max=15,
                            step=1,
                            value=STATE_DEFAULT["decimals"],
                            marks={i + 1: str(i + 1) for i in range(15)},
                            className="app-widget",
                        ),
                        Button(
                            "Copy to Clipboard",
                            id=_uid("copy-to-clipboard-button"),
                            n_clicks=0,
                            style={"width": "100%"},
                        ),
                        Pre(
                            [
                                Code(
                                    id=_uid("primaries-output"),
                                    className="code shell",
                                )
                            ],
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
                        Div(id=_uid("dev-null"), style={"display": "none"}),
                    ],
                ),
            ],
            className="col-6",
        ),
        Div(className="col-2"),
    ],
    className="row",
)
"""
App layout, i.e. :class:`Div` class instance.

LAYOUT : Div
"""


@APP.callback(
    Output(component_id=_uid("primaries-output"), component_property="children"),
    [
        Input(_uid("colourspace"), "value"),
        Input(_uid("illuminant"), "value"),
        Input(_uid("chromatic-adaptation-transform"), "value"),
        Input(_uid("formatter"), "value"),
        Input(_uid("decimals"), "value"),
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
        Output(_uid("colourspace"), "value"),
        Output(_uid("illuminant"), "value"),
        Output(_uid("chromatic-adaptation-transform"), "value"),
        Output(_uid("formatter"), "value"),
        Output(_uid("decimals"), "value"),
    ],
    [
        Input(_uid("url"), "href"),
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

        return STATE_DEFAULT[value.replace("-", "_")]

    state = (
        value_from_query("colourspace"),
        value_from_query("illuminant"),
        value_from_query("chromatic-adaptation-transform"),
        value_from_query("formatter"),
        int(value_from_query("decimals")),
    )

    return state


@APP.callback(
    Output(_uid("url"), "search"),
    [
        Input(_uid("colourspace"), "value"),
        Input(_uid("illuminant"), "value"),
        Input(_uid("chromatic-adaptation-transform"), "value"),
        Input(_uid("formatter"), "value"),
        Input(_uid("decimals"), "value"),
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


APP.clientside_callback(
    f"""
    function(n_clicks) {{
        var primariesOutput = document.getElementById(\
"{_uid('primaries-output')}");
        var content = primariesOutput.textContent;
        navigator.clipboard.writeText(content).then(function() {{
        }}, function() {{
        }});
        return content;
    }}
    """,
    [Output(component_id=_uid("dev-null"), component_property="children")],
    [Input(_uid("copy-to-clipboard-button"), "n_clicks")],
)
