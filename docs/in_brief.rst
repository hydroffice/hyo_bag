In brief
========

.. image:: https://bitbucket.org/ccomjhc/hyo_bag/raw/tip/hydroffice/bag/media/favicon.png
    :alt: logo

The BAG hydro-package collects tools for working with BAG files. BAG is a data format by the `ONS-WG <http://www.opennavsurf.org/>`_ (Open Navigation Surface Working Group).

.. image:: https://bitbucket.org/ccomjhc/hyo_bag/raw/tip/hydroffice/bag_explorer/media/BAGExplorer_128.png
    :alt: logo

BAG Explorer is a light application, based on HDF Compass with a BAG plugin, to explore BAG data files.


About HydrOffice
----------------

HydrOffice is a research development environment for ocean mapping. Its aim is to provide a collection of hydro-packages to deal with specific issues in such a field, speeding up both algorithms testing and research-2-operation.


About this hydro-package
------------------------

This package provides:

* the :code:`bag` package which provides functionalities to deal with BAG data files

* the :code:`bag_explorer` package that uses *HDF Compass* (a viewer program for HDF5 and related formats) and the BAG-specific plugin to build the resulting *BAG Explorer* application.

HDF Compass is written in Python, but ships as a native application on Windows, OS X, and Linux, by using PyInstaller and Py2App to package the app.
For more info about HDF Compass, visit the `GitHub <http://github.com/HDFGroup/hdf-compass>`_ repository and the `project <https://www.hdfgroup.org/projects/compass/>`_ web page.

