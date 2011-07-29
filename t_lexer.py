#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import lexer as lx
from lexer import Lex, token

def t_Number():
    assert list(Lex('234')) == [token(lx.NUMBER, 234)]
    assert list(Lex('   234')) == [token(lx.NUMBER, 234)]
    assert list(Lex('   234     ')) == [token(lx.NUMBER, 234)]
    assert list(Lex('234     ')) == [token(lx.NUMBER, 234)]
    assert list(Lex('234 23   45 ')) == [
                                            token(lx.NUMBER, 234),
                                            token(lx.NUMBER, 23),
                                            token(lx.NUMBER, 45)
                                        ]

def t_Plus():
    assert list(Lex('+')) == [token(lx.PLUS, '+')]
    assert list(Lex('  +')) == [token(lx.PLUS, '+')]
    assert list(Lex('  +   ')) == [token(lx.PLUS, '+')]
    assert list(Lex('+   ')) == [token(lx.PLUS, '+')]

def t_DASH():
    assert list(Lex('-')) == [token(lx.DASH, '-')]
    assert list(Lex('  -')) == [token(lx.DASH, '-')]
    assert list(Lex('  -   ')) == [token(lx.DASH, '-')]
    assert list(Lex('-   ')) == [token(lx.DASH, '-')]

def t_STAR():
    assert list(Lex('*')) == [token(lx.STAR, '*')]
    assert list(Lex('  *')) == [token(lx.STAR, '*')]
    assert list(Lex('  *   ')) == [token(lx.STAR, '*')]
    assert list(Lex('*   ')) == [token(lx.STAR, '*')]

def t_SLASH():
    assert list(Lex('/')) == [token(lx.SLASH, '/')]
    assert list(Lex('  /')) == [token(lx.SLASH, '/')]
    assert list(Lex('  /   ')) == [token(lx.SLASH, '/')]
    assert list(Lex('/   ')) == [token(lx.SLASH, '/')]

def t_LPAREN():
    assert list(Lex('(')) == [token(lx.LPAREN, '(')]
    assert list(Lex('  (')) == [token(lx.LPAREN, '(')]
    assert list(Lex('  (   ')) == [token(lx.LPAREN, '(')]
    assert list(Lex('(   ')) == [token(lx.LPAREN, '(')]

def t_RPAREN():
    assert list(Lex(')')) == [token(lx.RPAREN, ')')]
    assert list(Lex('  )')) == [token(lx.RPAREN, ')')]
    assert list(Lex('  )   ')) == [token(lx.RPAREN, ')')]
    assert list(Lex(')   ')) == [token(lx.RPAREN, ')')]

def t_COMPOUND():
    assert list(Lex('(2+5)*3/17')) == [
                                        token(lx.LPAREN, '('),
                                        token(lx.NUMBER, 2),
                                        token(lx.PLUS, '+'),
                                        token(lx.NUMBER, 5),
                                        token(lx.RPAREN, ')'),
                                        token(lx.STAR, '*'),
                                        token(lx.NUMBER, 3),
                                        token(lx.SLASH, '/'),
                                        token(lx.NUMBER, 17),
                                      ]