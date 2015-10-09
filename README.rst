HydrOffice BAG and BAG Explorer
===============================

.. image:: https://bitbucket.org/ccomjhc/hyo_bag/raw/tip/hydroffice/bag/gui/media/favicon.png
    :alt: logo

The BAG hydro-package collects tools for working with BAG files. BAG is a data format by the `ONS-WG <http://www.opennavsurf.org/>`_ (Open Navigation Surface Working Group).

.. image:: https://bitbucket.org/ccomjhc/hyo_bag/raw/tip/hydroffice/bag_explorer/media/BAGExplorer_128.png
    :alt: logo

BAG Explorer is a light application, based on HDF Compass with a BAG plugin, to explore BAG data files.

About HydrOffice
````````````````

HydrOffice is a research development environment for ocean mapping. Its aim is to provide a collection of hydro-packages to deal with specific issues in such a field, speeding up both algorithms testing and research-2-operation.

About this hydro-package
````````````````````````

This package provides:

* the :code:`bag` package which provides functionalities to deal with BAG data files

* the :code:`bag_explorer` package that uses *HDF Compass* (a viewer program for HDF5 and related formats) and the BAG-specific plugin to build the resulting *BAG Explorer* application.

HDF Compass is written in Python, but ships as a native application on Windows, OS X, and Linux, by using PyInstaller and Py2App to package the app.
For more info about HDF Compass, visit the `GitHub <http://github.com/HDFGroup/hdf-compass>`_ repository and the `project <https://www.hdfgroup.org/projects/compass/>`_ web page.


Development Environment
-----------------------

For the BAG library, you will need:

* `Python >=2.7` (`>=3.4` support is in progress)
* :code:`numpy`
* :code:`h5py`

For executing and packaging the *BAG Explorer* app:

* :code:`hdf_compass` (that requires: :code:`matplotlib`, `wxPython Phoenix` :code:`h5py`, (optionally) :code:`pydap` and :code:`hydroffice.bag`)
* `PyInstaller`


Packaging
---------

Use of Pyinstaller
``````````````````

* :code:`pyinstaller --clean -y BAGExplorer.1file.spec`
* :code:`pyinstaller --clean -y BAGExplorer.1folder.spec`

Creation of MAC OS dmg
``````````````````````

* :code:`appdmg spec.json BAGExplorer.dmg`


Useful Mercurial commands
-------------------------

Merge a branch to default
`````````````````````````

* :code:`hg update default`
* :code:`hg merge 2.0.0`
* :code:`hg commit -m"Merged 2.0.0 branch with default" -ugiumas`
* :code:`hg update 2.0.0`
* :code:`hg commit -m"Close 2.0.0 branch" -ugiumas --close-branch`

Open a new branch
`````````````````

* :code:`hg update default`
* :code:`hg branch 2.0.1`
* :code:`hg commit -m"Created 2.0.1 branch" -ugiumas`


Useful git commands
-------------------

Syncing a fork
``````````````

Add a remote that points to the upstream repo (from the forked project folder):

* :code:`git remote -v` (check before and after if the remote is present)
* :code:`git remote add upstream https://github.com/HDFGroup/hdf-compass`

Fetching from the remote repository:

* :code:`git branch -va` (check all the available branches)
* :code:`git fetch upstream`

Merging with the upstream repository:

* :code:`git checkout master` (to switch to :code:`master` branch)
* :code:`git merge upstream/master`

Finally:

* :code:`git push origin master`

Reset the fork
``````````````

* :code:`git remote add upstream https://github.com/HDFGroup/hdf-compass`
* :code:`git fetch upstream`
* :code:`git branch backup`
* :code:`git checkout upstream/master -B master`
* :code:`git push --force`

In case of need to retrieve the original code status:

* :code:`git checkout backup`


Other info
----------

* Bitbucket: `https://bitbucket.org/ccomjhc/hyo_bag <https://bitbucket.org/ccomjhc/hyo_bag>`_
* Project page: `http://ccom.unh.edu/project/hydroffice <http://ccom.unh.edu/project/hydroffice>`_
* License: BSD-like license (See `COPYING <https://bitbucket.org/ccomjhc/hyo_bag/raw/tip/COPYING.txt>`_)
