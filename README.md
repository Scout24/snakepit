# snakepit

## Description

Package Python software as an RPM including all dependencies (even the
interpreter) and miniconda/anaconda as base.

## Example

See the file `example.yaml` for details.

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
