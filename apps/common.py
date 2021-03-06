# -*- coding: utf-8 -*-
"""
Common
======
"""

import colour

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2018-2021 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'RGB_COLOURSPACE_OPTIONS', 'CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS',
    'ILLUMINANTS_OPTIONS', 'NUKE_COLORMATRIX_NODE_TEMPLATE',
    'nuke_format_matrix'
]

RGB_COLOURSPACE_OPTIONS = [{
    'label': key,
    'value': key
} for key in sorted(colour.RGB_COLOURSPACES.keys())
                           if key not in ('aces', 'adobe1998', 'prophoto')]
"""
*RGB* colourspace options for a :class:`Dropdown` class instance.

RGB_COLOURSPACE_OPTIONS : list
"""

CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS = [{
    'label': key,
    'value': key
} for key in sorted(colour.CHROMATIC_ADAPTATION_TRANSFORMS.keys())]
"""
*Chromatic adaptation transform* options for a :class:`Dropdown` class
instance.

CHROMATIC_ADAPTATION_TRANSFORM_OPTIONS : list
"""

ILLUMINANTS_OPTIONS = [{
    'label': key,
    'value': key
} for key in sorted(colour.CCS_ILLUMINANTS[
    'CIE 1931 2 Degree Standard Observer'].keys())]
"""
*CIE 1931 2 Degree Standard Observer* illuminant options for a
:class:`Dropdown`class instance.

ILLUMINANTS_OPTIONS : list
"""

NUKE_COLORMATRIX_NODE_TEMPLATE = """
ColorMatrix {{
 inputs 0
 matrix {{
     {0}
   }}
 name "{1}"
 selected true
 xpos 0
 ypos 0
}}""" [1:]
"""
*The Foundry Nuke* *ColorMatrix* node template.

NUKE_COLORMATRIX_NODE_TEMPLATE : unicode
"""


def nuke_format_matrix(M, decimals=10):
    """
    Formats given matrix for usage in *The Foundry Nuke*, i.e. *TCL* code for
    a *ColorMatrix* node.

    Parameters
    ----------
    M : array_like
        Matrix to format.
    decimals : int, optional
        Decimals to use when formatting the matrix.

    Returns
    -------
    unicode
        *The Foundry Nuke* formatted matrix.
    """

    def pretty(x):
        """
        Prettify given number.
        """

        return ' '.join(map('{{: 0.{0}f}}'.format(decimals).format, x))

    tcl = '{{{0}}}\n'.format(pretty(M[0]))
    tcl += '     {{{0}}}\n'.format(pretty(M[1]))
    tcl += '     {{{0}}}'.format(pretty(M[2]))

    return tcl
