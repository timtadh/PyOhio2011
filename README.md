PyOhio 2011 Example Code - LALR Parser Skeleton
===============================================

This branch contains skeleton code for a the LALR parser. See `lalr.py` for the
skeleton of the parser. The full grammar is contained in the `grammar.md` file.

Dependencies
============

In order to complete this example you will need PLY the LALR parsing engine
that I use. PLY is available from its homepage http://www.dabeaz.com/ply/ or
via easy_install/pip.

example:

    virtualenv --no-site-packages env
    . env/bin/activate
    pip install ply

