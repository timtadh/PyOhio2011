#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import lexer as lx
from lexer import Lex

def parse(s, debug=False):
    s = [x for x in Lex(s)] ## s now holds the (token, attribute) "stream"

    ## I suggest you start reading this code at "def Expr(...)"


    ## ## ## ## ## ## START EXPRESSION EVALUATOR ## ## ## ## ## ##
    def evalop(op, a, b):
        if debug: print 'evalop>', op, a, b
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/': return a / b
        raise Exception

    def collapse(a, b):
        if debug: print 'collapse>', a, b
        if b is not None:
            a = evalop(b[0], a, b[1])
            if debug: print ' '*4, 'evalop result>', a
            if len(b) == 3:
                if debug: print ' '*4, b[2]
                return collapse(a, b[2])
        if debug: print ' '*4, 'collapse result>', a
        return a

    def accumulate(op, b, extra):
        if debug: print 'accumulate>', op, b, extra
        if extra is not None:
            if len(extra) == 2:
                return op, b, (extra[0], extra[1])
            return op, b, (extra[0], extra[1], extra[2])
        return op, b
    ## ## ## ## ## ## END EXPRESSION EVALUATOR ## ## ## ## ## ##


    ## ## ## ## ## ## START PARSER ## ## ## ## ## ##

    #      #      #      #      #      #      #      #      #      #      #
    #
    # Notes on the construction of the parser.
    #
    # Each function models a production of the formal grammar of the
    # language as found in grammar.md. The signature of the each
    # function is the same ie.
    #
    #     def ProductionName(i): returns i_out, r
    #         @i = the index of the next token to consider (before the
    #              production has been processed).
    #         @i_out = the index of the next token to consider (after
    #                  the production has been processed) its value
    #                  reflects the input consumed by the production.
    #         @r = the return value to be passed to the parent.
    #
    # This parser does not produce an AST or any intermediate language.
    # Instead, it evaluates the language in place a produces the result
    # of the arithmetic expression. It is not necessary to understand
    # this process, but the interested can read the code contained in
    # `evalop`, `collapse`, and `accumulate`.
    #
    #      #      #      #      #      #      #      #      #      #      #

    ## NB. Sorry about the gratuitous print statement messing up the
    ## readability of the code. I wanted to make the execution of the
    ## parser understandable at run time. Go to an eariler version of
    ## this file to see the "clean" version.

    def Expr(i):
        ## Expr : Term Expr_
        if debug: print 'Expr : . Term Expr_'
        i, r0 = Term(i)                    # Expr : Term . Expr_
        if debug: print 'Expr : Term . Expr_'
        i, r1 = Expr_(i)                   # Expr : Term Expr_ .
        if debug: print 'Expr : Term Expr_ .'
        return i, collapse(r0, r1)

    def Expr_(i):
        ## Expr_ : PLUS Term Expr_
        ## Expr_ : DASH Term Expr_
        ## Expr_ : e (the empty string)
        if i >= len(s):                    # Expr_ : e .
            if debug: print 'Expr_ : e .'
            return i, None
        a = s[i]
        if a.type == lx.PLUS:              # Expr_ : PLUS . Term Expr_
            if debug: print 'Expr_ : PLUS . Term Expr_'
            i += 1
            op = '+'
        elif a.type == lx.DASH:            # Expr_ : DASH . Term Expr_
            if debug: print 'Expr_ : DASH . Term Expr_'
            i += 1
            op = '-'
        else:                              # Expr_ : e .
            if debug: print 'Expr_ : e .'
            return i, None
        i, b = Term(i)                     # Expr_ : (PLUS|DASH) Term . Expr_
        if debug: print 'Expr_ : (PLUS|DASH) Term . Expr_'
        i, extra = Expr_(i)                # Expr_ : (PLUS|DASH) Term Expr_ .
        if debug: print 'Expr_ : (PLUS|DASH) Term Expr_ .'
        return i, accumulate(op, b, extra)

    def Term(i):
        ## Term : Factor Term_
        if debug: print 'Term : . Factor Term_'
        i, r0 = Factor(i)                  # Term : Factor . Term_
        if debug: print 'Term : Factor . Term_'
        i, r1 = Term_(i)                   # Term : Factor Term_ .
        if debug: print 'Term : Factor Term_ .'
        return i, collapse(r0, r1)

    def Term_(i):
        ## Term_ : STAR Factor Term_
        ## Term_ : SLASH Factor Term_
        ## Term_ : e (the empty string)
        if i >= len(s):                    # Term_ : e .
            if debug: print 'Term_ : e .'
            return i, None
        a = s[i]
        if a.type == lx.STAR:              # Term_ : STAR . Factor Term_
            if debug: print 'Term_ : STAR . Factor Term_'
            i += 1
            op = '*'
        elif a.type == lx.SLASH:           # Term_ : SLASH . Factor Term_
            if debug: print 'Term_ : SLASH . Factor Term_'
            i += 1
            op = '/'
        else:                              # Term_ : e .
            if debug: print 'Term_ : e .'
            return i, None
        i, b = Factor(i)                   # Term_ : (STAR|SLASH) Factor . Term_
        if debug: print 'Term_ : (STAR|SLASH) Factor . Term_'
        i, extra = Term_(i)                # Term_ : (STAR|SLASH) Factor Term_ .
        if debug: print 'Term_ : (STAR|SLASH) Factor Term_ .'
        return i, accumulate(op, b, extra)

    def Factor(i):
        ## Factor : NUMBER
        ## Factor : DASH NUMBER
        ## Factor : LPAREN Expr RPAREN
        a = s[i]
        if a.type == lx.NUMBER:            # Factor : NUMBER .
            i += 1
            r = a.value
            if debug: print 'Factor : NUMBER .'
        elif a.type == lx.DASH:            # Factor : DASH . NUMBER
            if debug: print 'Factor : DASH . NUMBER'
            i += 1
            a = s[i]
            if a.type == lx.NUMBER:        # Factor : DASH NUMBER .
                if debug: print 'Factor : DASH NUMBER .'
                i += 1
                r = -1 * a.value
            else:
                raise SyntaxError
        elif a.type == lx.LPAREN:          # Factor : LPAREN . Expr RPAREN
            i += 1
            if debug: print 'Factor : LPAREN . Expr RPAREN'
            i, r = Expr(i)                 # Factor : LPAREN Expr . RPAREN
            if debug: print 'Factor : LPAREN Expr . RPAREN'
            a = s[i]
            if a.type != lx.RPAREN:
                raise SyntaxError
            i += 1                         # Factor : LPAREN Expr RPAREN .
            if debug: print 'Factor : LPAREN Expr RPAREN .'
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
