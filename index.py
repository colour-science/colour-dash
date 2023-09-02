"""
Index
=====
"""

import dash
from dash.dependencies import Input, Output
from dash.dcc import Link, Location, Markdown
from dash.html import A, Div, H3, P

import apps.rgb_colourspace_transformation_matrix as app_1
import apps.rgb_colourspace_chromatically_adapted_primaries as app_2
from app import APP, SERVER  # noqa: F401

__author__ = "Colour Developers"
__copyright__ = "Copyright 2018 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = ["load_app"]

APP.layout = Div([Location(id="url", refresh=False), Div(id="apps")])


@APP.callback(Output("apps", "children"), [Input("url", "pathname")])
def load_app(app: dash.Dash):
    """
    Load given app into the appropriate :class:`Div` class instance.

    Parameters
    ----------
    app
        App path.

    Returns
    -------
    :class:`Div`
        :class:`Div` class instance of the app layout.
    """

    if app == app_1.APP_PATH:
        return app_1.LAYOUT
    elif app == app_2.APP_PATH:
        return app_2.LAYOUT
    else:
        return Div(
            [
                P(
                    [
                        "Various colour science ",
                        A(
                            "Dash",
                            href="https://dash.plot.ly/",
                            target="_blank",
                        ),
                        " apps built on top of \n",
                        A(
                            "Colour",
                            href="https://github.com/colour-science/colour",
                            target="_blank",
                        ),
                        ".",
                    ]
                ),
                H3(
                    [
                        Link(
                            app_1.APP_NAME,
                            href=app_1.APP_PATH,
                            className="app-link",
                        )
                    ]
                ),
                Markdown(app_1.APP_DESCRIPTION.replace("This app c", "C")),
                H3(
                    [
                        Link(
                            app_2.APP_NAME,
                            href=app_2.APP_PATH,
                            className="app-link",
                        )
                    ]
                ),
                Markdown(app_2.APP_DESCRIPTION.replace("This app c", "C")),
            ]
        )


if __name__ == "__main__":
    APP.run_server(debug=True)
