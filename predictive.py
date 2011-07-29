#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import lexer as lx
from pytdpp.parser import BaseParser

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
        Term' : STAR Factor Term';
        ''')
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

    @BaseParser.production("Factor : LPAREN Expr RPAREN")
    def Factor2(self, factor, lparen, expr, rparen):
        return expr

parse = Parser(lx.Lex).parse

if __name__ == '__main__':
    print Parser.tokens
    parser = Parser(lx.Lex, debug=True)
    def test(expr):
        p = parser.parse(expr)
        assert eval(expr) == p
        print p
    #print parser.parse('7*4*3')
    test('9*4/(4*2+4)*6/8')
