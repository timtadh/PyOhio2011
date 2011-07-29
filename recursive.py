#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import lexer as lx
from lexer import Lex

def parse(s):
    s = [x for x in Lex(s)] ## s now holds the (token, attribute) "stream"

    ## I suggest you start reading this code at "def Expr(...)"


    ## ## ## ## ## ## START EXPRESSION EVALUATOR ## ## ## ## ## ##
    def evalop(op, a, b):
        #return op, a, b
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/': return a / b
        raise Exception

    def collapse(a, b):
        print 'collapse>', a, b
        if b is not None:
            a = evalop(b[0], a, b[1])
            print ' '*4, a
            if len(b) == 3:
                print ' '*4, b[2]
                return collapse(a, b[2])
        return a

    def accumulate(op, b, extra):
        print 'accumulate>', op, b, extra
        if extra is not None:
            if len(extra) == 2:
                return op, b, (extra[0], extra[1])
            return op, b, (extra[0], extra[1], extra[2])
        return op, b
    ## ## ## ## ## ## END EXPRESSION EVALUATOR ## ## ## ## ## ##


    ## ## ## ## ## ## START PARSER ## ## ## ## ## ##

    # Notes on the construction of the parser.

    def Expr(i):
        ## Expr : Term Expr_
        i, r0 = Term(i)                    # Expr : Term . Expr_
        i, r1 = Expr_(i)                   # Expr : Term Expr_ .

        print r0, r1
        return i, collapse(r0, r1)

    def Expr_(i):
        ## Expr_ : PLUS Term Expr_
        ## Expr_ : DASH Term Expr_
        ## Expr_ : e (the empty string)
        if i >= len(s): return i, None
        a = s[i]
        if a.type == lx.PLUS:              # Expr_ : PLUS . Term Expr_
            i += 1
            op = '+'
        elif a.type == lx.DASH:            # Expr_ : DASH . Term Expr_
            i += 1
            op = '-'
        else:                              # Expr_ : e .
            return i, None
        i, b = Term(i)                     # Expr_ : (PLUS|DASH) Term . Expr_
        i, extra = Expr_(i)                # Expr_ : (PLUS|DASH) Term Expr_ .
        return i, accumulate(op, b, extra)

    def Term(i):
        ## Term : Factor Term_
        i, r0 = Factor(i)                  # Term : Factor . Term_
        i, r1 = Term_(i)                   # Term : Factor Term_ .

        print r0, r1
        return i, collapse(r0, r1)

    def Term_(i):
        ## Term_ : STAR Factor Term_
        ## Term_ : SLASH Factor Term_
        ## Term_ : e (the empty string)
        if i >= len(s): return i, None
        a = s[i]
        if a.type == lx.STAR:              # Term_ : STAR . Factor Term_
            i += 1
            op = '*'
        elif a.type == lx.SLASH:           # Term_ : SLASH . Factor Term_
            i += 1
            op = '/'
        else:                              # Term_ : e .
            return i, None
        i, b = Factor(i)                   # Term_ : (STAR|SLASH) Factor . Term_
        i, extra = Term_(i)                # Term_ : (STAR|SLASH) Factor Term_ .
        return i, accumulate(op, b, extra)

    def Factor(i):
        ## Factor : NUMBER
        ## Factor : LPAREN Expr RPAREN
        a = s[i]
        if a.type == lx.NUMBER:            # Factor : NUMBER .
            i += 1
            r = a.value
        elif a.type == lx.LPAREN:          # Factor : LPAREN . Expr RPAREN
            i += 1
            i, r = Expr(i)                 # Factor : LPAREN Expr . RPAREN
            a = s[i]
            if a.type != lx.RPAREN:
                raise SyntaxError
            i += 1                         # Factor : LPAREN Expr RPAREN .
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
    print parse('9*(4*(3*2+4))')
