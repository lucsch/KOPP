import gettext
import os
from pathlib import Path

import wx
import wx.aui
import wx.dataview
import wx.svg

from kopp.frameinfo import FrameInfo
from kopp.framemainlist import FrameMainListView
from kopp.frameabout import FrameAbout
from kopp.database import ProjectDatabase
from kopp.framerecord import FrameRecord

from kopp.version import COMMIT_NUMBER
from kopp.version import VERSION_MAJOR_MINOR
from kopp.version import PROG_NAME

_ = gettext.gettext


class FrameMain(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=PROG_NAME, pos=wx.DefaultPosition,
                          size=wx.Size(1000, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.m_status_bar = self.CreateStatusBar(3, wx.STB_DEFAULT_STYLE, wx.ID_ANY)
        self.m_status_bar.SetStatusWidths([200, -1, 150])
        self.SetStatusBarPane(-1)
        self.m_status_bar.SetStatusText("version {}.{}".format(VERSION_MAJOR_MINOR, COMMIT_NUMBER), 2)

        self._create_menubar()
        self._create_toolbar()
        self._create_controls()

        self.m_prj_database = ProjectDatabase()
        self.m_prj_modified = False
        self.m_prj_in_memory = False

        self.Bind(wx.EVT_MENU, self.on_new_project, id=self.m_menui_file_new.GetId())
        self.Bind(wx.EVT_MENU, self.on_open_project, id=self.m_menui_file_open.GetId())
        self.Bind(wx.EVT_MENU, self.on_save_project, id=self.m_menui_file_save.GetId())
        self.Bind(wx.EVT_MENU, self.on_add_record, id=self.m_menui_rec_add.GetId())
        self.Bind(wx.EVT_MENU, self.on_edit_record, id=self.m_menui_rec_edit.GetId())
        self.Bind(wx.EVT_MENU, self.on_delete_record, id=self.m_menui_rec_delete.GetId())
        self.Bind(wx.EVT_MENU, self.on_view_info, id=self.m_menu_view_info.GetId())
        self.Bind(wx.EVT_MENU, self.on_about, id=self.m_menui_help_about.GetId())
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.on_pane_close)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # open a new project
        self.on_new_project(None)

    def on_new_project(self, event):
        self.m_prj_database.new_project()
        self.m_status_bar.SetStatusText(wx.EmptyString, 1)
        self.m_prj_modified = False
        self.m_prj_in_memory = True

    def on_open_project(self, event):
        with wx.FileDialog(
                self, _("Open Project"),defaultDir="",defaultFile="",
                wildcard="Kopp project files (*.kdb)|*.kdb|All files (*.*)|*.*",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            filename = dlg.GetPath()
            self.open_project(filename)

    def open_project(self, filename:str):
        if not self.m_prj_database.open_project(filename):
            wx.MessageBox(_("Failed to open project {}").format(filename), _("Error"), wx.OK | wx.ICON_ERROR)
            return
        self.m_status_bar.SetStatusText(filename, 1)
        self.m_prj_modified = False
        self.m_prj_in_memory = False

    def on_save_project(self, event):
        default_dir = ""
        default_file = "project.kdb"

        if self.m_prj_database.database_filename:
            default_dir = os.path.dirname(self.m_prj_database.database_filename)
            default_file = os.path.basename(self.m_prj_database.database_filename)

        with wx.FileDialog(self,_("Save Project"),defaultDir=default_dir,defaultFile=default_file,
                wildcard="Kopp project files (*.kdb)|*.kdb|All files (*.*)|*.*",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() != wx.ID_OK:
                return
            filename = fileDialog.GetPath()
            if not self.m_prj_database.save_project(filename):
                wx.MessageBox(_("Failed to save project {}").format(filename), _("Error"), wx.OK | wx.ICON_ERROR)
                return
            self.open_project(filename)

    def on_add_record(self, event):
        frame = FrameRecord(self)
        frame.data.database_handle = self.m_prj_database.database
        if frame.ShowModal() == wx.ID_CANCEL:
            return

        self.m_prj_modified = True
        # TODO: get the data from the frame and save it to the database

    def on_edit_record(self, event):
        pass

    def on_delete_record(self, event):
        pass

    def on_about(self, event):
        frame = FrameAbout(self, program_name=PROG_NAME)
        frame.Show()

    def on_view_info(self, event):
        pane = self.m_aui_manager.GetPane(self.m_info)
        pane.Show(event.IsChecked())
        self.m_aui_manager.Update()

    def on_pane_close(self, event):
        if event.GetPane().window == self.m_info:
            self.m_menu_view_info.Check(False)
        event.Skip()

    def on_close(self, event):
        self.m_aui_manager.UnInit()
        event.Skip()

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

        self.m_menui_file_save = wx.MenuItem(self.m_menu_file, wx.ID_ANY, _(u"Save as...") + u"\t" + u"Ctrl+S",
                                             wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu_file.Append(self.m_menui_file_save)

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

        self.m_aui_manager = wx.aui.AuiManager(self)
        self.m_list = FrameMainListView(self, wx.ID_ANY)
        self.m_info = FrameInfo(self)

        self.m_aui_manager.AddPane(
            self.m_list,
            wx.aui.AuiPaneInfo()
            .Name("records")
            .CenterPane()
            .PaneBorder(False),
        )
        self.m_aui_manager.AddPane(
            self.m_info,
            wx.aui.AuiPaneInfo()
            .Name("info")
            .Caption(_(u"Info window"))
            .Right()
            .BestSize(wx.Size(300, -1))
            .MinSize(wx.Size(200, -1))
            .CloseButton(True)
            .MaximizeButton(False)
            .PaneBorder(False)
            .Dockable(True),
        )

        self.m_aui_manager.Update()
        self.Centre(wx.BOTH)
