#!/usr/bin/env cram
# vim: set syntax=cram :

  $ export PROJECT_ROOT=$TESTDIR/../../
  $ cp $PROJECT_ROOT/snakepit.yaml .
  $ ls
  snakepit.yaml

# test w/o arguments

  $ snakepit
  Usage:
    snakepit <file>
    snakepit (-h | --help)
    snakepit --version
  [1]

# test help

  $ snakepit -h
  snakepit
  
  Usage:
    snakepit <file>
    snakepit (-h | --help)
    snakepit --version
  
  Options:
    -h --help     Show this screen.
    --version     Show version.

  $ snakepit --help
  snakepit
  
  Usage:
    snakepit <file>
    snakepit (-h | --help)
    snakepit --version
  
  Options:
    -h --help     Show this screen.
    --version     Show version.

# test generating file

  $ snakepit snakepit.yaml
  $ ls
  moto.spec
  snakepit.yaml

# Try doing it again

  $ snakepit snakepit.yaml
  File: 'moto.spec' exists already, use --force to overwrite
  [3]


