hyo_bag
===========

The `hyo_bag` package can be used as a starting point to build a hydro-package.

About HydrOffice
-----------------------

HydrOffice is a research development environment for ocean mapping. Its aim is to provide a collection of hydro-packages to deal with specific issues in such a field, speeding up both algorithms testing and research-2-operation.

About this hydro-package
-----------------------

This package provides functionalities to deal with BAG data files.

Freezing
-----------------------

### Pyinstaller

* `pyinstaller --clean -y -i BAG.ico --hidden-import=pkg_resources -F BAG.py`
* add `media_tree = Tree('hydroffice/bag/gui/media', prefix='hydroffice/bag/gui/media')`
* add `manual_tree = Tree('hydroffice/bag/docs', prefix='hydroffice/bag/docs', excludes=['*.docx',])`
* `pyinstaller --clean -y BAG.spec`

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
    
Other info
----------

* Bitbucket: https://bitbucket.org/gmasetti/hyo_bag
* Project page: http://ccom.unh.edu/project/hydroffice
* License: BSD-like license (See COPYING)




hyo_bag
===========

The bag hydro-package collects tools for working with BAG files.
BAG is a data format by the [ONS-WG](http://www.opennavsurf.org/) (Open Navigation Surface Working Group).

It also uses HDF Compass (a viewer program for
HDF5 and related formats) and the BAG-specific plugin to create a BAG Explorer application.  

HDF Compass is written in Python, but ships as a native application on
Windows, OS X, and Linux, by using PyInstaller and Py2App to package the app.

For more info about HDF Compass
* Github: http://github.com/HDFGroup/hdf-compass
* Project page: https://www.hdfgroup.org/projects/compass/

Development Environment
-----------------------

For the BAG library, you will need:

* `Python >=2.7` (`>=3.4` support is in progress)
* `NumPy`
* `h5py`

For executing and packaging the BAG Explorer app:

* `Matplotlib`
* `wxPython Phoenix` (`>=2.9.5.0`)
* `PyInstaller`: `pip install -i https://pypi.binstar.org/pypi/simple pyinstaller`


BAG Explorer
-------------------

For building the BAG Explorer, you need to clone the `hdf-compass` git repository, and the put it in your `PYTHONPATH`:

* `https://github.com/giumas/hdf-compass`


Running the Program
-------------------

    $ python BAG.py
    
    
Packaging
--------------------

### All supported platforms (Linux, Mac, and Windows)

    $ pyinstaller HDFCompass.spec
    
### Creation of a MAC OS X dmg 


Other info
----------

* Github: https://github.com/giumas/hdf-compass
* Project page: http://www.opennavsurf.org/
* License: BSD-like HDF Group license (See COPYING)