from __future__ import absolute_import, division, print_function, unicode_literals

import h5py


def is_bag(fname):
    """ Determine if a file is valid BAG (False if it doesn't exist). """

    # we first check if the file is a valid hdf5 (it also checks if the file exists)
    if not h5py.is_hdf5(fname):
        return False

    fid = h5py.File(fname, 'r')

    try:
        fid["BAG_root"]

    except KeyError:
        return False

    return True


class Bag(object):
    def __init__(self):
        pass
