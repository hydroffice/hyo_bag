from __future__ import absolute_import, division, print_function  # , unicode_literals

import os
import sys
import logging
import numpy as np
import h5py
from lxml import etree

log = logging.getLogger(__name__)

from .helper import Helper


class Meta(object):
    """ Helper class to manage BAG xml metadata. """

    ns = {
        'bag': 'http://www.opennavsurf.org/schema/bag',
        'gco': 'http://www.isotc211.org/2005/gco',
        'gmd': 'http://www.isotc211.org/2005/gmd',
        'gmi': 'http://www.isotc211.org/2005/gmi',
        'gml': 'http://www.opengis.net/gml/3.2',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    }

    def __init__(self, meta_xml):
        self.xml_tree = etree.fromstring(meta_xml)

        # rows and cols
        self.rows = None
        self.cols = None
        self._read_rows_and_cols()

        # resolution along x and y axes
        self.res_x = None
        self.res_y = None
        self._read_res_x_and_y()

        # corner SW and NE
        self.sw = None
        self.ne = None
        self._read_corners_sw_and_ne()

        # corner wkt projection
        self.wkt_srs = None
        self._read_wkt_prj()

        # bbox
        self.lon_min = None
        self.lon_max = None
        self.lat_min = None
        self.lat_max = None
        self._read_bbox()

        # abstract
        self.abstract = None
        self._read_abstract()

        # date
        self.date = None
        self._read_date()

    def __str__(self):
        output = "<metadata>"

        if (self.rows is not None) and (self.cols is not None):
            output += "\n    <shape rows=%d, cols=%d>" % (self.rows, self.cols)

        if (self.res_x is not None) and (self.res_y is not None):
            output += "\n    <resolution x=%f, y=%f>" % (self.res_x, self.res_y)

        if (self.sw is not None) and (self.ne is not None):
            output += "\n    <corners SW=%s, NE=%s>" % (self.sw, self.ne)

        if self.wkt_srs is not None:
            output += "\n    <projection=%s>" % Helper.elide(self.wkt_srs, max_len=60)

        if self.date is not None:
            output += "\n    <date=%s>" % self.date

        if self.abstract is not None:
            output += "\n    <abstract=%s>" % self.abstract

        output += "\n    <bbox>"
        if (self.lon_min is not None) and (self.lon_max is not None):
            output += "\n        <x min=%s, max=%s>" % (self.lon_min, self.lon_max)
        if (self.lat_min is not None) and (self.lat_max is not None):
            output += "\n        <y min=%s, max=%s>" % (self.lat_min, self.lat_max)

        return output

    def valid_bbox(self):
        return (self.lon_min is not None) and (self.lon_max is not None) and \
               (self.lat_min is not None) and (self.lat_max is not None)

    def geo_extent(self):
        """ Return the geographic extent as a tuple: (x_min, x_max, y_min, y_max) """
        return self.lon_min, self.lon_max, self.lat_min, self.lat_max

    def wkt_bbox(self):
        return "LINESTRING Z(%.6f %.6f 0, %.6f %.6f 0, %.6f %.6f 0, %.6f %.6f 0, %.6f %.6f 0)" \
               % (self.lon_min, self.lat_min, self.lon_min, self.lat_max, self.lon_max, self.lat_max, self.lon_max, self.lat_min,
                  self.lon_min, self.lat_min)

    def _read_rows_and_cols(self):
        """ attempts to read rows and cols info """

        try:
            ret = self.xml_tree.xpath('//*/gmd:spatialRepresentationInfo/gmd:MD_Georectified/'
                                      'gmd:axisDimensionProperties/gmd:MD_Dimension/gmd:dimensionSize/gco:Integer',
                                      namespaces=self.ns)
        except etree.Error as e:
            log.warning("unable to read rows and cols: %s" % e)
            return

        try:
            self.rows = int(ret[0].text)
            self.cols = int(ret[1].text)

        except (ValueError, IndexError) as e:
            log.warning("unable to read rows and cols: %s" % e)
            return

    def _read_res_x_and_y(self):
        """ attempts to read resolution along x- and y- axes """

        try:
            ret = self.xml_tree.xpath('//*/gmd:spatialRepresentationInfo/gmd:MD_Georectified/'
                                      'gmd:axisDimensionProperties/gmd:MD_Dimension/gmd:resolution/gco:Measure',
                                      namespaces=self.ns)
        except etree.Error as e:
            log.warning("unable to read res x and y: %s" % e)
            return

        try:
            self.res_x = float(ret[0].text)
            self.res_y = float(ret[1].text)

        except (ValueError, IndexError) as e:
            log.warning("unable to read res x and y: %s" % e)
            return

    def _read_corners_sw_and_ne(self):
        """ attempts to read corners SW and NE """

        try:
            ret = self.xml_tree.xpath('//*/gmd:spatialRepresentationInfo/gmd:MD_Georectified/'
                                      'gmd:cornerPoints/gml:Point/gml:coordinates',
                                      namespaces=self.ns)[0].text.split()
        except etree.Error as e:
            log.warning("unable to read corners SW and NE: %s" % e)
            return

        try:
            self.sw = [float(c) for c in ret[0].split(',')]
            self.ne = [float(c) for c in ret[1].split(',')]

        except (ValueError, IndexError) as e:
            log.warning("unable to read corners SW and NE: %s" % e)
            return

    def _read_wkt_prj(self):
        """ attempts to read the WKT projection string """

        try:
            ret = self.xml_tree.xpath('//*/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/'
                                      'gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString',
                                      namespaces=self.ns)
        except etree.Error as e:
            log.warning("unable to read the WKT projection string: %s" % e)
            return

        try:
            self.wkt_srs = ret[0].text

        except (ValueError, IndexError) as e:
            log.warning("unable to read the WKT projection string: %s" % e)
            return

    def _read_bbox(self):
        """ attempts to read the bounding box values """

        try:
            ret_x_min = self.xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal',
                                            namespaces=self.ns)
            ret_x_max = self.xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal',
                                            namespaces=self.ns)
        except etree.Error as e:
            log.warning("unable to read the bbox's longitude values: %s" % e)
            return

        try:
            self.lon_min = float(ret_x_min[0].text)
            self.lon_max = float(ret_x_max[0].text)
        except (ValueError, IndexError) as e:
            log.warning("unable to read the bbox's longitude values: %s" % e)
            return

        try:
            ret_y_min = self.xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal',
                                            namespaces=self.ns)
            ret_y_max = self.xml_tree.xpath('//*/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal',
                                            namespaces=self.ns)
        except etree.Error as e:
            log.warning("unable to read the bbox's latitude values: %s" % e)
            return

        try:
            self.lat_min = float(ret_y_min[0].text)
            self.lat_max = float(ret_y_max[0].text)
        except (ValueError, IndexError) as e:
            log.warning("unable to read the bbox's latitude values: %s" % e)
            return

    def _read_abstract(self):
        """ attempts to read the abstract string """

        try:
            ret = self.xml_tree.xpath('//*/gmd:abstract/gco:CharacterString',
                                      namespaces=self.ns)
        except etree.Error as e:
            log.warning("unable to read the abstract string: %s" % e)
            return

        try:
            self.abstract = ret[0].text
        except (ValueError, IndexError) as e:
            log.warning("unable to read the abstract string: %s" % e)
            return

    def _read_date(self):
        """ attempts to read the date string """

        try:
            ret = self.xml_tree.xpath('//*/gmd:CI_Date/gmd:date/gco:Date',
                                      namespaces=self.ns)
        except etree.Error as e:
            log.warning("unable to read the date string: %s" % e)
            return

        try:
            text_date = ret[0].text
        except (ValueError, IndexError) as e:
            log.warning("unable to read the date string: %s" % e)
            return

        tm_date = None
        try:
            import dateutil.parser
            parsed_date = dateutil.parser.parse(text_date)
            tm_date = parsed_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        except Exception:
            log.warning("unable to handle the date string: %s" % text_date)

        if tm_date is None:
            self.date = text_date
        else:
            self.date = tm_date
