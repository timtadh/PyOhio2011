#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

class token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __repr__(self):
        return str(self.value)

def Lex(inpt):
    digits = list()
    for x in inpt:
        if x.isdigit():
            digits.append(x)
        elif digits:
            yield token('NUMBER', int(''.join(digits)))
            digits = list()

        if x == ' ': continue
        elif x == '+': yield token('PLUS', x)
        elif x == '-': yield token('DASH', x)
        elif x == '*': yield token('STAR', x)
        elif x == '/': yield token('SLASH', x)
        elif x == '(': yield token('LPAREN', x)
        elif x == ')': yield token('RPAREN', x)
        elif not x.isdigit():
            raise Exception, 'Unknown character! %s' % (x)
    if digits:
        yield token('NUMBER', int(''.join(digits)))
