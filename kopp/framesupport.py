import os
import sys

import wx
import wx.xrc
import wx.html
from kopp.frameinfo import load_html_template
from kopp.infodataimporter import InfoData, InfoDataImporter

import gettext
_ = gettext.gettext

class FrameSupport ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Support"), pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.m_info_data = InfoData()
        self.html_template = load_html_template('support.html')

        self._create_controls()
        self._update_html()

        self.Bind(wx.EVT_BUTTON, self.on_button_import_clipboard, id=self.m_btn_import_clipboard.GetId())

    def on_button_import_clipboard( self, event):
        # open the clipboard and check if it content string
        if not wx.TheClipboard.IsOpened():  # may crash, otherwise
            do = wx.TextDataObject()
            wx.TheClipboard.Open()
            success = wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            if not success:
                wx.MessageBox(
                    "There is no data in the clipboard\nCopy some data to the clipboard",
                    "Warning",
                    wx.ICON_WARNING,
                )
                return

            self.m_ctrl_textctrl.SetValue(do.GetText())
            importer = InfoDataImporter()
            if importer.process(do.GetText()):
                self.m_info_data = importer.get_processed_data()
                self._update_html()
            else:
                wx.LogWarning("Error Importing data from clipboard. Please check the format of the data.")

    def _update_html(self):
        html_final = self.html_template.render(info_general=self.m_info_data)
        self.m_ctrl_html.SetPage(html_final)

    def _create_controls(self):
        self.SetSizeHints(wx.Size(400, 360), wx.DefaultSize)

        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.m_notebook1 = wx.Notebook(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_notebook1.SetMinSize(wx.Size(320, 180))
        self.m_panel_info = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer11 = wx.BoxSizer(wx.VERTICAL)

        self.m_ctrl_html = wx.html.HtmlWindow(self.m_panel_info, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                              wx.html.HW_SCROLLBAR_NEVER)
        self.m_ctrl_html.SetMinSize(wx.Size(300, 140))
        bSizer11.Add(self.m_ctrl_html, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel_info.SetSizer(bSizer11)
        self.m_notebook1.AddPage(self.m_panel_info, _(u"Info"), True)
        self.m_panel_raw = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer12 = wx.BoxSizer(wx.VERTICAL)

        self.m_ctrl_textctrl = wx.TextCtrl(self.m_panel_raw, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.DefaultSize, wx.TE_MULTILINE)
        self.m_ctrl_textctrl.SetMinSize(wx.Size(300, 140))
        bSizer12.Add(self.m_ctrl_textctrl, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel_raw.SetSizer(bSizer12)
        self.m_notebook1.AddPage(self.m_panel_raw, _(u"Raw"), False)

        bSizer10.Add(self.m_notebook1, 1, wx.EXPAND | wx.ALL, 5)

        self.m_btn_import_clipboard = wx.Button(self.m_panel1, wx.ID_ANY, _(u"Import clipboard"), wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        bSizer10.Add(self.m_btn_import_clipboard, 0, wx.ALL, 5)

        self.m_panel1.SetSizer(bSizer10)
        bSizer9.Add(self.m_panel1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer9)
        self.Layout()

        self.Centre(wx.BOTH)
