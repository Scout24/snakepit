#!/usr/bin/env python

from __future__ import print_function, division

import os.path as osp
import sys

import yaml
from jinja2 import Template

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
}


# command line errors
template_not_found = 2
output_file_exists = 3


class TemplateNoteFoundException(Exception):
    pass


def update_loaded(defaults, loaded_yaml):
    """ Update loaded_yaml with values and keys from defaults. """
    for key, value in defaults.items():
        if key not in loaded_yaml:
            loaded_yaml[key] = value


def add_conda_dist_flavour_prefix(loaded_yaml):
    """ Add an first letter uppercase version of the conda_dist_flavour.

    The files from Continuum at:

        http://repo.continuum.io/miniconda/

    all start with an uppercase letter. Hence we need an uppercase version in
    our dictionary so that we can use it in the template.

    """
    x = loaded_yaml['conda_dist_flavour']
    loaded_yaml['conda_dist_flavour_urlprefix'] = x[0].upper() + x[1:]


def locate_template():
    """ Find the template file.

    Look for it in the current working directory, then in the directory where
    this file is located and fail otherwise.

    """
    if osp.isfile(TEMPLATE_FILENAME):
        return TEMPLATE_FILENAME
    else:
        location = osp.join(osp.dirname(osp.abspath(__file__)),
                            TEMPLATE_FILENAME)
        if not osp.isfile(location):
            raise TemplateNoteFoundException()
        else:
            return location


def default_output_filename(loaded_yaml):
    return "{0}.spec".format(loaded_yaml['pypi_package_name'])


def main(arguments):
    global DEBUG
    if arguments['--debug']:
        DEBUG = True
    print_debug(arguments)

    with open(arguments['<file>']) as fp:
        loaded_yaml = yaml.load(fp)
    try:
        template_location = locate_template()
    except TemplateNoteFoundException:
        fail("Template not found!", exit_code=template_not_found)
    else:
        with open(template_location) as fp:
            loaded_template = fp.read()

    update_loaded(DEFAULTS, loaded_yaml)
    add_conda_dist_flavour_prefix(loaded_yaml)
    template = Template(loaded_template)

    output_filename = default_output_filename(loaded_yaml)
    if osp.isfile(output_filename) and not arguments['--force']:
        fail("File: '{0}' exists already, use --force to overwrite".
             format(output_filename), exit_code=3)
    else:
        print_debug("Writing output to: '{0}'".format(output_filename))
        with open(output_filename, 'w') as fp:
            fp.write(template.render(**loaded_yaml))
