
Tokens
======

    NUMBER  : [0-9]+
    PLUS    : \+
    DASH    : -
    STAR    : \*
    SLASH   : /
    LPAREN  : \(
    RPAREN  : \)

LL(1) Grammar
=============

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
    Factor : LPAREN Expr RPAREN;

LALR Grammar
============

    Expr : Expr PLUS Term
    Expr : Expr DASH Term
    Expr : Term
    Term : Term STAR Factor
    Term : Term SLASH Factor
    Term : Factor
    Factor : NUMBER
    Factor : DASH NUMBER
    Factor : LPAREN Expr RPAREN
