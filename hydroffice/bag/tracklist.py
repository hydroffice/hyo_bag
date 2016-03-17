from __future__ import absolute_import, division, print_function, unicode_literals

import os
import logging

log = logging.getLogger(__name__)

import numpy as np
from .meta import Meta
from .helper import BAGError, Helper
from . import __version__


class TrackList2Csv(object):

    default_csv_name = "BAG.tracklist.csv"

    def __init__(self, track_list, csv_file=None, header=None, comment=None):
        assert isinstance(track_list, np.ndarray)
        log.debug("track list shape: %s" % track_list.shape)
        log.debug("track list size: %s" % track_list.size)

        self.track_list = track_list
        if self.track_list.size == 0:
            log.warning("nothing to export since the tracking list is empty")
            return

        self.csv_file = csv_file
        if csv_file is None:
            self.csv_file = self.default_csv_name
        self.csv_file = os.path.abspath(self.csv_file)
        log.debug("output: %s" % self.csv_file)

        self.header = header
        if self.header is None:
            self.header = str()
        if type(self.header) is tuple:
            self.header = bytes(",".join(fld for fld in self.header))
        log.debug("header: %s" % self.header)

        self.comment = comment
        if self.comment is None:
            self.comment = "# Exported using BAG tools r%s\n" % bytes(__version__)
        self.comment = self.comment.encode("utf-8")
        log.debug("comment: %s" % self.comment)

        np.savetxt(fname=self.csv_file, X=track_list, fmt=b'%.7g', delimiter=b',',
                   header=self.header, comments=self.comment)
