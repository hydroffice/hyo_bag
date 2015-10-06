from __future__ import absolute_import, division, print_function  # , unicode_literals

import os
import sys
import logging
import numpy as np
import h5py
from lxml import etree

log = logging.getLogger(__name__)

from .base import is_bag, File
from .helper import BAGError
from .meta import Meta


class BAGFile(File):
    """ Represents a BAG file. """

    _bag_root = "BAG_root"
    _bag_version = "Bag Version"
    _bag_version_number = b'1.5.3'
    _bag_elevation = "BAG_root/elevation"
    _bag_elevation_min_ev = "Minimum Elevation Value"
    _bag_elevation_max_ev = "Maximum Elevation Value"
    _bag_metadata = "BAG_root/metadata"
    _bag_tracking_list = "BAG_root/tracking_list"
    _bag_tracking_list_len = "Tracking List Length"
    _bag_tracking_list_type = np.dtype([('Row', np.uint32), ('Col', np.uint32),
                                        ('Depth', np.float32), ('Uncertainty', np.float32),
                                        ('track_code', np.byte), ('list_series', np.uint16)])
    _bag_uncertainty = "BAG_root/uncertainty"
    _bag_uncertainty_min_uv = "Minimum Uncertainty Value"
    _bag_uncertainty_max_uv = "Maximum Uncertainty Value"
    _bag_nan = 1000000

    def __init__(self, name, mode=None, driver=None,
                 libver=None, userblock_size=None, swmr=False, **kwds):
        """
        Create a new file object.

        See the low level bag.File for a detailed explanation of the options.
        """
        if mode is not None:
            if 'w' not in mode:
                if not is_bag(name):
                    raise BAGError("The passed file %s is not a BAG file")

        super(BAGFile, self).__init__(name=name, mode=mode, driver=driver,
                                      libver=libver, userblock_size=userblock_size, swmr=swmr, **kwds)

        self.meta = None

    @classmethod
    def create_template(cls, name):
        """ create a BAG file with empty template structure """
        log.debug("create new BAG file: %s" % name)
        try:
            new_bag = File(name, 'w')
            new_bag.create_group(cls._bag_root)
            new_bag.attrs.create(cls._bag_version, cls._bag_version_number, shape=(), dtype="S5")

            elevation = new_bag.create_dataset(cls._bag_elevation, shape=(), dtype=np.float32)
            elevation.attrs.create(cls._bag_elevation_min_ev, 0.0, shape=(), dtype=np.float32)
            elevation.attrs.create(cls._bag_elevation_max_ev, 0.0, shape=(), dtype=np.float32)

            new_bag.create_dataset(cls._bag_metadata, shape=(1, ), dtype="S1")

            tracking_list = new_bag.create_dataset(cls._bag_tracking_list, shape=(), dtype=cls._bag_tracking_list_type)
            tracking_list.attrs.create(cls._bag_tracking_list_len, 0, shape=(), dtype=np.uint32)

            uncertainty = new_bag.create_dataset(cls._bag_uncertainty, shape=(), dtype=np.float32)
            uncertainty.attrs.create(cls._bag_uncertainty_min_uv, 0.0, shape=(), dtype=np.float32)
            uncertainty.attrs.create(cls._bag_uncertainty_max_uv, 0.0, shape=(), dtype=np.float32)

        except (BAGError, OSError) as e:
            raise BAGError("Unable to create the BAG file %s: %s" % (name, e))

        return new_bag

    def elevation(self, mask_nan=True):
        """
        Return the elevation as numpy array

        mask_nan
            If True, apply a mask using the BAG nan value
        """
        if mask_nan:
            el = self[BAGFile._bag_elevation][:]
            mask = el == BAGFile._bag_nan
            el[mask] = np.nan
            return el

        return self[BAGFile._bag_elevation][:]

    def uncertainty(self, mask_nan=True):
        """
        Return the uncertainty as numpy array

        mask_nan
            If True, apply a mask using the BAG nan value
        """
        if mask_nan:
            el = self[BAGFile._bag_uncertainty][:]
            mask = el == BAGFile._bag_nan
            el[mask] = np.nan
            return el

        return self[BAGFile._bag_uncertainty][:]

    def tracking_list(self):
        """ Return the tracking list as numpy array """
        return self[BAGFile._bag_tracking_list][:]

    def metadata(self, as_string=True, as_pretty_xml=True):
        """
        Return the metadata

        as_string
            If True, convert the metadata from a dataset of characters to a string
        """
        if as_string and not as_pretty_xml:
            try:
                return self[BAGFile._bag_metadata][:].tostring()
            except RuntimeError as e:
                log.info("exception raised: %s" % e)
                return None
        if as_pretty_xml:
            try:
                xml_tree = etree.fromstring(self[BAGFile._bag_metadata][:].tostring())
                return etree.tostring(xml_tree, pretty_print=True)
            except RuntimeError as e:
                log.info("exception raised: %s" % e)
                return None

        return self[BAGFile._bag_metadata][:]

    def extract_metadata(self, name=None):
        """
        Save metadata on disk

        name
            The file path where the metadata will be save. If None, "BAG_metadata.xml"
        """

        meta_xml = self.metadata(as_pretty_xml=True)
        if meta_xml is None:
            log.info("unable to access the metadata")
            return

        if name is None:
            name = os.path.join("BAG_metadata.xml")

        with open(os.path.abspath(name), 'w') as fid:
            fid.write(meta_xml)

    def populate_metadata(self):
        """ Populate metadata class """

        if self.meta is not None:
            log.debug("metadata already populated")
            return

        self.meta = Meta(meta_xml=self.metadata(as_pretty_xml=True))

    def __str__(self):
        output = super(BAGFile, self).__str__()

        output += "<BAG root>"
        output += "\n  <elevation shape=%s>" % str(self.elevation().shape)
        output += "\n  <uncertainty shape=%s>" % str(self.uncertainty().shape)
        output += "\n  <tracking list shape=%s>" % str(self.tracking_list().shape)

        if self.meta is not None:
            output += "\n  %s" % str(self.meta)

        return output
