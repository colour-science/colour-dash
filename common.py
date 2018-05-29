# -*- coding: utf-8 -*-
"""
Common
======
"""

from __future__ import division, unicode_literals

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['NUKE_COLORMATRIX_NODE_TEMPLATE', 'nuke_format_matrix']

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


def nuke_format_matrix(M, decimals=10):
    pretty = lambda x: ' '.join(map('{{:0.{0}f}}'.format(decimals).format, x))

    tcl = '{{{0}}}\n'.format(pretty(M[0]))
    tcl += '     {{{0}}}\n'.format(pretty(M[1]))
    tcl += '     {{{0}}}'.format(pretty(M[2]))

    return tcl
