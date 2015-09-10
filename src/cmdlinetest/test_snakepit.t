#!/usr/bin/env cram
# vim: set syntax=cram :

  $ export PROJECT_ROOT=$TESTDIR/../../
  $ cp $PROJECT_ROOT/snakepit.yaml .
  $ ls
  snakepit.yaml

# test w/o arguments

  $ snakepit
  Usage:
    snakepit [--debug] [(-f | --force)]<file>
    snakepit (-h | --help)
    snakepit --version
  [1]

# check the version, yo!

  $ snakepit --version
  alpha

# test help

  $ snakepit -h
  snakepit
  
  Usage:
    snakepit [--debug] [(-f | --force)]<file>
    snakepit (-h | --help)
    snakepit --version
  
  Options:
    -h --help     Show this screen.
    --version     Show version.
    --debug       Enable debug output.
    -f, --force   Force overwrite of output.

  $ snakepit --help
  snakepit
  
  Usage:
    snakepit [--debug] [(-f | --force)]<file>
    snakepit (-h | --help)
    snakepit --version
  
  Options:
    -h --help     Show this screen.
    --version     Show version.
    --debug       Enable debug output.
    -f, --force   Force overwrite of output.

# test generating file

  $ snakepit snakepit.yaml
  $ ls
  moto.spec
  snakepit.yaml

# Try doing it again

  $ snakepit snakepit.yaml
  File: 'moto.spec' exists already, use --force to overwrite
  [3]

# now use the force switch

  $ snakepit --force snakepit.yaml
  $ snakepit -f snakepit.yaml

# now double check with --debug

  $ snakepit --force --debug snakepit.yaml
  {'--debug': True,
   '--force': True,
   '--help': False,
   '--version': False,
   '<file>': 'snakepit.yaml'}
  Looking for template in '.*' (re)
  Looking for template in '.*/src/main/python/snakepit/TEMPLATE.spec' (re)
  Template found
  Writing output to: 'moto.spec'
