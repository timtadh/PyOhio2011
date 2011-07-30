PyOhio 2011 Example Code for "Python, Parsing, and You"
=======================================================

By Tim Henderson (tim.tadh@gmail.com)


How To Use This Repositories
============================

There are 3 branches in this repository. The top level branch `master` contains
all of the "answers." It has complete implementations for all of the examples
used in the talk. This repository will used during the talk to explain the
algorithms and demontrate their individual characteristics.

There are two other branches, these are meant to allow /you/ the attendeed to
learn by doing. They contain a *skeleton* of two of the parsers with handy "Fill
in this line" comments letting you know where you need to make changes. The
first of these `recursive_skel` contains a skeleton recursive descent parser.
`lalr_skel` contains a skeleton of a LALR parser built using the PLY parser
library.

# Getting the Code

First clone the repository. You will need `git` installed.

    git clone https://github.com/timtadh/PyOhio2011.git

### Check out `master`

It is automatically checked out, but should you switch to a different branch
you can easily switch back with.

    git checkout master

### Check out `recursive_skel`

    git checkout recursive_skel

### Check out `lalr_skel`

    git checkout lalr_skel

Feel free to make commits to any of the branches. If you would like to share
your changes fork the project on github and follow the instructions to push
your changes back up.

Installing PLY
==============

In order to run the lalr this examples you will need PLY the LALR parsing engine
that I use. PLY is available from its homepage http://www.dabeaz.com/ply/ or
via easy_install/pip.

example:

    virtualenv --no-site-packages env
    . env/bin/activate
    pip install ply

