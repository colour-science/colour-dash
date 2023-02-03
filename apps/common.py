"""
Common
======
"""

from io import StringIO
from colour.adaptation import CHROMATIC_ADAPTATION_TRANSFORMS
from colour.colorimetry import CCS_ILLUMINANTS
from colour.io import LUTOperatorMatrix, write_LUT_SonySPImtx
from colour.models import RGB_COLOURSPACES
from colour.utilities import as_float_array

from colour.hints import ArrayLike, Dict, Iterable, List

__author__ = "Colour Developers"
__copyright__ = "Copyright 2018 Colour Developers"
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "RGB_COLOURSPACE_OPTIONS",
    "CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS",
    "ILLUMINANTS_OPTIONS",
    "NUKE_COLORMATRIX_NODE_TEMPLATE",
    "nuke_format_matrix",
    "spimtx_format_matrix",
]

RGB_COLOURSPACE_OPTIONS: List[Dict] = [
    {"label": key, "value": key}
    for key in sorted(RGB_COLOURSPACES.keys())
    if key not in ("aces", "adobe1998", "prophoto")
]
"""
*RGB* colourspace options for a :class:`Dropdown` class instance.
"""

CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS: List[Dict] = [
    {"label": key, "value": key}
    for key in sorted(CHROMATIC_ADAPTATION_TRANSFORMS.keys())
]
"""
*Chromatic adaptation transform* options for a :class:`Dropdown` class
instance.
"""

ILLUMINANTS_OPTIONS: List[Dict] = [
    {"label": key, "value": key}
    for key in sorted(
        CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"].keys()
    )
]
"""
*CIE 1931 2 Degree Standard Observer* illuminant options for a
:class:`Dropdown`class instance.
"""

NUKE_COLORMATRIX_NODE_TEMPLATE: str = """
ColorMatrix {{
 inputs 0
 matrix {{
     {0}
   }}
 name "{1}"
 selected true
 xpos 0
 ypos 0
}}"""[
    1:
]
"""
*The Foundry Nuke* *ColorMatrix* node template.
"""


def nuke_format_matrix(M: ArrayLike, decimals: int = 10) -> str:
    """
    Format given matrix for usage in *The Foundry Nuke*, i.e. *TCL* code for
    a *ColorMatrix* node.

    Parameters
    ----------
    M
        Matrix to format.
    decimals
        Decimals to use when formatting the matrix.

    Returns
    -------
    :class:`str`
        *The Foundry Nuke* formatted matrix.
    """

    M = as_float_array(M)

    def pretty(x: Iterable) -> str:
        """Prettify given number."""

        return " ".join(map(f"{{: 0.{decimals}f}}".format, x))

    tcl = f"{{{pretty(M[0])}}}\n"
    tcl += f"     {{{pretty(M[1])}}}\n"
    tcl += f"     {{{pretty(M[2])}}}"

    return tcl


def spimtx_format_matrix(M: ArrayLike, decimals: int = 10) -> str:
    """
    Format given matrix as a *Sony* *.spimtx* *LUT* formatted matrix.

    Parameters
    ----------
    M
        Matrix to format.
    decimals
        Decimals to use when formatting the matrix.

    Returns
    -------
    :class:`str`
        *Sony* *.spimtx* *LUT* formatted matrix.
    """

    string = StringIO()

    write_LUT_SonySPImtx(LUTOperatorMatrix(M), string, decimals)

    return string.getvalue()
