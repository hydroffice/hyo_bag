import sys
import os
import cStringIO

import wx

from . import bag_images

import compass_viewer
#from compass_viewer import CompassApp, frame, open_store, platform
import bag_model
from hydroffice import bag


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


class InitFrame(compass_viewer.frame.BaseFrame):
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
                m[0].Append(ID_ABOUT_BAG, "&About BAG plugin"," Information about the BAG plugin")

        self.Bind(wx.EVT_MENU, self.on_about_bag, id=ID_ABOUT_BAG)

        data = getbitmap('logo')
        bmp = wx.StaticBitmap(self, wx.ID_ANY, data)
        self.SetIcon(wx.Icon(os.path.join(self.be_folder, 'media', 'BAGExplorer_32.png')))

        if os.name == 'nt':
            # This is needed to display the app icon on the taskbar on Windows 7
            import ctypes
            app_id = 'BAG Explorer [HDF Compass v.%s]' % compass_viewer.platform.VERSION
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


        # The init frame isn't visible on Mac, so there shouldn't be an
        # option to close it.  "Quit" does the same thing.
        if compass_viewer.platform.MAC:
            mb = self.GetMenuBar()
            mu = mb.GetMenu(0)
            mu.Enable(wx.ID_CLOSE, False)
        self.Center()

    def on_about_bag(self, evt):
        """ Display an "About" dialog """
        info = wx.AboutDialogInfo()
        info.Name = "BAG plugin"
        info.Version = bag_model.__version__
        info.Licence = """
            Copyright Notice and License Terms for
            bag_hdfc_plugin - BAG plugin for HDFCompass
            -----------------------------------------------------------------------------
            
            bag_hdfc_plugin
            Copyright 2015- by Giuseppe Masetti (CCOM, UNH).

            All rights reserved.

            Redistribution and use in source and binary forms, with or without
            modification, are permitted for any purpose (including commercial purposes)
            provided that the following conditions are met:

            1. Redistributions of source code must retain the above copyright notice,
               this list of conditions, and the following disclaimer.

            2. Redistributions in binary form must reproduce the above copyright notice,
               this list of conditions, and the following disclaimer in the documentation
               and/or materials provided with the distribution.

            3. In addition, redistributions of modified forms of the source or binary
               code must carry prominent notices stating that the original code was
               changed and the date of the change.

            4. All publications or advertising materials mentioning features or use of
               this software are asked, but not required, to acknowledge that it was
               developed by Giuseppe Masetti and credit the contributors.

            5. Neither the name of Giuseppe Masetti, nor the name of any Contributor may
               be used to endorse or promote products derived from this software
               without specific prior written permission from Giuseppe Masetti or the
               Contributor, respectively.

            DISCLAIMER:
            THIS SOFTWARE IS PROVIDED BY THE CCOM AND THE CONTRIBUTORS
            "AS IS" WITH NO WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED.  In no
            event shall Giuseppe Masetti or the Contributors be liable for any damages
            suffered by the users arising out of the use of this software, even if
            advised of the possibility of such damage."""

        info.Copyright = "(c) 2015 Giuseppe Masetti (CCOM, UNH)"
        info.SetDescription("An HDFCompass plugin for Open Navigation Surface (ONS-WG)\nBAG data files. "
                            "The plugin uses the BAG library v.%s" % bag.__version__)
        info.SetIcon(wx.Icon(os.path.join(self.be_folder, 'media', 'BAGExplorer_128.png')))
        wx.AboutBox(info)

    def on_file_open(self, evt):
        """ Request to open a file via the Open entry in the File menu """
        import compass_model

        def make_filter_string():
            """ Make a wxPython dialog filter string segment from dict """
            filter_string = []
            hdf_filter_string = []  # put BAG filters in the front
            for store in compass_model.getstores():
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

        from compass_viewer import open_store
        dlg = wx.FileDialog(self, "Open Local File", wildcard=wc_string, style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() != wx.ID_OK:
            return
        path = dlg.GetPath()
        url = 'file://'+path
        if not open_store(url):
            dlg = wx.MessageDialog(self, 'The following file could not be opened:\n\n%s' % path,
                               'No handler for file', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()


def run():
    """ Run BAG Explorer.  Handles all command-line arguments, etc."""

    # These are imported to register their classes with
    # compass_model.  We don't use them directly.
    import filesystem_model
    import array_model
    import hdf5_model
    import asc_model

    # These are imported to register their classes with compass_model

    app = BagExplorerApp(False)

    urls = sys.argv[1:]

    for url in sys.argv[1:]:
        if "://" not in url:
            # assumed to be file path
            url = 'file://' + sys.path.abspath(url)
        if not compass_viewer.open_store(url):
            print 'Failed to open "%s"; no handlers'%url

    f = InitFrame()

    if compass_viewer.platform.MAC:
        wx.MenuBar.MacSetCommonMenuBar(f.GetMenuBar())
    else:
        f.Show()

    app.MainLoop()
