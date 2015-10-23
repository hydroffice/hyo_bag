from __future__ import absolute_import, division, print_function, unicode_literals

import os

import wx

import logging
log = logging.getLogger(__name__)

from hdf_compass import utils
from hdf_compass.compass_viewer import frame
from hdf_compass import compass_model
from hydroffice import bag


ID_ABOUT_BAG = wx.NewId()
ID_OPEN_SAMPLES = wx.NewId()


frame.BaseFrame.icon_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'media'))


class InitFrame(frame.InitFrame):
    """ Frame displayed when the application starts up. """

    icon_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'media'))

    def __init__(self):
        super(InitFrame, self).__init__()
        self.SetTitle("BAG Explorer [HDF Compass with BAG plugin]")

        for m in self.GetMenuBar().GetMenus():
            if m[1] == '&File':
                m[0].Insert(2, ID_OPEN_SAMPLES, "Open &Samples\tCtrl-S", "Open data samples")
            if m[1] == '&Help':
                m[0].Append(ID_ABOUT_BAG, "&About BAG plugin", "Information about the BAG plugin")


        self.Bind(wx.EVT_MENU, self.on_open_samples, id=ID_OPEN_SAMPLES)
        self.Bind(wx.EVT_MENU, self.on_about_bag, id=ID_ABOUT_BAG)

    def on_about_bag(self, evt):
        """ Display an "About" dialog """
        from hdf_compass import bag_model

        description = """
        Plugin for Open Navigation Surface BAG files,
        using hydroffice.bag v.%s

        2015 (c) Masetti,Calder (CCOM/JHC,UNH)
        """ % bag.__version__

        info = wx.AboutDialogInfo()
        info.Name = "BAG plugin"
        info.Version = bag_model.__version__
        info.Licence = """
        BSD-like license.
        Refer to the documentation
        for the full license.
        """
        info.SetDescription(description)
        info.SetIcon(wx.Icon(os.path.join(self.icon_folder, 'BAGExplorer_128.png')))
        info.SetWebSite("https://bitbucket.org/ccomjhc/hyo_bag")
        wx.AboutBox(info)

    def on_file_open(self, evt):
        """ Request to open a file via the Open entry in the File menu """

        def make_filter_string():
            """ Make a wxPython dialog filter string segment from dict """
            filter_string = []
            hdf_filter_string = []  # put HDF filters in the front
            for store in compass_model.get_stores():
                if len(store.file_extensions) == 0:
                    continue
                for key in store.file_extensions:
                    s = "{name} ({pattern_c})|{pattern_sc}".format(
                        name=key,
                        pattern_c=",".join(store.file_extensions[key]),
                        pattern_sc=";".join(store.file_extensions[key]) )
                    if s.startswith("BAG"):
                        hdf_filter_string.append(s)
                    else:
                        filter_string.append(s)
            filter_string = hdf_filter_string + filter_string
            filter_string.append('All Files (*.*)|*.*')
            pipe = "|"
            return pipe.join(filter_string)

        wc_string = make_filter_string()

        dlg = wx.FileDialog(self, "Open Local File", wildcard=wc_string, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() != wx.ID_OK:
            return
        path = dlg.GetPath()

        url = utils.path2url(path)
        self.open_url(url)

    def on_open_samples(self, evt):
        """ Request to open a file via the Open entry in the File menu """
        def make_filter_string():
            """ Make a wxPython dialog filter string segment from dict """
            filter_string = []
            hdf_filter_string = []  # put HDF filters in the front
            for store in compass_model.get_stores():
                if len(store.file_extensions) == 0:
                    continue
                for key in store.file_extensions:
                    s = "{name} ({pattern_c})|{pattern_sc}".format(
                        name=key,
                        pattern_c=",".join(store.file_extensions[key]),
                        pattern_sc=";".join(store.file_extensions[key]) )
                    if s.startswith("BAG"):
                        hdf_filter_string.append(s)
                    else:
                        filter_string.append(s)
            filter_string = hdf_filter_string + filter_string
            filter_string.append('All Files (*.*)|*.*')
            pipe = "|"
            return pipe.join(filter_string)

        wc_string = make_filter_string()

        samples_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "bag", "samples"))
        if os.path.exists(samples_dir):
            log.debug("samples folder: %s" % samples_dir)
        else:
            log.warning("missing samples folder: %s" % samples_dir)
        dlg = wx.FileDialog(self, "Open Samples Folder", defaultDir=samples_dir, wildcard=wc_string,
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() != wx.ID_OK:
            return
        path = dlg.GetPath()

        url = utils.path2url(path)
        self.open_url(url)

