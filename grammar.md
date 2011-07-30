
Tokens
======

    NUMBER  : [0-9]+
    PLUS    : \+
    DASH    : -
    STAR    : \*
    SLASH   : /
    LPAREN  : \(
    RPAREN  : \)

Productions
===========

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
