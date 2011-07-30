#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

'''
Generates Abstract Syntax Trees (ASTs) using PLY as the parser engine. The AST
generated is from the LALR grammar.
'''

import functools

from ply import yacc
from lexer import TOKENSR, Lex
from ast import Node

## If you are confused about the syntax in this file I recommend reading the
## documentation on the PLY website to see how this compiler compiler's syntax
## works.
class Parser(object):

    tokens = TOKENSR
    precedence = (
    )

    def __new__(cls, **kwargs):
        ## Does magic to allow PLY to do its thing.
        self = super(Parser, cls).__new__(cls)
        self.table = dict()
        self.loc = list()
        self.yacc = yacc.yacc(module=self, tabmodule="lalr_tab", debug=0, **kwargs)
        return self.yacc

    def get_table(self):
        c = self.table
        for s in self.loc:
            c = self.table[c]
        return c

    def p_Expr1(self, t):
        'Expr : Expr PLUS Term'
        t[0] = t[1] + t[3]

    def p_Expr2(self, t):
        'Expr : Expr DASH Term'
        t[0] = t[1] - t[3]

    def p_Expr3(self, t):
        'Expr : Term'
        t[0] = t[1]

    def p_Term1(self, t):
        'Term : Term STAR Factor'
        t[0] = t[1] * t[3]

    def p_Term2(self, t):
        'Term : Term SLASH Factor'
        t[0] = t[1] / t[3]

    def p_Term3(self, t):
        'Term : Factor'
        t[0] = t[1]

    def p_Factor1(self, t):
        'Factor : NUMBER '
        t[0] = t[1]

    def p_Factor2(self, t):
        'Factor : DASH NUMBER'
        t[0] = -1 * t[2]

    def p_Factor3(self, t):
        'Factor : LPAREN Expr RPAREN '
        t[0] = t[2]

    def p_error(self, t):
        raise SyntaxError, "An error occured at %s" % str(t)

parse = functools.partial(Parser().parse, lexer=Lex)

if __name__ == '__main__':
    def test(expr):
        p = parse(expr)
        assert eval(expr) == p
        print p
    test('(-2+3)*4')
