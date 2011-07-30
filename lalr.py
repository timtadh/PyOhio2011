#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

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

    def p_Start(self, t):
        '''
        Expr : Expr PLUS Term
        Expr : Expr DASH Term
        Expr : Term
        Term : Term STAR Factor
        Term : Term SLASH Factor
        Term : Factor
        Factor : NUMBER
        Factor : DASH NUMBER
        Factor : LPAREN Expr RPAREN
        '''

        #Expr : Term Expr_
        #Expr_ : PLUS Term Expr_
        #Expr_ : DASH Term Expr_
        #Expr_ :
        #Term : Factor Term_
        #Term_ : STAR Factor Term_
        #Term_ : SLASH Factor Term_
        #Term_ :
        #Factor : NUMBER
        #Factor : DASH NUMBER
        #Factor : LPAREN Expr RPAREN
        t[0] = [x for x in t[1:]]
        print t[0]

parse = functools.partial(Parser().parse, lexer=Lex)

if __name__ == '__main__':
    def test(expr):
        p = parse(expr)
    test('(2+3)*4')
