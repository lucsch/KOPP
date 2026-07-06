import gettext
import os
from pathlib import Path

import wx
import wx.dataview
import wx.svg

from kopp.version import COMMIT_NUMBER
from kopp.version import VERSION_MAJOR_MINOR

_ = gettext.gettext


class FrameMain(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=_(u"KOPP"), pos=wx.DefaultPosition,
                          size=wx.Size(1000, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.m_status_bar = self.CreateStatusBar(3, wx.STB_DEFAULT_STYLE, wx.ID_ANY)
        self.m_status_bar.SetStatusWidths([200, -1, 150])
        self.SetStatusBarPane(-1)
        self.m_status_bar.SetStatusText("version {}.{}".format(VERSION_MAJOR_MINOR, COMMIT_NUMBER), 2)

