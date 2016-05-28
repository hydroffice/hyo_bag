from __future__ import absolute_import, division, print_function  # , unicode_literals

import os
import sys
import logging
import numpy as np
import h5py
from lxml import etree

log = logging.getLogger(__name__)

from .base import is_bag, File
from .helper import BAGError, Helper
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
    _bag_tracking_list_type = np.dtype([('row', np.uint32), ('col', np.uint32),
                                        ('depth', np.float32), ('uncertainty', np.float32),
                                        ('track_code', np.byte), ('list_series', np.uint16)])
    _bag_uncertainty = "BAG_root/uncertainty"
    _bag_uncertainty_min_uv = "Minimum Uncertainty Value"
    _bag_uncertainty_max_uv = "Maximum Uncertainty Value"
    BAG_NAN = 1000000

    default_metadata_file = "BAG_metadata.xml"

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
        self.meta_errors = list()
        self._str = None

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

    def elevation(self, mask_nan=True, row_range=None):
        """
        Return the elevation as numpy array

        mask_nan
            If True, apply a mask using the BAG nan value
        row_range
            If present, a slice of rows to read from
        """
        if row_range:
            if not isinstance(row_range, slice):
                raise BAGError("Invalid type of slice selector: %s" % type(row_range))
            if (row_range.start < 0) or (row_range.start >= self.elevation_shape()[0]) \
                    or (row_range.stop < 0) or (row_range.stop > self.elevation_shape()[0]) \
                    or (row_range.start > row_range.stop):
                raise BAGError("Invalid values for slice selector: %s" % row_range)

        if mask_nan:
            if row_range:
                el = self[BAGFile._bag_elevation][row_range]
            else:
                el = self[BAGFile._bag_elevation][:]
            mask = el == BAGFile.BAG_NAN
            el[mask] = np.nan
            return el

        if slice:
            return self[BAGFile._bag_elevation][row_range]
        else:
            return self[BAGFile._bag_elevation][:]

    def elevation_shape(self):
        return self[BAGFile._bag_elevation].shape

    def uncertainty(self, mask_nan=True, row_range=None):
        """
        Return the uncertainty as numpy array

        mask_nan
            If True, apply a mask using the BAG nan value
        row_range
            If present, a slice of rows to read from
        """
        if row_range:
            if not isinstance(row_range, slice):
                raise BAGError("Invalid type of slice selector: %s" % type(row_range))
            if (row_range.start < 0) or (row_range.start >= self.uncertainty_shape()[0]) \
                    or (row_range.stop < 0) or (row_range.stop > self.uncertainty_shape()[0]) \
                    or (row_range.start > row_range.stop):
                raise BAGError("Invalid values for slice selector: %s" % row_range)

        if mask_nan:
            if row_range:
                un = self[BAGFile._bag_uncertainty][row_range]
            else:
                un = self[BAGFile._bag_uncertainty][:]
            mask = un == BAGFile.BAG_NAN
            un[mask] = np.nan
            return un

        if slice:
            return self[BAGFile._bag_uncertainty][row_range]
        else:
            return self[BAGFile._bag_uncertainty][:]

    def uncertainty_shape(self):
        return self[BAGFile._bag_uncertainty].shape

    def tracking_list(self):
        """ Return the tracking list as numpy array """
        return self[BAGFile._bag_tracking_list][:]

    def tracking_list_fields(self):
        """ Return the tracking list field names """
        return self[BAGFile._bag_tracking_list].dtype.names

    def metadata(self, as_string=True, as_pretty_xml=True):
        """ Return the metadata

        as_string
            If True, convert the metadata from a dataset of characters to a string
        as_pretty_xml
            If True, return the xml in a pretty format
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
        """ Save metadata on disk

        name
            The file path where the metadata will be saved. If None, use a default name.
        """

        meta_xml = self.metadata(as_pretty_xml=True)
        if meta_xml is None:
            log.info("unable to access the metadata")
            return

        if name is None:
            name = os.path.join(self.default_metadata_file)

        with open(os.path.abspath(name), 'w') as fid:
            fid.write(meta_xml)

    def validate_metadata(self):
        """ Validate metadata based on XML Schemas and schematron. """
        # clean metadata error list
        self.meta_errors = list()
        # assuming a valid BAG
        is_valid = True

        try:
            xml_tree = etree.fromstring(self.metadata(as_pretty_xml=True))
        except etree.Error as e:
            log.warning("unabled to parse XML metadata: %s" % e)
            self.meta_errors.append(e.message)
            return False

        try:
            schema_path = os.path.join(Helper.iso19139_folder(), 'bag', 'bag.xsd')
            schema_doc = etree.parse(schema_path)
            schema = etree.XMLSchema(schema_doc)
        except etree.Error as e:
            log.warning("unabled to parse XML schema: %s" % e)
            self.meta_errors.append(e.message)
            return False

        try:
            schema.assertValid(xml_tree)
        except etree.DocumentInvalid as e:
            log.warning("invalid metadata based on XML schema: %s" % e)
            self.meta_errors.append(e.message)
            for i in schema.error_log:
                self.meta_errors.append(i)
            is_valid = False

        if is_valid:
            log.debug("xsd validated")

        try:
            schematron_path = os.path.join(Helper.iso19757_3_folder(), 'bag_metadata_profile.sch')
            schematron_doc = etree.parse(schematron_path)
        except etree.DocumentInvalid as e:
            log.warning("unabled to parse BAG schematron: %s" % e)
            self.meta_errors.append(e.message)
            return False

        try:
            from lxml import isoschematron
        except IOError as e:
            msg = "Unable to load lxml isoschematron files"
            log.warning("%s: %s" % (msg, e))
            self.meta_errors.append(e.message)
            return False

        try:
            schematron = isoschematron.Schematron(schematron_doc, store_report=True)
        except etree.DocumentInvalid as e:
            log.warning("unabled to load BAG schematron: %s" % e)
            self.meta_errors.append(e.message)
            return False

        if schematron.validate(xml_tree):
            log.debug("schematron validated")
        else:
            log.warning("invalid metadata based on Schematron")
            is_valid = False
            ns = {
                'svrl': 'http://purl.oclc.org/dsdl/svrl',
            }
            for i in schematron.error_log:
                err_tree = etree.fromstring(i.message)
                # print(etree.tostring(err_tree, pretty_print=True))
                err_msg = err_tree.xpath('/svrl:failed-assert/svrl:text', namespaces=ns)[0].text.strip()
                log.warning(err_msg)
                self.meta_errors.append(err_msg)

        return is_valid

    def validation_info(self):
        """ Return a message string with the result of the validation """
        msg = str()

        msg += "XML input source: %s\nValidation output: " % self._bag_metadata
        if self.validate_metadata():
            msg += "VALID"
        else:
            msg += "INVALID\nReasons:\n"
            for err_msg in self.meta_errors:
                msg += " - %s\n" % err_msg
        return msg

    def populate_metadata(self):
        """ Populate metadata class """

        if self.meta is not None:
            # log.debug("metadata already populated")
            return self.meta

        self.meta = Meta(meta_xml=self.metadata(as_pretty_xml=True))
        return self.meta

    def _str_group_info(self, grp):
        if grp == self._bag_root:
            self._str += "  <root>\n"
        elif grp == self._bag_elevation:
            self._str += "  <elevation shape=%s>\n" % str(self.elevation().shape)
        elif grp == self._bag_uncertainty:
            self._str += "  <uncertainty shape=%s>\n" % str(self.uncertainty().shape)
        elif grp == self._bag_tracking_list:
            self._str += "  <tracking list shape=%s>\n" % str(self.tracking_list().shape)
        elif grp == self._bag_metadata:
            if self.meta is not None:
                self._str += "  %s\n" % str(self.meta)
            else:
                self._str += "  <%s>\n" % grp
        else:
            self._str += "  <%s>\n" % grp

        if grp != self._bag_metadata:
            for atr in self[grp].attrs:
                atr_val = self[grp].attrs[atr]
                self._str += "    <%s: %s (%s, %s)>\n" % (atr, atr_val, atr_val.shape, atr_val.dtype)

    def __str__(self):
        self._str = super(BAGFile, self).__str__()
        self.visit(self._str_group_info)
        return self._str
