#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

'''
Generates Abstract Syntax Trees (ASTs) using PyTDPP as the parser engine. The AST
generated is from the LL(1) grammar.
'''

import sys

import lexer as lx
from pytdpp.parser import BaseParser
from ast import Node

# This class subclasses the BaseParser from the Top Down Predictive Parser module. The
# base class implements the actual parsing algorithm. You only need to write the LL(1)
# grammar and parsing actions.

class Parser(BaseParser):
    '''Parses the LL(1) arithmetic grammar and generates an AST.

    Usage
    =====

    using the parse function (at the module level).

        ast = parse(expr)

    using this class directly.

        import lexer as lx
        parser = Parser(lx.Lex)
        ast = parser.parse(expr)
    '''

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
        '''
        The production action for all productions in the grammar. The AST
        which is built is actually the same as the Parse Tree. Therefore,
        it is easy to have a generic action for all of the grammar rules.
        '''
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
