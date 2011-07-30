#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

'''
Implements an evaluator for the arithmetic language defined in grammar.md. It uses
PyTDPP as the parser engine.
'''


import lexer as lx
from pytdpp.parser import BaseParser

# This class subclasses the BaseParser from the Top Down Predictive Parser module. The
# base class implements the actual parsing algorithm. You only need to write the LL(1)
# grammar and parsing actions. In this case I interleaved some of the productions to
# simplify the actions.

class Parser(BaseParser):

    tokens = lx.TOKENSR

    def evalop(self, op, a, b):
        #return op, a, b
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/': return a / b
        raise Exception

    @BaseParser.production("Start : Expr")
    def Start(self, start, expr):
        return expr

    @BaseParser.production("Term : Factor Term'")
    @BaseParser.production("Expr : Term Expr'")
    def ExprTerm(self, expr_, b, extra):
        if extra is not None:
            b = self.evalop(extra[0], b, extra[1])
            if len(extra) == 3:
                return self.ExprTerm(None, b, extra[2])
        return b

    @BaseParser.productions('''
        Expr' : DASH Term Expr';
        Expr' : PLUS Term Expr';
        Term' : SLASH Factor Term';
        Term' : STAR Factor Term';   ''')
    def Op(self, nt, op, b, extra):
        #print 'op>', op, b, extra
        if extra is not None:
            if len(extra) == 2:
                return op.value, b, (extra[0], extra[1])
            return op.value, b, (extra[0], extra[1], extra[2])
        return op.value, b

    @BaseParser.production("Term' : e")
    @BaseParser.production("Expr' : e")
    def Empty(self, *args): pass

    @BaseParser.production("Factor : NUMBER")
    def Factor1(self, factor, number):
        return number.value

    @BaseParser.production("Factor : DASH NUMBER")
    def Factor2(self, factor, dash, number):
        return -1 * number.value

    @BaseParser.production("Factor : LPAREN Expr RPAREN")
    def Factor3(self, factor, lparen, expr, rparen):
        return expr

parse = Parser(lx.Lex).parse

if __name__ == '__main__':
    parser = Parser(lx.Lex, debug=True)
    def test(expr):
        p = parser.parse(expr)
        assert eval(expr) == p
        print p
    test('(2+3)*4')
