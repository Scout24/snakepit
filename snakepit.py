#!/usr/bin/env python

"""snakepit

Usage:
  snakepit <file>
  snakepit (-h | --help)
  snakepit --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
import yaml
from jinja2 import Template


def add_conda_dist_flavour_prefix(loaded_yaml):
    x = loaded_yaml['conad_dist_flavour']
    loaded_yaml['conad_dist_flavour_urlprefix'] = x[0].upper() + x[1:]


if __name__ == '__main__':
    arguments = docopt(__doc__)
    with open(arguments['<file>']) as fp:
        loaded_yaml = yaml.load(fp)
    with open('TEMPLATE.spec') as fp:
        loaded_template = fp.read()

    add_conda_dist_flavour_prefix(loaded_yaml)
    template = Template(loaded_template)
    print template.render(**loaded_yaml)
