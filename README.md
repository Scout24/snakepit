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
