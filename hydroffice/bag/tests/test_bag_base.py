from __future__ import absolute_import, division, print_function, unicode_literals

import pytest


class TestBagBase(object):

    from hydroffice.bag.helper import Helper
    import os

    file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_00.bag")
    file_bag_1 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
    file_fake_0 = os.path.join(Helper.samples_folder(), "fake_00.bag")

    def test_bag_is_bag(self):
        from hydroffice.bag.base import is_bag, File
        assert is_bag(self.file_bag_0) is True
        assert is_bag(self.file_bag_1) is True
        assert is_bag(self.file_fake_0) is False

    def test_bag_File_raise(self):
        from hydroffice.bag.base import is_bag, File
        from hydroffice.bag.helper import BAGError
        with pytest.raises(IOError):
            File(self.file_fake_0)

    def test_bag_File_open(self):
        from hydroffice.bag.base import is_bag, File
        from hydroffice.bag.helper import BAGError
        File(self.file_bag_0)
        File(self.file_bag_1)

    def test_bag_File_filename(self):
        import os
        from hydroffice.bag.base import is_bag, File
        from hydroffice.bag.helper import BAGError
        bag_0 = File(self.file_bag_0)
        assert os.path.abspath(self.file_bag_0) == bag_0.filename
        bag_1 = File(self.file_bag_1)
        assert os.path.abspath(self.file_bag_1) == bag_1.filename
