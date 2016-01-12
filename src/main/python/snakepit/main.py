#!/usr/bin/env python

from __future__ import print_function, division

import os.path as osp
import sys

import yaml
from jinja2 import Environment, PackageLoader
import requests

DEBUG = False
REQUIRED = None
FROMPYPIMETA = None


def print_debug(message):
    if DEBUG:
        print(message)


def fail(message, exit_code=1):
    print(message)
    sys.exit(exit_code)

# Arguments for the template
# REQUIRED means it is required
# FROMPYPIMETA means it will get it from PyPi
# Strings and other values are defaults
DEFAULTS = {
    'pypi_package_name':            REQUIRED,
    'pypi_package_version':         FROMPYPIMETA,
    'pypi_package_summary':         FROMPYPIMETA,
    'pypi_package_licence':         FROMPYPIMETA,
    'conda_dist_flavour':           'miniconda',
    'conda_dist_flavour_version':   '',
    'conda_dist_version':           '3.9.1',
    'pyrun_dist_version':           '2.1.1',
    'pyrun_pythonfullversion':      '2.7.10',
    'extra_pip_args':               '',
    'symlinks':                     [],
    'build':                        0,
    'setuptools':                   'setuptools-18.8.1.tar.gz',
    'pip':                          'pip-7.1.2.tar.gz',
    'interpreter':                  'python',
    'distribution':                 'miniconda',
}

PYPIMETAMAPPINGS = {
    'pypi_package_version':         'version',
    'pypi_package_summary':         'summary',
    'pypi_package_licence':         'license',
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


def get_pypi_metadata(package, url='https://pypi.python.org/pypi'):
    return requests.get("{url}/{package}/json".
                        format(url=url, package=package)).json()


def custom_output_filename(filename, output_directory):
    return osp.join(output_directory, filename)


def build_template(yaml_spec):
    distribution = yaml_spec['distribution']
    if distribution == "miniconda":
        template_filename = 'TEMPLATE-miniconda.spec'
    elif distribution == "pyrun":
        template_filename = 'TEMPLATE-PyRun.spec'

    # load the template
    template = Environment(
        loader=PackageLoader('snakepit', 'templates')
    ).get_template(template_filename)

    # check if PyRun Python Version 3 is desired and change the interpreter
    if yaml_spec['pyrun_pythonfullversion'].split('.')[0] == '3':
        yaml_spec['interpreter'] = 'python3'

    # render the template
    return template.render(**yaml_spec)


def construct_build_number(build, yaml_spec):
    # create the build number
    yaml_spec['build'] = build
    distribution = yaml_spec['distribution']
    if distribution == "miniconda":
        build_number = "{0}_{1}{2}_{3}".format(
            yaml_spec['build'],
            yaml_spec['conda_dist_flavour'],
            yaml_spec['conda_dist_flavour_version'],
            yaml_spec['conda_dist_version'],)
    elif distribution == "pyrun":
        build_number = "{0}_pyrun_{1}_py{2}".format(
            yaml_spec['build'],
            yaml_spec['pyrun_dist_version'],
            yaml_spec['pyrun_pythonfullversion'].rsplit(".", 1)[0])

    yaml_spec['build'] = build_number


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
    if not yaml_spec['pypi_package_version']:
        pypi_meta = get_pypi_metadata(yaml_spec['pypi_package_name'])['info']
        # inject things we can get from pypi, that are missing
        for snakepit_key, pypi_meta_key in PYPIMETAMAPPINGS.items():
            if snakepit_key not in yaml_spec or yaml_spec[snakepit_key] is None:
                yaml_spec[snakepit_key] = pypi_meta[pypi_meta_key]

    # do some more magic
    add_conda_dist_flavour_prefix(yaml_spec)

    # update the distribution with a value from the command-line
    if arguments['--distribution']:
        yaml_spec['distribution'] = arguments['--distribution']

    # build release number
    construct_build_number(arguments['--build'], yaml_spec)

    rendered_template = build_template(yaml_spec)

    # get the output filename
    if arguments['--output']:
        if osp.isdir(arguments['--output']):
            output_filename = custom_output_filename(
                default_output_filename(yaml_spec), arguments['--output'])
        else:
            output_filename = arguments['--output']
    else:
        output_filename = default_output_filename(yaml_spec)

    # write it out
    if osp.isfile(output_filename) and not arguments['--force']:
        fail("File: '{0}' exists already, use --force to overwrite".
             format(output_filename), exit_code=output_file_exists)
    else:
        print_debug("Writing output to: '{0}'".format(output_filename))
        with open(output_filename, 'w') as fp:
            fp.write(rendered_template)
