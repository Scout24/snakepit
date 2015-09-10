# snakepit

## Description

Package Python software as an RPM including all dependencies (even the
interpreter) and miniconda/anaconda as base.

## Example

See the file `snakepit.yaml` for details on how to build a spec file for
`moto`.

# Licence

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
* Specifiy template file
* Specify output
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
