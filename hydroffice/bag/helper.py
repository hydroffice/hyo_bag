from __future__ import absolute_import, division, print_function, unicode_literals

import os
import logging

log = logging.getLogger(__name__)


class BAGError(Exception):
    """ BAG class for exceptions"""

    def __init__(self, message, *args):
        if isinstance(message, Exception):
            msg = message.args[0] if len(message.args) > 0 else ''
        else:
            msg = message

        self.message = msg
        # allow users initialize misc. arguments as any other builtin Error
        Exception.__init__(self, message, *args)


class Helper(object):
    @classmethod
    def samples_folder(cls):
        samples_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)), "samples")
        if not os.path.exists(samples_dir):
            raise BAGError("unable to find the samples folder: %s" % samples_dir)
        return samples_dir