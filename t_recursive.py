#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from recursive import parse

def t_expr_compound():
    assert (4*3/2) == parse('4*3/2')
    assert (4/2*3) == parse('4/2*3')
    assert ((3+9)*4/8) == parse('(3+9)*4/8')
    assert (((9-3)*(5-3))/2 + 2) == parse('((9-3)*(5-3))/2 + 2')
    assert (5 * 4 / 2 - 10 + 5 - 2 + 3) == parse('5 * 4 / 2 - 10 + 5 - 2 + 3')
    assert (5 / 4 * 2 + 10 - 5 * 2 / 3) == parse('5 / 4 * 2 + 10 - 5 * 2 / 3')
