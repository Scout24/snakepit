#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from pybuilder.core import use_plugin, init, Author
from pybuilder.vcs import VCSRevision

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
#use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin('python.cram')

name = "snakepit"
default_task = "publish"
version = VCSRevision().get_git_revision_count()
summary = "Package Python software as an RPM including all dependencies " \
          "(even the interpreter)."
authors = [Author('Valentin Haenel', 'valentin@haenel.co')]
license = 'Apache'
url = 'https://github.com/ImmobilienScout24/snakepit'


@init
def set_properties(project):
    project.set_property('install_dependencies_upgrade', True)
    project.build_depends_on("unittest2")
    project.build_depends_on("requests_mock")
    project.depends_on("jinja2")
    project.depends_on("pyyaml")
    project.depends_on("docopt")
    project.depends_on("requests")
    project.include_file('snakepit', 'templates/TEMPLATE-PyRun.spec')
    project.include_file('snakepit', 'templates/TEMPLATE-miniconda.spec')
    project.set_property('distutils_classifiers', [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: Utilities',
    ])
