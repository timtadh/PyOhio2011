#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import lexer as lx
from lexer import Lex

def parse(s):
    s = [x for x in Lex(s)] ## s now holds the (token, attribute) "stream"


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
    def Expr(i):
        i, r0 = Term(i)
        i, r1 = Expr_(i)

        print r0, r1
        return i, collapse(r0, r1)

    def Expr_(i):
        if i >= len(s): return i, None
        a = s[i]
        if a.type == lx.PLUS:
            i += 1
            op = '+'
        elif a.type == lx.DASH:
            i += 1
            op = '-'
        else:
            return i, None
        i, b = Term(i)
        i, extra = Expr_(i)
        return i, accumulate(op, b, extra)

    def Term(i):
        i, r0 = Factor(i)
        i, r1 = Term_(i)

        print r0, r1
        return i, collapse(r0, r1)

    def Term_(i):
        if i >= len(s): return i, None
        a = s[i]
        if a.type == lx.STAR:
            i += 1
            op = '*'
        elif a.type == lx.SLASH:
            i += 1
            op = '/'
        else:
            return i, None
        i, b = Factor(i)
        i, extra = Term_(i)
        return i, accumulate(op, b, extra)

    def Factor(i):
        a = s[i]
        if a.type == lx.NUMBER:
            i += 1
            r = a.value
        elif a.type == lx.LPAREN:
            i += 1
            i, r = Expr(i)
            a = s[i]
            if a.type != lx.RPAREN:
                raise SyntaxError
            i += 1
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
