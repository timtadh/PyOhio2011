#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

'''
Skeleton of the LALR parser. Instead of building an evaluator you will build the
AST.

I have removed a few lines from the recursive descent parser for your benefit.
Please find them and fill them in!

eg. grep for "# FILL THIS IN"
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
        t[0] = Node('Expr').addkid(
            Node('+')
                .addkid(t[1])
                .addkid(t[3])
        )

    def p_Expr2(self, t):
        'Expr : Expr DASH Term'
        # FILL THIS IN
            # FILL THIS IN
                # FILL THIS IN
                # FILL THIS IN
        # FILL THIS IN

    def p_Expr3(self, t):
        # FILL THIS IN
        # FILL THIS IN

    ## COMPLETE THE PARSER BY ADDING THE REST OF THE PRODUCTIONS
    ## For your convience one projection has been completed for you!

    #Term : Term STAR Factor
    #Term : Term SLASH Factor
    #Term : Factor
    #Factor : NUMBER
    #Factor : DASH NUMBER ----------> Already implemented in def p_Factor2(...)
    #Factor : LPAREN Expr RPAREN

    def p_Factor2(self, t):
        'Factor : DASH NUMBER'
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
