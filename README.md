# snakepit

## Description

Package Python software as an RPM including all dependencies (even the
interpreter).

This solves the problem of an outdated Python (2.6) on RHEL since we can now
deploy self-contained RPMs that are independent.

The source of truth for the software to be installed is the Python package
index at: https://pypi.python.org/pypi

## Example

See the file `snakepit.yaml` for details on how to build a spec file for
`moto`.

You can then:

```
$ snakepit snakepit.yaml
```

Which will produce a `moto.spec` file.

For more information on options:

```
$ snakepit -h
```

## Building the resulting `*.spec` files.

The resulting spec file requires the `make-opt-writable` rpm which you can
build using the `make-opt-writable.spec` (included in repository) file. This is
required due to very low-level reasons related to the way in which miniconda
is installed.

Furthermore, the spec file is of a special flavour of `svn2rpm` which can be
found at: https://github.com/immobilienscout24/svn2rpm/. You may not yet be
able to use the spec files w/o this tool and the surrounding boilerplate.

# How does it work?

For a given product to build an RPM for---let's call it
`mypackage`---`snakepit` will create a spec file. The spec file works as
follows:

* Install anaconda/miniconda to `/opt/mypackage`
* Install the product into that installtion using `pip`
* Setup any symlinks from `/opt/mypackage/bin` to `/usr/bin`
* Copy the whole installation into the buildroot

## Installation

It is available from PyPi: https://pypi.python.org/pypi/snakepit

To install:

```
pip install snakepit
```

## Development

Use pybuilder: http://pybuilder.github.io/

## Getting in touch

Please use the conda mailinglist at: https://groups.google.com/a/continuum.io/forum/#!forum/conda

## Status

This tool is in an early alpha stage and the output is guaranteed to change.
Feedback, comments and pull-requests welcome, but please do bear in mind that,
this is work in progress and therefore probably full of many, many horrible
bugs.

## Licence

Copyright 2015 Immobilienscout24 GmbH

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

## TODO

* Include git-hash of snakepit in spec
* Include version number of conda-dist
* Specify template file via `--template`
* Specify output via `--output`
* Allow outputing the spec file on stdout using `--stdout`
* Download .sh installer via Source0
* Install optional dependencies, e.g. `ipython[all]`
* What if we want to install conda packages?
* What if we have a complex dependency chain
* What if we want to install multiple products
* What about additional spec-file metadata, e.g. licence?
* What about the illegibility of the spec file template
* Add a `--release` switch to modify the release number
* Decouple from make-opt-writable
* Decouple svn2rpm
* Consider "snakepyt" as name
* If no file specified, it should look for a `snakepit.yaml` or `.snakepit.yaml`
* `--pre` and `--post` hooks for the spec file
* Fixup the package summary from metadata on pypi
* Fixup the package description from metadata on pypi
* Release number should be: XX-miniconda.-pythonA.B
* Augment the description with complete metadata
* Automagically determine the symlinks. (either by doing deltas during install,
  or by inspecting the metadata.)
* Ability to package additional things, such as bash completions, cron-jobs and
  so on.
* Search for an existing `snakepit.yaml` in the current working directory.
* Change package name from `product`-`conda-dist` to something the user can
  select.
