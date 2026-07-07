import gettext
import os
from pathlib import Path

import wx
import wx.dataview
import wx.svg

from kopp.framemainlist import FrameMainListView

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

        self._create_menubar()
        self._create_toolbar()
        self._create_controls()


    def _create_menubar(self):
        self.m_menubar = wx.MenuBar(0)
        self.m_menu_file = wx.Menu()
        self.m_menui_file_new = wx.MenuItem(self.m_menu_file, wx.ID_NEW, _(u"New"), wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu_file.Append(self.m_menui_file_new)

        self.m_menui_file_open = wx.MenuItem(self.m_menu_file, wx.ID_OPEN, _(u"Open...") + u"\t" + u"Ctrl+O",
                                             wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu_file.Append(self.m_menui_file_open)

        self.m_menu_file_recent = wx.Menu()
        self.m_menu_file.AppendSubMenu(self.m_menu_file_recent, _(u"Recent"))

        self.m_menu_file.AppendSeparator()

        self.m_menui_file_exit = wx.MenuItem(self.m_menu_file, wx.ID_EXIT, _(u"Quit"), wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu_file.Append(self.m_menui_file_exit)

        self.m_menubar.Append(self.m_menu_file, _(u"&File"))

        self.m_menu_rec = wx.Menu()
        self.m_menui_rec_add = wx.MenuItem(self.m_menu_rec, wx.ID_ANY, _(u"Add...") + u"\t" + u"Ctrl+N", wx.EmptyString,
                                           wx.ITEM_NORMAL)
        self.m_menu_rec.Append(self.m_menui_rec_add)

        self.m_menui_rec_delete = wx.MenuItem(self.m_menu_rec, wx.ID_ANY, _(u"Delete") + u"\t" + u"DEL", wx.EmptyString,
                                              wx.ITEM_NORMAL)
        self.m_menu_rec.Append(self.m_menui_rec_delete)

        self.m_menui_rec_edit = wx.MenuItem(self.m_menu_rec, wx.ID_ANY, _(u"Edit...") + u"\t" + u"ENTER",
                                            wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu_rec.Append(self.m_menui_rec_edit)

        self.m_menubar.Append(self.m_menu_rec, _(u"Records"))

        self.m_menu_view = wx.Menu()
        self.m_menu_view_info = wx.MenuItem(self.m_menu_view, wx.ID_ANY, _(u"Info window") + u"\t" + u"Ctrl+I",
                                            wx.EmptyString, wx.ITEM_CHECK)
        self.m_menu_view.Append(self.m_menu_view_info)
        self.m_menu_view_info.Check(True)

        self.m_menubar.Append(self.m_menu_view, _(u"View"))

        self.m_menui_help = wx.Menu()
        self.m_menui_help_about = wx.MenuItem(self.m_menui_help, wx.ID_ABOUT, _(u"About"), wx.EmptyString,
                                              wx.ITEM_NORMAL)
        self.m_menui_help.Append(self.m_menui_help_about)

        self.m_menui_help_web = wx.MenuItem(self.m_menui_help, wx.ID_ANY, _(u"Website..."), wx.EmptyString,
                                            wx.ITEM_NORMAL)
        self.m_menui_help.Append(self.m_menui_help_web)

        self.m_menubar.Append(self.m_menui_help, _(u"Help"))

        self.SetMenuBar(self.m_menubar)

    def _create_toolbar(self):
        pass

    def _create_controls(self):
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_list = FrameMainListView(self, wx.ID_ANY)
        bSizer1.Add(self.m_list, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

