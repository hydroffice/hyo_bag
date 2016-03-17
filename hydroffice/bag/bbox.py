from __future__ import absolute_import, division, print_function, unicode_literals

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
        'gjs': [b"GeoJSON", "bag.geojson"],
        'gml': [b"GML", "bag.gml"],
        'kml': [b"KML", "bag.kml"],
        'shp': [b"ESRI Shapefile", "bag.shp"],
    }

    def __init__(self, bag_meta, fmt="kml", title=None, out_file=None):
        assert isinstance(bag_meta, Meta)
        self.bag_meta = bag_meta
        if not self.bag_meta.valid_bbox():
            raise BAGError("invalid bbox read in BAG metadata")

        self.title = title
        if self.title is None:
            self.title = "Metadata"
        log.debug("title: %s" % self.title)

        # get the ogr driver
        self.drv = ogr.GetDriverByName(self.formats[fmt][0])
        if self.drv is None:
            raise BAGError("%s driver not available.\n" % self.formats[fmt][0])

        # set the output file
        self.out_file = out_file
        if self.out_file is None:
            self.out_file = os.path.abspath(self.formats[fmt][1])
            log.debug("output: %s" % self.out_file)

        if os.path.exists(self.out_file):
            os.remove(self.out_file)

        # create the data source
        ds = self.drv.CreateDataSource(self.out_file)

        # create the spatial reference (WGS84)
        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(4326)

        # create the layer
        self.lyr = ds.CreateLayer(b"BAG", self.srs, ogr.wkbLineString25D)
        self._define_layer_fields()

        # add feature
        self._add_feature()

        ds.Destroy()

    def _define_layer_fields(self):

        # Add the fields we're interested in
        self.lyr.CreateField(ogr.FieldDefn(b"Name", ogr.OFTString))
        if self.bag_meta.rows is not None:
            self.lyr.CreateField(ogr.FieldDefn(b"Rows", ogr.OFTInteger))
        if self.bag_meta.cols is not None:
            self.lyr.CreateField(ogr.FieldDefn(b"Cols", ogr.OFTInteger))
        if self.bag_meta.ne is not None:
            self.lyr.CreateField(ogr.FieldDefn(b"NE", ogr.OFTString))
        if self.bag_meta.sw is not None:
            self.lyr.CreateField(ogr.FieldDefn(b"SW", ogr.OFTString))
        if self.bag_meta.res_x is not None:
            self.lyr.CreateField(ogr.FieldDefn(b"ResX", ogr.OFTReal))
        if self.bag_meta.res_y is not None:
            self.lyr.CreateField(ogr.FieldDefn(b"ResY", ogr.OFTReal))
        if self.bag_meta.abstract is not None:
            self.lyr.CreateField(ogr.FieldDefn(b"Abstract", ogr.OFTString))
        if self.bag_meta.date is not None:
            self.lyr.CreateField(ogr.FieldDefn(b"Date", ogr.OFTString))
        if self.bag_meta.wkt_srs is not None:
            self.lyr.CreateField(ogr.FieldDefn(b"SRS", ogr.OFTString))
        self.lyr.CreateField(ogr.FieldDefn(b"Tools", ogr.OFTString))

    def _add_feature(self):
        # create the WKT for the feature using Python string formatting
        feature = ogr.Feature(self.lyr.GetLayerDefn())
        feature.SetField(b"Name", self.title.encode())
        if self.bag_meta.rows is not None:
            feature.SetField(b"Rows", self.bag_meta.rows)
        if self.bag_meta.cols is not None:
            feature.SetField(b"Cols", self.bag_meta.cols)
        if self.bag_meta.ne is not None:
            feature.SetField(b"NE", ("%s" % self.bag_meta.ne).encode())
        if self.bag_meta.sw is not None:
            feature.SetField(b"SW", ("%s" % self.bag_meta.sw).encode())
        if self.bag_meta.res_x is not None:
            feature.SetField(b"ResX", ("%s" % self.bag_meta.res_x).encode())
        if self.bag_meta.res_y is not None:
            feature.SetField(b"ResY", ("%s" % self.bag_meta.res_y).encode())
        if self.bag_meta.abstract is not None:
            feature.SetField(b"Abstract", self.bag_meta.abstract)
        if self.bag_meta.date is not None:
            feature.SetField(b"Date", self.bag_meta.date)
        if self.bag_meta.wkt_srs is not None:
            feature.SetField(b"SRS", Helper.elide(self.bag_meta.wkt_srs, max_len=60).encode())
        feature.SetField(b"Tools", ("r%s" % __version__).encode())
        wkt = self.bag_meta.wkt_bbox()
        # log.debug("bbox: %s" % wkt)
        point = ogr.CreateGeometryFromWkt(wkt)
        feature.SetGeometry(point)
        self.lyr.CreateFeature(feature)
        feature.Destroy()

