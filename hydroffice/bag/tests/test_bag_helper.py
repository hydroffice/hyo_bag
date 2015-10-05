from __future__ import absolute_import, division, print_function, unicode_literals

import pytest


class TestHyOError(object):

    from hydroffice.bag.helper import BAGError
    err = BAGError("test")

    def test_is_instance(self):
        assert isinstance(self.err, Exception)

    def test_raise(self):
        from hydroffice.bag.helper import BAGError
        try:
            raise self.err
        except BAGError as e:
            assert "test" in str(e)

    def test_has_message(self):
        assert hasattr(self.err, 'message')
