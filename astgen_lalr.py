#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

'''
Generates Abstract Syntax Trees (ASTs) using PLY as the the parser engine. It
generates the syntax trees based on the LALR grammar.
'''

import sys, functools

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
        self.yacc = yacc.yacc(module=self, tabmodule="lalr_tab", debug=0, **kwargs)
        return self.yacc

    def p_Expr1(self, t):
        'Expr : Expr PLUS Term'
        t[0] = Node('Expr').addkid(
            Node('+')
                .addkid(t[1])
                .addkid(t[3])
        )

    def p_Expr2(self, t):
        'Expr : Expr DASH Term'
        t[0] = Node('Expr').addkid(
            Node('-')
                .addkid(t[1])
                .addkid(t[3])
        )

    def p_Expr3(self, t):
        'Expr : Term'
        t[0] = Node('Expr').addkid(t[1])

    def p_Term1(self, t):
        'Term : Term STAR Factor'
        t[0] = Node('Term').addkid(
            Node('*')
                .addkid(t[1])
                .addkid(t[3])
        )

    def p_Term2(self, t):
        'Term : Term SLASH Factor'
        t[0] = Node('Term').addkid(
            Node('/')
                .addkid(t[1])
                .addkid(t[3])
        )

    def p_Term3(self, t):
        'Term : Factor'
        t[0] = Node('Term').addkid(t[1])

    def p_Factor1(self, t):
        'Factor : NUMBER '
        t[0] = Node('Factor').addkid(t[1])

    def p_Factor2(self, t):
        'Factor : DASH NUMBER'
        t[0] = Node('Factor').addkid(t[2])

    def p_Factor3(self, t):
        'Factor : LPAREN Expr RPAREN '
        t[0] = Node('Factor').addkid(t[2])

    def p_error(self, t):
        raise SyntaxError, "An error occured at %s" % str(t)

parse = functools.partial(Parser().parse, lexer=Lex)

if __name__ == '__main__':
    def test(expr):
        p = parse(expr)
        print p.dotty()
    print >>sys.stderr, 'expression: ',
    test(raw_input())
