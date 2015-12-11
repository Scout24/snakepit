#!/usr/bin/env cram
# vim: set syntax=cram :

  $ export PROJECT_ROOT=$TESTDIR/../../
  $ cp $PROJECT_ROOT/snakepit.yaml .
  $ ls
  snakepit.yaml

# test w/o arguments

  $ snakepit
  Usage:
    snakepit [--debug] [--build=<build>] [(-f | --force)] [--output=<filename>] [--distribution=<distribution>] <file>
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
    snakepit [--debug] [--build=<build>] [(-f | --force)] [--output=<filename>] [--distribution=<distribution>] <file>
    snakepit (-h | --help)
    snakepit --version
  
  Options:
    -h --help                      Show this screen.
    --version                      Show version.
    --debug                        Enable debug output.
    --build=<build>                The build number [default: 0]
    -f, --force                    Force overwrite of output.
    --output=<filename>            Filename for SPEC-File.
    --distribution=<distribution>  Python distribution to use [default: miniconda]

  $ snakepit --help
  snakepit
  
  Usage:
    snakepit [--debug] [--build=<build>] [(-f | --force)] [--output=<filename>] [--distribution=<distribution>] <file>
    snakepit (-h | --help)
    snakepit --version
  
  Options:
    -h --help                      Show this screen.
    --version                      Show version.
    --debug                        Enable debug output.
    --build=<build>                The build number [default: 0]
    -f, --force                    Force overwrite of output.
    --output=<filename>            Filename for SPEC-File.
    --distribution=<distribution>  Python distribution to use [default: miniconda]

# test generating file

  $ snakepit snakepit.yaml
  $ ls
  moto.spec
  snakepit.yaml

# Try doing it again

  $ snakepit snakepit.yaml
  File: 'moto.spec' exists already, use --force to overwrite
  [2]

# now use the force switch

  $ snakepit --force snakepit.yaml
  $ snakepit -f snakepit.yaml

# now double check with --debug

  $ snakepit --force --debug snakepit.yaml
  {'--build': '0',
   '--debug': True,
   '--distribution': 'miniconda',
   '--force': True,
   '--help': False,
   '--output': None,
   '--version': False,
   '<file>': 'snakepit.yaml'}
  Writing output to: 'moto.spec'

# now double check with --debug and --build

  $ snakepit --force --debug --build 1 snakepit.yaml
  {'--build': '1',
   '--debug': True,
   '--distribution': 'miniconda',
   '--force': True,
   '--help': False,
   '--output': None,
   '--version': False,
   '<file>': 'snakepit.yaml'}
  Writing output to: 'moto.spec'

# test specified output is an existent directory

  $ snakepit snakepit.yaml --output /some/where/else
  Traceback (most recent call last):
  .* (re)
  .* (re)
  .* (re)
  .* (re)
  IOError: [Errno 2] No such file or directory: '/some/where/else'
  [1]

# test specified output writable

  $ snakepit snakepit.yaml --output /some/where/else/moto.spec
  Traceback (most recent call last):
  .* (re)
  .* (re)
  .* (re)
  .* (re)
  IOError: [Errno 2] No such file or directory: '/some/where/else/moto.spec'
  [1]

# test specified output file was created

  $ snakepit snakepit.yaml --output moto.spec --force
  $ ls moto.spec
  moto.spec

# test specified output file was created in specified directory  

  $ mkdir somewhere
  $ snakepit snakepit.yaml --output somewhere/moto.spec
  $ ls somewhere/moto.spec
  somewhere/moto.spec
  $ rm -r somewhere
