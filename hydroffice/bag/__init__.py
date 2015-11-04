"""
Hydro-Package
BAG
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from .helper import BAGError
from .base import is_bag
from .bag import BAGFile


__version__ = '0.2.4'
__doc__ = 'BAG'
__author__ = 'gmasetti@ccom.unh.edu, brc@ccom.unh.edu'
__license__ = 'BSD-like license'
__copyright__ = 'Copyright 2015 Giuseppe Masetti, Brian R. Calder'


# def hyo():
# def hyo_app():
def hyo_lib():
    return __doc__, __version__
