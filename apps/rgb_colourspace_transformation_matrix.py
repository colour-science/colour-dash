"""
RGB Colourspace Transformation Matrix Application
=================================================
"""

import urllib.parse
import re
import sys
from contextlib import suppress
from dash.dcc import Dropdown, Location, Link, Markdown, Slider
from dash.dependencies import Input, Output
from dash.html import A, Code, Div, H3, H5, Li, Pre, Ul
from urllib.parse import parse_qs, urlencode, urlparse

from colour.models import RGB_COLOURSPACES, matrix_RGB_to_RGB
from colour.utilities import numpy_print_options

from app import APP, SERVER_URL
from apps.common import (
    CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS,
    NUKE_COLORMATRIX_NODE_TEMPLATE,
    RGB_COLOURSPACE_OPTIONS,
    nuke_format_matrix,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2018 Colour Developers"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "APP_NAME",
    "APP_NAME",
    "APP_DESCRIPTION",
    "APP_UID",
    "DEFAULT_STATE",
    "LAYOUT",
    "set_RGB_to_RGB_matrix_output",
    "update_state_on_url_query_change",
    "update_url_query_on_state_change",
]

APP_NAME: str = "RGB Colourspace Transformation Matrix"
"""
App name.
"""

APP_PATH: str = f"/apps/{__name__.split('.')[-1]}"
"""
App path, i.e. app url.
"""

APP_DESCRIPTION: str = (
    "This app computes the colour transformation "
    "matrix from the *Input RGB Colourspace* to the "
    "*Output RGB Colourspace* using the given "
    "*Chromatic Adaptation Transform*."
)
"""
App description.
"""

APP_UID: int = hash(APP_NAME)
"""
App unique id.
"""

DEFAULT_STATE = {
    "input_colourspace": RGB_COLOURSPACE_OPTIONS[0]["value"],
    "output_colourspace": RGB_COLOURSPACE_OPTIONS[0]["value"],
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
                H5(children="Input Colourspace"),
                Dropdown(
                    id=f"input-colourspace-{APP_UID}",
                    options=RGB_COLOURSPACE_OPTIONS,
                    value=DEFAULT_STATE["input_colourspace"],
                    clearable=False,
                    className="app-widget",
                ),
                H5(children="Output Colourspace"),
                Dropdown(
                    id=f"output-colourspace-{APP_UID}",
                    options=RGB_COLOURSPACE_OPTIONS,
                    value=DEFAULT_STATE["output_colourspace"],
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
                        {"label": "Nuke", "value": "Nuke"},
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
                    [
                        Code(
                            id=f"RGB-transformation-matrix-{APP_UID}",
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
    Output(
        component_id=f"RGB-transformation-matrix-{APP_UID}",
        component_property="children",
    ),
    [
        Input(f"input-colourspace-{APP_UID}", "value"),
        Input(f"output-colourspace-{APP_UID}", "value"),
        Input(f"chromatic-adaptation-transform-{APP_UID}", "value"),
        Input(f"formatter-{APP_UID}", "value"),
        Input(f"decimals-{APP_UID}", "value"),
    ],
)
def set_RGB_to_RGB_matrix_output(
    input_colourspace: str,
    output_colourspace: str,
    chromatic_adaptation_transform: str,
    formatter: str,
    decimals: int,
) -> str:
    """
    Compute and write the colour transformation matrix from given input *RGB*
    colourspace to the output *RGB* colourspace using given
    *chromatic adaptation transform* into the output :class:`Pre` class
    instance.

    Parameters
    ----------
    input_colourspace
        Input *RGB* colourspace.
    output_colourspace
        Output *RGB* colourspace.
    chromatic_adaptation_transform
        *Chromatic adaptation transform* to use.
    formatter
        Formatter to use, :func:`str`, :func:`repr` or *Nuke*.
    decimals
        Decimals to use when formatting the colour transformation matrix.

    Returns
    -------
    :class:`str`
        Colour transformation matrix.
    """

    M = matrix_RGB_to_RGB(
        RGB_COLOURSPACES[input_colourspace],
        RGB_COLOURSPACES[output_colourspace],
        chromatic_adaptation_transform,
    )

    with numpy_print_options(
        formatter={"float": f"{{: 0.{decimals}f}}".format},
        threshold=sys.maxsize,
    ):
        if formatter == "str":
            M_f = str(M)
        elif formatter == "repr":
            M_f = repr(M)
        else:

            def slugify(string: str) -> str:
                """Slugify given string for *Nuke*."""

                string = string.replace("+", "_Plus")
                pattern = r"\(|\)"
                string = re.sub(pattern, "", string)
                pattern = r"\s-\s|\s|-|\.|/"
                string = re.sub(pattern, "_", string)
                return string

            M_f = NUKE_COLORMATRIX_NODE_TEMPLATE.format(
                nuke_format_matrix(M, decimals),
                (
                    f"{slugify(input_colourspace)}"
                    f"__to__"
                    f"{slugify(output_colourspace)}"
                ),
            )

        return M_f


@APP.callback(
    [
        Output(f"input-colourspace-{APP_UID}", "value"),
        Output(f"output-colourspace-{APP_UID}", "value"),
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
        value_from_query("input-colourspace"),
        value_from_query("output-colourspace"),
        value_from_query("chromatic-adaptation-transform"),
        value_from_query("formatter"),
        int(value_from_query("decimals")),
    )

    return state


@APP.callback(
    Output(f"url-{APP_UID}", "search"),
    [
        Input(f"input-colourspace-{APP_UID}", "value"),
        Input(f"output-colourspace-{APP_UID}", "value"),
        Input(f"chromatic-adaptation-transform-{APP_UID}", "value"),
        Input(f"formatter-{APP_UID}", "value"),
        Input(f"decimals-{APP_UID}", "value"),
    ],
)
def update_url_query_on_state_change(
    input_colourspace: str,
    output_colourspace: str,
    chromatic_adaptation_transform: str,
    formatter: str,
    decimals: int,
) -> str:
    """
    Update the URL query on App state change.

    Parameters
    ----------
    input_colourspace
        Input *RGB* colourspace.
    output_colourspace
        Output *RGB* colourspace.
    chromatic_adaptation_transform
        *Chromatic adaptation transform* to use.
    formatter
        Formatter to use, :func:`str`, :func:`repr` or *Nuke*.
    decimals
        Decimals to use when formatting the colour transformation matrix.

    Returns
    -------
    :class:`str`
        Url query.
    """

    query = urlencode(
        {
            "input-colourspace": input_colourspace,
            "output-colourspace": output_colourspace,
            "chromatic-adaptation-transform": chromatic_adaptation_transform,
            "formatter": formatter,
            "decimals": decimals,
        }
    )

    return f"?{query}"
