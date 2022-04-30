"""
RGB Colourspace Transformation Matrix Application
=================================================
"""

import urllib.parse
import re
import sys
from dash.dcc import Dropdown, Link, Markdown, Slider
from dash.dependencies import Input, Output
from dash.html import A, Code, Div, H3, H5, Li, Pre, Ul

import colour
from colour.hints import Integer

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
    "LAYOUT",
    "set_RGB_to_RGB_matrix_output",
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

APP_UID: str = hash(APP_NAME)
"""
App unique id.
"""

LAYOUT: Div = Div(
    [
        H3([Link(APP_NAME, href=APP_PATH)], className="text-center"),
        Div(
            [
                Markdown(APP_DESCRIPTION),
                H5(children="Input Colourspace"),
                Dropdown(
                    id=f"input-colourspace-{APP_UID}",
                    options=RGB_COLOURSPACE_OPTIONS,
                    value=RGB_COLOURSPACE_OPTIONS[0]["value"],
                    clearable=False,
                    className="app-widget",
                ),
                H5(children="Output Colourspace"),
                Dropdown(
                    id=f"output-colourspace-{APP_UID}",
                    options=RGB_COLOURSPACE_OPTIONS,
                    value=RGB_COLOURSPACE_OPTIONS[0]["value"],
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
                        {"label": "Nuke", "value": "Nuke"},
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
                                        SERVER_URL, APP_PATH
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
    decimals: Integer,
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

    M = colour.matrix_RGB_to_RGB(
        colour.RGB_COLOURSPACES[input_colourspace],
        colour.RGB_COLOURSPACES[output_colourspace],
        chromatic_adaptation_transform,
    )

    with colour.utilities.numpy_print_options(
        formatter={"float": f"{{: 0.{decimals}f}}".format},
        threshold=sys.maxsize,
    ):
        if formatter == "str":
            M = str(M)
        elif formatter == "repr":
            M = repr(M)
        else:

            def slugify(string: str) -> str:
                """Slugify given string for *Nuke*."""

                string = string.replace("+", "_Plus")
                pattern = r"\(|\)"
                string = re.sub(pattern, "", string)
                pattern = r"\s-\s|\s|-|\.|/"
                string = re.sub(pattern, "_", string)
                return string

            M = NUKE_COLORMATRIX_NODE_TEMPLATE.format(
                nuke_format_matrix(M, decimals),
                (
                    f"{slugify(input_colourspace)}"
                    f"__to__"
                    f"{slugify(output_colourspace)}"
                ),
            )
        return M
