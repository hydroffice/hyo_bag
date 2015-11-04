from __future__ import absolute_import, division, print_function  # , unicode_literals

import os
import logging

log = logging.getLogger(__name__)

from osgeo import ogr, osr
from .meta import Meta
from .helper import BAGError, Helper
from . import __version__

ogr.UseExceptions()


class Bbox2Gdal(object):

    formats = {
        'gjs': ["GeoJSON", "bag.geojson"],
        'gml': ["GML", "bag.gml"],
        'kml': ["KML", "bag.kml"],
        'shp': ["ESRI Shapefile", "bag.shp"],
    }

    def __init__(self, bag_meta, fmt="kml", title=None, kml_file=None):
        assert isinstance(bag_meta, Meta)

        if not bag_meta.valid_bbox():
            raise BAGError("invalid bbox read in BAG metadata")

        self.title = title
        if self.title is None:
            self.title = "Metadata"

        # get the ogr driver
        drv = ogr.GetDriverByName(self.formats[fmt][0])
        if drv is None:
            raise BAGError("%s driver not available.\n" % self.formats[fmt][0])

        # set the output file
        self.kml_file = kml_file
        if self.kml_file is None:
            self.kml_file = os.path.abspath(self.formats[fmt][1])
            log.debug("output: %s" % self.kml_file)

        if os.path.exists(self.kml_file):
            os.remove(self.kml_file)

        # create the data source
        ds = drv.CreateDataSource(self.kml_file)

        # create the spatial reference (WGS84)
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)

        # create the layer
        lyr = ds.CreateLayer("BAG", srs, ogr.wkbLineString25D)

        # Add the fields we're interested in
        lyr.CreateField(ogr.FieldDefn("Name", ogr.OFTString))
        if bag_meta.rows is not None:
            lyr.CreateField(ogr.FieldDefn("Rows", ogr.OFTInteger))
        if bag_meta.cols is not None:
            lyr.CreateField(ogr.FieldDefn("Cols", ogr.OFTInteger))
        if bag_meta.abstract is not None:
            lyr.CreateField(ogr.FieldDefn("Abstract", ogr.OFTString))
        if bag_meta.date is not None:
            lyr.CreateField(ogr.FieldDefn("Date", ogr.OFTString))
        if bag_meta.wkt_srs is not None:
            lyr.CreateField(ogr.FieldDefn("SRS", ogr.OFTString))
        lyr.CreateField(ogr.FieldDefn("Tools", ogr.OFTString))

        # create the WKT for the feature using Python string formatting
        feature = ogr.Feature(lyr.GetLayerDefn())
        feature.SetField("Name", self.title)
        if bag_meta.rows is not None:
            feature.SetField("Rows", bag_meta.rows)
        if bag_meta.cols is not None:
            feature.SetField("Cols", bag_meta.cols)
        if bag_meta.abstract is not None:
            feature.SetField("Abstract", bag_meta.abstract)
        if bag_meta.date is not None:
            feature.SetField("Date", bag_meta.date)
        if bag_meta.wkt_srs is not None:
            feature.SetField("SRS", Helper.elide(bag_meta.wkt_srs, max_len=60))
        feature.SetField("Tools", "r%s" % __version__)
        wkt = bag_meta.wkt_bbox()
        log.debug("bbox: %s" % wkt)
        point = ogr.CreateGeometryFromWkt(wkt)
        feature.SetGeometry(point)
        lyr.CreateFeature(feature)
        feature.Destroy()

        ds.Destroy()
