from __future__ import absolute_import, division, print_function, unicode_literals

import os
import logging

log = logging.getLogger(__name__)

import numpy as np

from osgeo import gdal, osr
from .meta import Meta
from .helper import BAGError, Helper
from . import __version__
from .bag import BAGFile

gdal.UseExceptions()


class Uncertainty2Gdal(object):

    formats = {
        'ascii': [b"AAIGrid", "bag.uncertainty.asc"],
        'geotiff': [b"GTiff", "bag.uncertainty.tif"],
        'xyz': [b"XYZ", "bag.uncertainty.xyz"],
    }

    def __init__(self, bag_uncertainty, bag_meta, fmt="geotiff", out_file=None):
        assert isinstance(bag_uncertainty, np.ndarray)
        assert isinstance(bag_meta, Meta)
        self.bag_unc = bag_uncertainty
        self.bag_meta = bag_meta

        # get the IN-MEMORY ogr driver
        self.mem = gdal.GetDriverByName(b"MEM")
        if self.mem is None:
            raise BAGError("%s driver not available.\n" % self.formats[fmt][0])
        log.debug("format: %s" % fmt)

        # set the output file
        self.out_file = out_file
        if self.out_file is None:
            self.out_file = os.path.abspath(self.formats[fmt][1])
            log.debug("output: %s" % self.out_file)

        if os.path.exists(self.out_file):
            os.remove(self.out_file)

        log.debug("dtype: %s" % self.bag_unc.dtype)
        self.rst = self.mem.Create(utf8_path=self.out_file, xsize=self.bag_meta.cols, ysize=self.bag_meta.rows,
                                   bands=1, eType=gdal.GDT_Float32)
        self.rst.SetGeoTransform((self.bag_meta.sw[0], self.bag_meta.res_x, 0,
                                  self.bag_meta.ne[1], 0, -self.bag_meta.res_y))

        self.bnd = self.rst.GetRasterBand(1)
        self.bnd.WriteArray(self.bag_unc[::-1])
        self.bnd.SetNoDataValue(BAGFile.BAG_NAN)
        self.srs = osr.SpatialReference()
        if self.bag_meta.wkt_srs is not None:
            self.srs.ImportFromWkt(self.bag_meta.wkt_srs)
        else:
            log.warning("unable to recover valid spatial reference info")
        self.rst.SetProjection(self.srs.ExportToWkt())
        self.bnd.FlushCache()

        # get the required ogr driver
        self.drv = gdal.GetDriverByName(self.formats[fmt][0])
        self.drv.CreateCopy(self.out_file, self.rst)
        self.rst = None
