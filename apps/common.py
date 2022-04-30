"""
Common
======
"""

import colour

from colour.hints import ArrayLike, Dict, Integer, Iterable, List

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
]

RGB_COLOURSPACE_OPTIONS: List[Dict] = [
    {"label": key, "value": key}
    for key in sorted(colour.RGB_COLOURSPACES.keys())
    if key not in ("aces", "adobe1998", "prophoto")
]
"""
*RGB* colourspace options for a :class:`Dropdown` class instance.
"""

CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS: List[Dict] = [
    {"label": key, "value": key}
    for key in sorted(colour.CHROMATIC_ADAPTATION_TRANSFORMS.keys())
]
"""
*Chromatic adaptation transform* options for a :class:`Dropdown` class
instance.
"""

ILLUMINANTS_OPTIONS: List[Dict] = [
    {"label": key, "value": key}
    for key in sorted(
        colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"].keys()
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


def nuke_format_matrix(M: ArrayLike, decimals: Integer = 10) -> str:
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

    M = colour.utilities.as_float_array(M)

    def pretty(x: Iterable) -> str:
        """Prettify given number."""

        return " ".join(map(f"{{: 0.{decimals}f}}".format, x))

    tcl = f"{{{pretty(M[0])}}}\n"
    tcl += f"     {{{pretty(M[1])}}}\n"
    tcl += f"     {{{pretty(M[2])}}}"

    return tcl
