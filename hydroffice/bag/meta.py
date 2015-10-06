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
        xml_tree = etree.fromstring(meta_xml)

        try:
            ret = xml_tree.xpath('/gmi:MI_Metadata/gmd:spatialRepresentationInfo/gmd:MD_Georectified/'
                                 'gmd:axisDimensionProperties/gmd:MD_Dimension/gmd:dimensionSize/gco:Integer',
                                 namespaces=self.ns)
            self.rows = int(ret[0].text)
            self.cols = int(ret[1].text)

        except (ValueError, etree.Error) as e:
            log.warning("unable to read rows and cols: %s" % e)
            self.rows = None
            self.cols = None

        try:
            ret = xml_tree.xpath('/gmi:MI_Metadata/gmd:spatialRepresentationInfo/gmd:MD_Georectified/'
                                 'gmd:axisDimensionProperties/gmd:MD_Dimension/gmd:resolution/gco:Measure',
                                 namespaces=self.ns)
            self.res_x = float(ret[0].text)
            self.res_y = float(ret[1].text)

        except (ValueError, etree.Error) as e:
            log.warning("unable to read x and y resolutions: %s" % e)
            self.res_x = None
            self.res_y = None

        try:
            ret = xml_tree.xpath('/gmi:MI_Metadata/gmd:spatialRepresentationInfo/gmd:MD_Georectified/'
                                 'gmd:cornerPoints/gml:Point/gml:coordinates',
                                 namespaces=self.ns)[0].text.split()
            self.sw = [float(c) for c in ret[0].split(',')]
            self.ne = [float(c) for c in ret[1].split(',')]

        except (ValueError, etree.Error) as e:
            log.warning("unable to read SW and NE corners: %s" % e)
            self.sw = None
            self.ne = None

        try:
            ret = xml_tree.xpath('/gmi:MI_Metadata/gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/'
                                 'gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString',
                                 namespaces=self.ns)
            self.prj_coord_sys = ret[0].text

        except (ValueError, etree.Error) as e:
            log.warning("unable to read SW and NE corners: %s" % e)
            self.prj_coord_sys = None

    def __str__(self):
        output = "<metadata>"

        if (self.rows is not None) and (self.cols is not None):
            output += "\n    <shape rows=%d, cols=%d>" % (self.rows, self.cols)

        if (self.res_x is not None) and (self.res_y is not None):
            output += "\n    <resolution x=%f, y=%f>" % (self.res_x, self.res_y)

        if (self.sw is not None) and (self.ne is not None):
            output += "\n    <corners SW=%s, NE=%s>" % (self.sw, self.ne)

        if self.prj_coord_sys is not None:
            output += "\n    <projection=%s>" % Helper.elide(self.prj_coord_sys, max_len=60)

        return output
