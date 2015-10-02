#!/usr/bin/env python

from __future__ import print_function, division

import os.path as osp
import sys
import pkg_resources

import yaml
from jinja2 import Template
import requests

TEMPLATE_FILENAME = 'TEMPLATE.spec'
DEBUG = False


def print_debug(message):
    if DEBUG:
        print(message)


def fail(message, exit_code=1):
    print(message)
    sys.exit(exit_code)

# Arguments for the template
# None means no default, anything else is the default
DEFAULTS = {
    'pypi_package_name':            None,
    'pypi_package_version':         None,
    'conda_dist_flavour':           'miniconda',
    'conda_dist_flavour_version':   '',
    'conda_dist_version':           '3.9.1',
    'extra_pip_args':               '',
    'symlinks':                     [],
    'build':                        0,
}

PYPIMETAMAPPINGS = {
    'pypi_package_version':         'version',
}

# command line errors
output_file_exists = 2


class TemplateNoteFoundException(Exception):
    pass


def add_conda_dist_flavour_prefix(yaml_spec):
    """ Add an first letter uppercase version of the conda_dist_flavour.

    The files from Continuum at:

        http://repo.continuum.io/miniconda/

    all start with an uppercase letter. Hence we need an uppercase version in
    our dictionary so that we can use it in the template.

    """
    x = yaml_spec['conda_dist_flavour']
    yaml_spec['conda_dist_flavour_urlprefix'] = x[0].upper() + x[1:]


def default_output_filename(yaml_spec):
    return "{0}.spec".format(yaml_spec['pypi_package_name'])


def get_pypi_metadata(package, url='https://pypi.python.org/pypi/'):
    return requests.get("{url}/{package}/json".
                        format(url=url, package=package)).json()


def main(arguments):
    global DEBUG
    if arguments['--debug']:
        DEBUG = True
    print_debug(arguments)

    # create the object to hold the final yaml spec
    yaml_spec = {}
    # inject the defaults
    yaml_spec.update(DEFAULTS)

    # load the snakepit.yaml and update
    with open(arguments['<file>']) as fp:
        loaded_yaml = yaml.load(fp)
    yaml_spec.update(loaded_yaml)

    # get package metadata from PyPi
    pypi_meta = get_pypi_metadata(yaml_spec['pypi_package_name'])['info']
    # inject things we can get from pypi, that are missing
    for snakepit_key, pypi_meta_key in PYPIMETAMAPPINGS.items():
        if snakepit_key not in yaml_spec or yaml_spec[snakepit_key] is None:
            yaml_spec[snakepit_key] = pypi_meta[pypi_meta_key]

    # do some more magic
    add_conda_dist_flavour_prefix(yaml_spec)

    # create the build number
    build_number = "{0}-{1}{2}_{3}".format(yaml_spec['build'],
                                           yaml_spec['conda_dist_flavour'],
                                           yaml_spec['conda_dist_flavour_version'],
                                           yaml_spec['conda_dist_version'],
                                           )
    yaml_spec['build'] = build_number

    # load the template
    template = Template(pkg_resources.resource_string('snakepit',
                                                      TEMPLATE_FILENAME))

    # get the output filename
    output_filename = default_output_filename(yaml_spec)

    # render the template
    rendered_template = template.render(**yaml_spec)

    # write it out
    if osp.isfile(output_filename) and not arguments['--force']:
        fail("File: '{0}' exists already, use --force to overwrite".
             format(output_filename), exit_code=output_file_exists)
    else:
        print_debug("Writing output to: '{0}'".format(output_filename))
        with open(output_filename, 'w') as fp:
            fp.write(rendered_template)
