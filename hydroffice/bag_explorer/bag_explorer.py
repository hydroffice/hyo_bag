from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
import cStringIO

import wx

from hdf_compass import compass_viewer
from hdf_compass import common
from hdf_compass.compass_viewer import frame
from hdf_compass.compass_viewer.viewer import load_plugins
from hydroffice.bag_explorer import bag_images
from hydroffice import bag

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

ID_ABOUT_BAG = wx.NewId()


class BagExplorerApp(compass_viewer.CompassApp):
    def __init__(self, redirect):
        """ Constructor.  If *redirect*, show a windows with console output."""
        super(BagExplorerApp, self).__init__(redirect=redirect)
        self.SetAppName("BAGExplorer")


def getbitmap(name):
    """ Return a wx.Bitmap of the given icon """
    png = getattr(bag_images, name)()
    return png_to_bitmap(png)


def png_to_bitmap(png):
    """ Convert a string with raw PNG data to a wx.Bitmap """
    stream = cStringIO.StringIO(png)
    img = wx.ImageFromStream(stream, wx.BITMAP_TYPE_PNG)
    return img.ConvertToBitmap()


class InitFrame(frame.BaseFrame):
    """
    Frame displayed when the application starts up.

    This includes the menu bar provided by TopFrame.  On the Mac, although it
    still exists (to prevent the application from exiting), the frame
    is typically not shown.
    """

    be_folder = os.path.abspath(os.path.dirname(__file__))

    def __init__(self):

        style = wx.DEFAULT_FRAME_STYLE & (~wx.RESIZE_BORDER) & (~wx.MAXIMIZE_BOX)
        title = "BAG Explorer [HDF Compass with BAG plugin]"
        super(InitFrame, self).__init__(size=(552, 247), title=title, style=style)

        for m in self.GetMenuBar().GetMenus():
            if m[1] == '&Help':
                m[0].Append(ID_ABOUT_BAG, "&About BAG plugin", "Information about the BAG plugin")

        self.Bind(wx.EVT_MENU, self.on_about_bag, id=ID_ABOUT_BAG)

        data = getbitmap('logo')
        bmp = wx.StaticBitmap(self, wx.ID_ANY, data)
        self.SetIcon(wx.Icon(os.path.join(self.be_folder, 'media', 'BAGExplorer_32.png')))

        if os.name == 'nt':
            # This is needed to display the app icon on the taskbar on Windows 7
            import ctypes
            app_id = 'BAG Explorer [HDF Compass v.%s]' % common.__version__
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


        # The init frame isn't visible on Mac, so there shouldn't be an
        # option to close it.  "Quit" does the same thing.
        if common.is_darwin:
            mb = self.GetMenuBar()
            mu = mb.GetMenu(0)
            mu.Enable(wx.ID_CLOSE, False)
        self.Center()

    def on_about_bag(self, evt):
        """ Display an "About" dialog """
        from hdf_compass import bag_model

        description = """
        A HDFCompass plugin for Open Navigation Surface (ONS-WG) BAG data files.
        For bugs and suggestions on this plugin, write to: gmasetti@ccom.unh.edu

        Using hydroffice.bag v.%s (c) 2015 G.Masetti, B.R.Calder (CCOM/JHC, UNH)
""" % bag.__version__

        info = wx.AboutDialogInfo()
        info.Name = "BAG plugin"
        info.Version = bag_model.__version__
        info.Licence = "BSD-like license. Refer to the documentation for the full license."
        info.Copyright = "(c) 2015 Giuseppe Masetti (CCOM/JHC, UNH)"
        info.SetDescription(description)
        info.SetIcon(wx.Icon(os.path.join(self.be_folder, 'media', 'BAGExplorer_128.png')))
        info.SetWebSite("https://bitbucket.org/ccomjhc/hyo_bag")
        wx.AboutBox(info)

    def on_file_open(self, evt):
        """ Request to open a file via the Open entry in the File menu """
        from hdf_compass import compass_model

        def make_filter_string():
            """ Make a wxPython dialog filter string segment from dict """
            filter_string = []
            bag_filter_string = []  # put BAG filters in the front
            for store in compass_model.get_stores():
                if len(store.file_extensions) == 0:
                    continue
                for key in store.file_extensions:
                    s = "{name} ({pattern_c})|{pattern_sc}".format(
                        name=key,
                        pattern_c=",".join(store.file_extensions[key]),
                        pattern_sc=";".join(store.file_extensions[key]) )
                    if s.startswith("BAG"):
                        bag_filter_string.append(s)
                    else:
                        filter_string.append(s)
            filter_string = bag_filter_string + filter_string
            filter_string.append('All Files (*.*)|*.*')
            pipe = "|"
            return pipe.join(filter_string)

        wc_string = make_filter_string()

        from hdf_compass.compass_viewer import open_store
        dlg = wx.FileDialog(self, "Open Local File", wildcard=wc_string, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() != wx.ID_OK:
            return
        path = dlg.GetPath()
        if common.is_win:
            url = 'file:///' + path
        else:
            url = 'file://' + path
        if not open_store(url):
            dlg = wx.MessageDialog(self, 'The following file could not be opened:\n\n%s' % path,
                                   'No handler for file', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def on_samples_open(self, evt):
        """ Request to open a file via the Open entry in the File menu """
        from hdf_compass import compass_model

        def make_filter_string():
            """ Make a wxPython dialog filter string segment from dict """
            filter_string = []
            bag_filter_string = []  # put BAG filters in the front
            for store in compass_model.get_stores():
                if len(store.file_extensions) == 0:
                    continue
                for key in store.file_extensions:
                    s = "{name} ({pattern_c})|{pattern_sc}".format(
                        name=key,
                        pattern_c=",".join(store.file_extensions[key]),
                        pattern_sc=";".join(store.file_extensions[key]) )
                    if s.startswith("BAG"):
                        bag_filter_string.append(s)
                    else:
                        filter_string.append(s)
            filter_string = bag_filter_string + filter_string
            filter_string.append('All Files (*.*)|*.*')
            pipe = "|"
            return pipe.join(filter_string)

        wc_string = make_filter_string()

        from hdf_compass.compass_viewer import open_store
        samples_dir = os.path.abspath(os.path.join(os.path.dirname(frame.__file__), os.pardir, "data"))
        if os.path.exists(samples_dir):
            log.debug("samples folder: %s" % samples_dir)
        else:
            log.warning("missing samples folder: %s" % samples_dir)
        dlg = wx.FileDialog(self, "Open Samples Folder", defaultDir=samples_dir, wildcard=wc_string,
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() != wx.ID_OK:
            return
        path = dlg.GetPath()
        if common.is_win:
            url = 'file:///' + path
        else:
            url = 'file://' + path
        if not open_store(url):
            dlg = wx.MessageDialog(self, 'The following file could not be opened:\n\n%s' % path,
                                   'No handler for file', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

def run():
    """ Run BAG Explorer.  Handles all command-line arguments, etc."""
    try:
        import faulthandler
        faulthandler.enable()
    except ImportError:
        pass

    log.debug('Start')
    load_plugins()
    app = BagExplorerApp(False)

    urls = sys.argv[1:]

    for url in urls:
        if "://" not in url:
            # assumed to be file path
            if common.is_win:
                url = 'file:///%s' % sys.path.abspath(url)
            else:
                url = 'file://%s' % sys.path.abspath(url)
        if not compass_viewer.open_store(url):
            log.warning('No handlers to open: %s' % url)

    f = InitFrame()

    if common.is_darwin:
        wx.MenuBar.MacSetCommonMenuBar(f.GetMenuBar())
    else:
        f.Show()

    app.MainLoop()
