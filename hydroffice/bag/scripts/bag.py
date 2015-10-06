from __future__ import absolute_import, division, print_function, unicode_literals

import os
import logging
from matplotlib import pyplot as plt

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # change to WARNING to reduce verbosity, DEBUG for high verbosity
ch_formatter = logging.Formatter('%(levelname)-9s %(name)s.%(funcName)s:%(lineno)d > %(message)s')
ch.setFormatter(ch_formatter)
logger.addHandler(ch)

from hydroffice.bag import BAGFile
from hydroffice.bag import BAGError
from hydroffice.bag.helper import Helper

file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_00.bag")
if os.path.exists(file_bag_0):
    print("- file_bag_0: %s" % file_bag_0)

bag_0 = BAGFile(file_bag_0)
print(bag_0)

print(type(bag_0.elevation(mask_nan=True)), bag_0.elevation(mask_nan=True).shape, bag_0.elevation(mask_nan=True).dtype)
# plt.contourf(bag_0.elevation(mask_nan=True))
# plt.show()

print(type(bag_0.uncertainty(mask_nan=True)), bag_0.uncertainty(mask_nan=True).shape, bag_0.uncertainty(mask_nan=True).dtype)
# plt.contourf(bag_0.uncertainty(mask_nan=True))
# plt.show()

print(type(bag_0.metadata()), len(bag_0.metadata()))
file_bag_0_xml = os.path.join("bdb_00.bag.xml")
bag_0.extract_metadata(name=file_bag_0_xml)

bag_0.populate_metadata()
print("rows, cols: %d, %d" % (bag_0.meta.rows, bag_0.meta.cols))
print("res x, y: %f, %f" % (bag_0.meta.res_x, bag_0.meta.res_y))
print("corner SW, NE: %s, %s" % (bag_0.meta.sw, bag_0.meta.ne))
print("coord sys: %s" % bag_0.meta.prj_coord_sys)

print(bag_0)

file_bag_1 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(file_bag_1):
    print("- file_bag_1: %s" % file_bag_1)

file_bag_2 = os.path.abspath(os.path.join("test_00.bag"))
print("- file_bag_2: %s" % file_bag_2)

bag_2 = BAGFile.create_template(file_bag_2)
bag_2.close()

# if os.path.exists(file_bag_2):
#     os.remove(file_bag_2)



