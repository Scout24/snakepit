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


# Arguments for the template
# None means no default, anything else is the default
arguments = {
    'pypi_package_name':            None,
    'pypi_package_version':         None,
    'conda_dist_flavour':           'miniconda',
    'conda_dist_flavour_version':   '',
    'conda_dist_version':           '3.9.1',
    'extra_pip_args':               '',
    'symlinks':                     [],
}


def update_arguments(loaded_yaml):
    for key, value in arguments.items():
        if key not in loaded_yaml:
            loaded_yaml[key] = loaded_yaml


def add_conda_dist_flavour_prefix(loaded_yaml):
    """ Add an first letter uppercase version of the conda_dist_flavour.

    The files from Continuum at:

        http://repo.continuum.io/miniconda/

    all start with an uppercase letter. Hence we need an uppercase version in
    our dictionary so that we can use it in the template.

    """
    x = loaded_yaml['conad_dist_flavour']
    loaded_yaml['conda_dist_flavour_urlprefix'] = x[0].upper() + x[1:]

if __name__ == '__main__':
    arguments = docopt(__doc__)
    with open(arguments['<file>']) as fp:
        loaded_yaml = yaml.load(fp)
    with open('TEMPLATE.spec') as fp:
        loaded_template = fp.read()

    add_conda_dist_flavour_prefix(loaded_yaml)
    template = Template(loaded_template)
    print template.render(**loaded_yaml)
