#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import sys

import lexer as lx
from pytdpp.parser import BaseParser
from ast import Node

# This class subclasses the BaseParser from the Top Down Predictive Parser module. The
# base class implements the actual parsing algorithm. You only need to write the LL(1)
# grammar and parsing actions. In this case I interleaved some of the productions to
# simplify the actions.

class Parser(BaseParser):

    tokens = lx.TOKENSR

    @BaseParser.productions('''
    Expr : Term Expr';
    Expr' : PLUS Term Expr';
    Expr' : DASH Term Expr';
    Expr' : e;
    Term : Factor Term';
    Term' : STAR Factor Term';
    Term' : SLASH Factor Term';
    Term' : e;
    Factor : NUMBER;
    Factor : DASH NUMBER;
    Factor : LPAREN Expr RPAREN; ''')
    def Start(self, nt, *kids):
        n = Node(nt.sym)
        for kid in kids:
            if isinstance(kid, Node): n.addkid(kid)
            elif kid is None: continue
            else: n.addkid(Node(kid.type).addkid(Node(kid.value)))
        return n

parse = Parser(lx.Lex).parse

if __name__ == '__main__':
    parser = Parser(lx.Lex, debug=False)
    def test(expr):
        p = parser.parse(expr)
        print p.dotty()
    print >>sys.stderr, 'expression: ',
    test(raw_input())
