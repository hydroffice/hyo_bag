from __future__ import absolute_import, division, print_function, unicode_literals

import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # change to WARNING to reduce verbosity, DEBUG for high verbosity
ch_formatter = logging.Formatter('%(levelname)-9s %(name)s.%(funcName)s:%(lineno)d > %(message)s')
ch.setFormatter(ch_formatter)
logger.addHandler(ch)


from hydroffice.bag.base import is_bag, File
from hydroffice.bag.helper import Helper, BAGError


file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_00.bag")
if os.path.exists(file_bag_0):
    print("- file_bag_0: %s is BAG? %r" % (file_bag_0, is_bag(file_bag_0)))

file_bag_1 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(file_bag_1):
    print("- file_bag_1: %s is BAG? %r" % (file_bag_1, is_bag(file_bag_1)))

file_fake_0 = os.path.join(Helper.samples_folder(), "fake_00.bag")
if os.path.exists(file_fake_0):
    print("- file_fake_0: %s is BAG? %r" % (file_fake_0, is_bag(file_fake_0)))

bag_0 = File(file_bag_0)
print(bag_0)
print(bag_0.attrs['/'])
bag_0.flush()
bag_0.close()
print(bag_0)

bag_1 = File(file_bag_1)
bag_1.flush()
bag_1.close()

try:
    fake_0 = File(file_fake_0)
except BAGError:
    print("Expected exception")



