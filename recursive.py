#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

'''
Skeleton of the recursive descent parser. Instead of building an evaluator
you will build the AST.

I have removed a few lines from the recursive descent parser for your benefit.
Please find them and fill them in!

eg. grep for "# FILL THIS IN"
'''

import lexer as lx
from ast import Node

def parse(s, debug=False):
    s = [x for x in lx.Lex(s)] ## s now holds the (token, attribute) "stream"

    def Expr(i):
        ## Expr : Term Expr_
        i, r0 = Term(i)                    # Expr : Term . Expr_
        i, r1 = Expr_(i)                   # Expr : Term Expr_ .
        return i, Node('Expr').addkid(r0).addkid(r1)

    def Expr_(i):
        ## Expr_ : PLUS Term Expr_
        ## Expr_ : DASH Term Expr_
        ## Expr_ : e (the empty string)
        if i >= len(s):                    # Expr_ : e .
            return i, None
        a = s[i]
        if a.type == lx.PLUS:              # Expr_ : PLUS . Term Expr_
            i += 1
            op = '+'
        # FILL THIS IN                     # Expr_ : DASH . Term Expr_
        else:                              # Expr_ : e .
            return i, None
        i, b = Term(i)                     # Expr_ : (PLUS|DASH) Term . Expr_
        i, extra = Expr_(i)                # Expr_ : (PLUS|DASH) Term Expr_ .
        return i, Node('Expr_').addkid(Node(op)).addkid(b).addkid(extra)

    def Term(i):
        ## Term : Factor Term_
        # FILL THIS IN                     # Term : Factor . Term_
        # FILL THIS IN                     # Term : Factor Term_ .
        return i, # FILL THIS IN

    def Term_(i):
        ## Term_ : STAR Factor Term_
        ## Term_ : SLASH Factor Term_
        ## Term_ : e (the empty string)
        # FILL THIS IN                     # Term_ : e .
            # FILL THIS IN

        a = s[i]
        # FILL THIS IN                     # Term_ : STAR . Factor Term_
            # FILL THIS IN
            # FILL THIS IN
        # FILL THIS IN                     # Term_ : SLASH . Factor Term_
            # FILL THIS IN
            # FILL THIS IN
        # FILL THIS IN                     # Term_ : e .
            # FILL THIS IN
        # FILL THIS IN                     # Term_ : (STAR|SLASH) Factor . Term_
        # FILL THIS IN                     # Term_ : (STAR|SLASH) Factor Term_ .
        return i, # FILL THIS IN

    def Factor(i):
        ## Factor : NUMBER
        ## Factor : DASH NUMBER
        ## Factor : LPAREN Expr RPAREN
        a = s[i]
        if a.type == lx.NUMBER:            # Factor : NUMBER .
            i += 1
            r = a.value
        elif a.type == lx.DASH:            # Factor : DASH . NUMBER
            # FILL THIS IN
            # FILL THIS IN
            # FILL THIS IN                 # Factor : DASH NUMBER .
                # FILL THIS IN
                # FILL THIS IN
            else:
                raise SyntaxError
        # FILL THIS IN                     # Factor : LPAREN . Expr RPAREN
            # FILL THIS IN
            # FILL THIS IN                 # Factor : LPAREN Expr . RPAREN
            # FILL THIS IN
            # FILL THIS IN
                # FILL THIS IN
            # FILL THIS IN                 # Factor : LPAREN Expr RPAREN .
        else:
            raise SyntaxError, "Unexpected token %s" % a
        return i, r
    ## ## ## ## ## ## END PARSER ## ## ## ## ## ##

    # This kicks off the parser.
    i, r = Expr(0)

    # If i (the next symbol indicator) does not equal the length of the
    # input then there is unconsumed input.
    if i != len(s):
        raise SyntaxError, "Unconsumed input %s" % (s[i:])
    return r

if __name__ == '__main__':
    print parse('(2+3)*4', True)
