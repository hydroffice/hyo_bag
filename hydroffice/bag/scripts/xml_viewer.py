from xml.dom.minidom import *

import wx
from wx import stc

OPEN_MENU = wx.NewId()
QUIT_MENU = wx.NewId()

if wx.Platform == '__WXMSW__':
    faces = {'times': 'Courier New',
             'mono': 'Courier New',
             'helv': 'Courier New',
             'other': 'Comic Sans MS',
             'size': 9,
             'size2': 8,
             }
elif wx.Platform == "__WXMAC__":
    faces = {'times': 'Times',
             'mono': 'Monaco',
             'helv': 'Helvetica',
             'other': 'Courier New',
             'size': 10,
             'size2': 8,
             }
else:
    faces = {'times': 'Times',
             'mono': 'Courier New',
             'helv': 'Helvetica',
             'other': 'new century schoolbook',
             'size': 10,
             'size2': 8,
             }


class XmlFrame(wx.MDIParentFrame):
    """ XML frame """

    def __init__(self):
        wx.MDIParentFrame.__init__(self, None, -1, "XML Viewer", size=(800, 400))

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(OPEN_MENU, "&Open")
        menu.AppendSeparator()
        menu.Append(QUIT_MENU, "&Quit")
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)

        wx.EVT_MENU(self, OPEN_MENU, self.on_open)
        wx.EVT_MENU(self, QUIT_MENU, self.on_quit)

    def on_open(self, event):
        """  Open an XML file """
        dlg = wx.FileDialog(self, "Open XML file", ".", "", "XML files (*.xml)|*.xml|All files (*.*)|*.*",
                            wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()
            filename = path[0]
        else:
            return
        dlg.Destroy()
        self.new_xml_window(filename)

    def on_quit(self, event):
        self.Close()

    def new_xml_window(self, xml_filename):
        try:
            xml_document = parse(xml_filename)
        except RuntimeError as e:
            print "Parse error of file %s: %s" % (xml_filename, e)
            return

        # Construct keywords string
        def GetNodeNames(node, keywords=""):
            if not hasattr(node, "data"):
                keywords = keywords + node.nodeName + " "
            for item in node.childNodes:
                keywords = GetNodeNames(item, keywords)
            return keywords

        xml_document_keywords = GetNodeNames(xml_document)
        # print(xml_document_keywords)

        # xml_string = "%s" % xml_document.toprettyxml()
        xml_string = xml_document.toxml()
        # print(xml_string)

        # window definition
        xml_win = wx.Frame(self, -1, xml_filename, size=(750, 350))
        ed = XmlStc(xml_win, xml_string=xml_string)
        # ed = XmlStc(xml_win, xml_string=xml_string, keywords=xml_document_keywords)
        xml_win.Show(True)


class XmlStc(stc.StyledTextCtrl):
    def __init__(self, parent, xml_string, keywords=None):
        stc.StyledTextCtrl.__init__(self, parent, -1)
        self.SetLexer(stc.STC_LEX_XML)
        if keywords is not None:
            self.SetKeyWords(0, keywords)

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(mono)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(mono)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000,bold")

        self.StyleSetSpec(stc.STC_H_VALUE, "fore:#1111ff,bold,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_H_DEFAULT, "fore:#1111ff,bold,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_H_ENTITY, "fore:#ccccff,bold,face:%(helv)s,size:%(size)d" % faces)
        # initial XML tag
        self.StyleSetSpec(stc.STC_H_XMLSTART, "fore:#ffcccc,bold,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_H_XMLEND, "fore:#ffcccc,bold,face:%(helv)s,size:%(size)d" % faces)
        # XML tags
        self.StyleSetSpec(stc.STC_H_TAG, "fore:#888888,bold,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_H_TAGEND, "fore:#888888,bold,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_H_TAGUNKNOWN, "fore:#888888,bold,face:%(helv)s,size:%(size)d" % faces)
        # XML attributes
        self.StyleSetSpec(stc.STC_H_ATTRIBUTE, "fore:#11ff11,bold,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_H_ATTRIBUTEUNKNOWN, "fore:#11ff11,bold,face:%(helv)s,size:%(size)d" % faces)
        # XML comments and quotes
        self.StyleSetSpec(stc.STC_H_COMMENT, "fore:#888888,bold,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_H_SINGLESTRING, "fore:#ff1111,bold,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_H_DOUBLESTRING, "fore:#ff1111,bold,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_H_SGML_SIMPLESTRING, "fore:#ff1111,bold,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_H_SGML_DOUBLESTRING, "fore:#ff1111,bold,face:%(helv)s,size:%(size)d" % faces)

        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#990000,size:%(size)d" % faces)

        # Caret color
        self.SetCaretForeground("BLUE")
        # Selection background
        self.SetSelBackground(1, '#66CCFF')

        self.SetSelBackground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        self.SetProperty("fold", "1")  # Enable folding
        self.SetProperty("fold.html", "1")  # Enable folding
        self.SetProperty("tab.timmy.whinge.level", "1")  # Highlight tab/space mixing (shouldn't be any)
        self.SetMargins(3, 3)  # Set left and right margins
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)  # Set up the numbers in the margin for margin #1
        self.SetMarginWidth(1, 40)  # Reasonable value for, say, 4-5 digits using a mono font (40 pix)
        self.SetViewWhiteSpace(False)
        self.SetWrapMode(stc.STC_WRAP_WORD)
        self.SetUseVerticalScrollBar(True)
        self.SetUseHorizontalScrollBar(True)

        # Setup a margin to hold fold markers
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 15)
        # marker style
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, "white", "#cccccc")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, "white", "black")
        stc.EVT_STC_MARGINCLICK(self, -1, self.on_margin_click)

        self.SetText(xml_string)
        self.SetEditable(False)

    def on_margin_click(self, evt):
        """ Folds and unfolds as needed """

        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.fold_all()

            else:
                line_clicked = self.LineFromPosition(evt.GetPosition())
                if self.GetFoldLevel(line_clicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(line_clicked, True)
                        self.expand_item(line_clicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(line_clicked):
                            self.SetFoldExpanded(line_clicked, False)
                            self.expand_item(line_clicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(line_clicked, True)
                            self.expand_item(line_clicked, True, True, 100)
                    else:
                        self.ToggleFold(line_clicked)

    def fold_all(self):
        line_count = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for line_num in range(line_count):
            if self.GetFoldLevel(line_num) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(line_num)
                break

        line_num = 0
        while line_num < line_count:
            level = self.GetFoldLevel(line_num)
            if level & stc.STC_FOLDLEVELHEADERFLAG and (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(line_num, True)
                    line_num = self.expand_item(line_num, True)
                    line_num -= 1
                else:
                    last_child = self.GetLastChild(line_num, -1)
                    self.SetFoldExpanded(line_num, False)
                    if last_child > line_num:
                        self.HideLines(line_num + 1, last_child)

            line_num += 1

    def expand_item(self, line, do_expand, force=False, vis_levels=0, level=-1):
        last_child = self.GetLastChild(line, level)
        line += 1
        while line <= last_child:
            if force:
                if vis_levels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if do_expand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if vis_levels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)
                    line = self.expand_item(line, do_expand, force, vis_levels - 1)

                else:
                    if do_expand and self.GetFoldExpanded(line):
                        line = self.expand_item(line=line, do_expand=True, force=force, vis_levels=(vis_levels - 1))
                    else:
                        line = self.expand_item(line=line, do_expand=False, force=force, vis_levels=(vis_levels - 1))
            else:
                line += 1

        return line


class MyApp(wx.PySimpleApp):
    def OnInit(self):
        window = XmlFrame()
        window.Show(True)
        return True


def main():
    xml_viewer = MyApp()
    xml_viewer.MainLoop()


if __name__ == "__main__":
    main()
