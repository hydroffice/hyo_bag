hyo_bag
===========

![logo](https://bitbucket.org/ccomjhc/hyo_bag/raw/tip/hydroffice/bag/gui/media/favicon.png)

The bag hydro-package collects tools for working with BAG files. BAG is a data format by the [ONS-WG](http://www.opennavsurf.org/) (Open Navigation Surface Working Group).

### About HydrOffice

HydrOffice is a research development environment for ocean mapping. Its aim is to provide a collection of hydro-packages to deal with specific issues in such a field, speeding up both algorithms testing and research-2-operation.

### About this hydro-package

This package provides:

* the `bag` package which provides functionalities to deal with BAG data files

* the `bag_explorer` package that uses *HDF Compass* (a viewer program for HDF5 and related formats) and the BAG-specific plugin to build the resulting *BAG Explorer* application.  

HDF Compass is written in Python, but ships as a native application on Windows, OS X, and Linux, by using PyInstaller and Py2App to package the app.
For more info about HDF Compass, visit the [GitHub](http://github.com/HDFGroup/hdf-compass) repository and the [project](https://www.hdfgroup.org/projects/compass/) web page.


Development Environment
-----------------------

For the BAG library, you will need:

* `Python >=2.7` (`>=3.4` support is in progress)
* `NumPy`
* `h5py`

For executing and packaging the *BAG Explorer* app:

* `hdf_compass` (that requires: `matplotlib`, `wxPython Phoenix` `h5py` and (optionally) `pydap`)
* `PyInstaller`


Packaging
--------------------

### Use of Pyinstaller

* `pyinstaller --clean -y BAGExplorer.1file.spec`
* `pyinstaller --clean -y BAGExplorer.1folder.spec`

### Creation of MAC OS dmg

* `appdmg spec.json BAGExplorer.dmg`


Useful Mercurial commands
-----------------------

### Merge a branch to default

* `hg update default`
* `hg merge 1.0.0`
* `hg commit -m"Merged 1.0.2 branch with default" -ugiumas`
* `hg update 1.0.0`
* `hg commit -m"Close 1.0.2 branch" -ugiumas --close-branch`

### Open a new branch

* `hg update default`
* `hg branch 1.0.1`
* `hg commit -m"Created 1.0.3 branch" -ugiumas`


Useful git commands
-----------------------

### Syncing a fork

Add a remote that points to the upstream repo (from the forked project folder):

* `git remote -v` (check before and after if the remote is present)
* `git remote add upstream https://github.com/HDFGroup/hdf-compass`

Fetching from the remote repository:

* `git branch -va` (check all the available branches)
* `git fetch upstream`

Merging with the upstream repository:

* `git checkout master` (to switch to `master` branch)
* `git merge upstream/master`

Finally:

* `git push origin master`

### Reset the fork

* `git remote add upstream https://github.com/HDFGroup/hdf-compass`
* `git fetch upstream`
* `git branch backup`
* `git checkout upstream/master -B master`
* `git push --force`

In case of need to retrieve the original code status:

* `git checkout backup`


Other info
----------

* Bitbucket: [https://bitbucket.org/ccomjhc/hyo_bag](https://bitbucket.org/ccomjhc/hyo_bag)
* Project page: [http://ccom.unh.edu/project/hydroffice](http://ccom.unh.edu/project/hydroffice)
* License: BSD-like license (See [COPYING](https://bitbucket.org/ccomjhc/hyo_bag/raw/tip/COPYING.txt))
