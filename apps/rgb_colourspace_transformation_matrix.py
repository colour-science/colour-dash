"""
RGB Colourspace Transformation Matrix Application
=================================================
"""

import re
import sys
import urllib.parse
from contextlib import suppress
from urllib.parse import parse_qs, urlencode, urlparse

from colour.models import RGB_COLOURSPACES, matrix_RGB_to_RGB
from colour.utilities import numpy_print_options
from dash.dcc import Dropdown, Link, Location, Markdown, Slider
from dash.dependencies import Input, Output
from dash.html import H3, H5, A, Button, Code, Div, Li, Pre, Ul

from app import APP, SERVER_URL
from apps.common import (
    OPTIONS_CHROMATIC_ADAPTATION_TRANSFORM,
    OPTIONS_RGB_COLOURSPACE,
    TEMPLATE_NUKE_NODE_COLORMATRIX,
    TEMPLATE_OCIO_COLORSPACE,
    matrix_3x3_to_4x4,
    nuke_format_matrix,
    spimtx_format_matrix,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2018 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "APP_NAME",
    "APP_NAME",
    "APP_DESCRIPTION",
    "APP_UID",
    "STATE_DEFAULT",
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
App path, i.e., app url.
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


def _uid(id_):
    """
    Generate a unique id for given id by appending the application *UID*.
    """

    return f"{id_}-{APP_UID}"


STATE_DEFAULT = {
    "input_colourspace": OPTIONS_RGB_COLOURSPACE[0]["value"],
    "output_colourspace": OPTIONS_RGB_COLOURSPACE[0]["value"],
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
                        H5(children="Input Colourspace"),
                        Dropdown(
                            id=_uid("input-colourspace"),
                            options=OPTIONS_RGB_COLOURSPACE,
                            value=STATE_DEFAULT["input_colourspace"],
                            clearable=False,
                            className="app-widget",
                        ),
                        H5(children="Output Colourspace"),
                        Dropdown(
                            id=_uid("output-colourspace"),
                            options=OPTIONS_RGB_COLOURSPACE,
                            value=STATE_DEFAULT["output_colourspace"],
                            clearable=False,
                            className="app-widget",
                        ),
                        H5(children="Chromatic Adaptation Transform"),
                        Dropdown(
                            id=_uid("chromatic-adaptation-transform"),
                            options=[
                                *OPTIONS_CHROMATIC_ADAPTATION_TRANSFORM,
                                {"label": "None", "value": "None"},
                            ],
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
                                {"label": "Nuke", "value": "nuke"},
                                {
                                    "label": "OpenColorIO",
                                    "value": "opencolorio",
                                },
                                {"label": "Spimtx", "value": "spimtx"},
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
                                    id=_uid(
                                        "rgb-colourspace-transformation-matrix-output"
                                    ),
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
            className="col-8",
        ),
        Div(className="col-2"),
    ],
    className="row",
)
"""
App layout, i.e., :class:`Div` class instance.

LAYOUT : Div
"""


@APP.callback(
    Output(
        component_id=_uid("rgb-colourspace-transformation-matrix-output"),
        component_property="children",
    ),
    [
        Input(_uid("input-colourspace"), "value"),
        Input(_uid("output-colourspace"), "value"),
        Input(_uid("chromatic-adaptation-transform"), "value"),
        Input(_uid("formatter"), "value"),
        Input(_uid("decimals"), "value"),
    ],
)
def set_RGB_to_RGB_matrix_output(
    input_colourspace: str,
    output_colourspace: str,
    chromatic_adaptation_transform: str | None,
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

    chromatic_adaptation_transform = (
        None
        if chromatic_adaptation_transform == "None"
        else chromatic_adaptation_transform
    )

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
        elif formatter == "nuke":

            def slugify(string: str) -> str:
                """Slugify given string for *Nuke*."""

                string = string.replace("+", "_Plus")
                pattern = r"\(|\)"
                string = re.sub(pattern, "", string)
                pattern = r"\s-\s|\s|-|\.|/"
                string = re.sub(pattern, "_", string)
                return string

            M_f = TEMPLATE_NUKE_NODE_COLORMATRIX.format(
                name=(
                    f"{slugify(input_colourspace)}"
                    f"__to__"
                    f"{slugify(output_colourspace)}"
                ),
                matrix=nuke_format_matrix(M, decimals),
            )
        elif formatter == "opencolorio":
            M_f = TEMPLATE_OCIO_COLORSPACE.format(
                name=output_colourspace,
                input_colourspace=input_colourspace,
                output_colourspace=output_colourspace,
                matrix=re.sub(
                    r"\s+",
                    " ",
                    repr(matrix_3x3_to_4x4(M))
                    .replace("array(", "")
                    .replace("[ ", "[")
                    .replace(")", "")
                    .replace("\n", ""),
                ),
            )

        elif formatter == "spimtx":
            M_f = spimtx_format_matrix(M, decimals)

        return M_f


@APP.callback(
    [
        Output(_uid("input-colourspace"), "value"),
        Output(_uid("output-colourspace"), "value"),
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
        value_from_query("input-colourspace"),
        value_from_query("output-colourspace"),
        value_from_query("chromatic-adaptation-transform"),
        value_from_query("formatter"),
        int(value_from_query("decimals")),
    )

    return state


@APP.callback(
    Output(_uid("url"), "search"),
    [
        Input(_uid("input-colourspace"), "value"),
        Input(_uid("output-colourspace"), "value"),
        Input(_uid("chromatic-adaptation-transform"), "value"),
        Input(_uid("formatter"), "value"),
        Input(_uid("decimals"), "value"),
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


APP.clientside_callback(
    f"""
    function(n_clicks) {{
        var rgbColourspaceTransformationMatrixOutput = document.getElementById(\
"{_uid('rgb-colourspace-transformation-matrix-output')}");
        var content = rgbColourspaceTransformationMatrixOutput.textContent;
        navigator.clipboard.writeText(content).then(function() {{
        }}, function() {{
        }});
        return content;
    }}
    """,
    [Output(component_id=_uid("dev-null"), component_property="children")],
    [Input(_uid("copy-to-clipboard-button"), "n_clicks")],
)
