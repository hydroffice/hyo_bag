"""
Hydro-Package
BAG
"""
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from .helper import BAGError
from .base import is_bag
from .bag import BAGFile


__version__ = '0.5.7'
__doc__ = 'BAG'
__author__ = 'gmasetti@ccom.unh.edu, brc@ccom.unh.edu'
__license__ = 'LGPLv3 license'
__copyright__ = 'Copyright (c) 2018, University of New Hampshire, Center for Coastal and Ocean Mapping'


# def hyo_app():
#     return __doc__, __version__

def hyo_lib():
    return __doc__, __version__
