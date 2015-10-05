from __future__ import absolute_import, division, print_function, unicode_literals

import logging

log = logging.getLogger(__name__)

import h5py

from .helper import BAGError


def is_bag(file_name):
    """ Determine if a file is valid BAG (False if it doesn't exist). """

    # we first check if the file is a valid hdf5 (it also checks if the file exists)
    if not h5py.is_hdf5(file_name):
        return False

    fid = h5py.File(file_name, 'r')

    try:
        fid["BAG_root"]

    except KeyError:
        return False

    return True


class File(object):
    def __init__(self, name, mode=None, driver=None,
                 libver=None, userblock_size=None, swmr=False, **kwds):
        """ Create a new file object.

        See the h5py user guide for a detailed explanation of the options.

        name
            Name of the file on disk.  Note: for files created with the 'core'
            driver, HDF5 still requires this be non-empty.
        driver
            Name of the driver to use.  Legal values are None (default,
            recommended), 'core', 'sec2', 'stdio', 'mpio'.
        libver
            Library version bounds.  Currently only the strings 'earliest'
            and 'latest' are defined.
        userblock
            Desired size of user block.  Only allowed when creating a new
            file (mode w, w- or x).
        swmr
            Open the file in SWMR read mode. Only used when mode = 'r'.
        Additional keywords
            Passed on to the selected file driver.
        """

        if not is_bag(name):
            raise BAGError("The passed file %s is not a BAG file")

        self.fid = h5py.File(name=name, mode=mode, driver=driver,
                             libver=libver, userblock_size=userblock_size, swmr=swmr, **kwds)
