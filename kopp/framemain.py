import gettext
import os
from datetime import date, datetime

import wx
import wx.aui
import wx.dataview
import wx.svg

from kopp.framegraph import FrameGraph
from kopp.frameinfo import FrameInfo
from kopp.framemainlist import FrameMainListView, MainListViewData
from kopp.frameabout import FrameAbout
from kopp.framesettings import FrameSettings
from kopp.database import ProjectDatabase
from kopp.database_model import Records, Tags, Tagsmix
from kopp.framerecord import FrameRecord
from kopp.record_totals import (
    RecordCumulativeTotalsCalculator,
    RecordTotals,
    RecordTotalsCalculator,
)
from kopp.timeconverter import TimeConverter
from kopp.xlsx_exporter import XlsxExporter

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
        self.m_config = wx.FileConfig(PROG_NAME)

        self.Bind(wx.EVT_MENU, self.on_new_project, id=self.m_menui_file_new.GetId())
        self.Bind(wx.EVT_MENU, self.on_open_project, id=self.m_menui_file_open.GetId())
        self.Bind(wx.EVT_MENU, self.on_save_project, id=self.m_menui_file_save.GetId())
        self.Bind(wx.EVT_MENU, self.on_add_record, id=self.m_menui_rec_add.GetId())
        self.Bind(wx.EVT_MENU, self.on_edit_record, id=self.m_menui_rec_edit.GetId())
        self.Bind(wx.EVT_MENU, self.on_delete_record, id=self.m_menui_rec_delete.GetId())
        self.Bind(wx.EVT_MENU, self.on_export_xlsx, id=self.m_menui_rec_export_xlsx.GetId())
        self.Bind(wx.EVT_MENU, self.on_view_info, id=self.m_menui_view_info.GetId())
        self.Bind(wx.EVT_MENU, self.on_view_graph, id=self.m_menui_view_graph.GetId())
        self.Bind(wx.EVT_MENU, self.on_about, id=self.m_menui_help_about.GetId())
        self.Bind(wx.EVT_MENU, self.on_website, id=self.m_menui_help_web.GetId())
        self.Bind(wx.EVT_MENU, self.on_settings, id=self.m_menui_settings.GetId())
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.on_pane_close)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.m_list.Bind(wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.on_list_item_activated)
        self.m_list.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.on_list_selection_changed)

        # open a new project or load the last one depending on the config
        auto_load_project = self.m_config.Read("auto_load_project", "")
        if auto_load_project != "" and os.path.exists(auto_load_project):
            self.open_project(auto_load_project)
        else:
            self.on_new_project(None)

    def on_new_project(self, event):
        self.m_prj_database.new_project()
        self.m_list.DeleteAllItems()
        self._update_info_window()
        self._update_graph_window()
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
        self._reload_records_list()
        self._update_info_window()
        self._update_graph_window()
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

            # do not save the project on the same file (endless loop)
            if self.m_prj_database.database_filename == filename:
                wx.LogMessage(_("Project already saved to {}").format(filename))
                return

            if not self.m_prj_database.save_project(filename):
                wx.MessageBox(_("Failed to save project {}").format(filename), _("Error"), wx.OK | wx.ICON_ERROR)
                return
            self.open_project(filename)

    def on_add_record(self, event):
        frame = FrameRecord(self)
        frame.data.database_handle = self.m_prj_database.database
        frame.TransferDataToWindow()
        if frame.ShowModal() == wx.ID_CANCEL:
            return
        frame.TransferDataFromWindow()

        self._save_record_data(frame.data)
        self._reload_records_list()
        self._update_info_window()
        self._update_graph_window()
        self.m_prj_modified = True

    def on_edit_record(self, event):
        selection = self._get_selected_record()
        if not selection:
            return

        row, record = selection
        frame = FrameRecord(self)
        frame.data.database_handle = self.m_prj_database.database
        frame.data.date = self._datetime_to_wx_date(record.date)
        frame.data.hr_done = record.hr_base or 0
        frame.data.hr_increased = record.hr_maj or 0
        frame.data.a_total = record.annual or 0
        frame.data.vac_total = record.vac or 0
        frame.data.comment = record.comment or ""
        frame.data.tags_id = [
            tag_mix.tag.id
            for tag_mix in Tagsmix.select(Tagsmix, Tags).join(Tags).where(Tagsmix.record == record)
        ]
        frame.TransferDataToWindow()

        if frame.ShowModal() == wx.ID_CANCEL:
            return
        frame.TransferDataFromWindow()

        self._save_record_data(frame.data, record)
        self._reload_records_list()
        self._update_info_window()
        self._update_graph_window()
        self.m_prj_modified = True

    def on_delete_record(self, event):
        selection = self._get_selected_record()
        if not selection:
            return

        row, record = selection
        with self.m_prj_database.database.db.atomic():
            Tagsmix.delete().where(Tagsmix.record == record).execute()
            record.delete_instance()

        self.m_list.DeleteItem(row)
        self._update_info_window()
        self._update_graph_window()
        self.m_prj_modified = True

    def on_export_xlsx(self, event):
        if self.m_list.GetItemCount() == 0:
            wx.MessageBox(_("No records to export."), _("Info"), wx.OK | wx.ICON_INFORMATION)
            return

        with wx.FileDialog(
            self,
            _("Export to xlsx"),
            defaultDir="",
            defaultFile="records.xlsx",
            wildcard="Excel workbook (*.xlsx)|*.xlsx",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return

            filename = dlg.GetPath()
            if not filename.lower().endswith(".xlsx"):
                filename += ".xlsx"

            try:
                XlsxExporter.export(
                    filename,
                    MainListViewData.column_info.keys(),
                    self.m_list.GetAllTextValues(),
                )
            except OSError as error:
                wx.MessageBox(str(error), _("Export failed"), wx.OK | wx.ICON_ERROR)
                return

        wx.MessageBox(_("Export completed."), _("Info"), wx.OK | wx.ICON_INFORMATION)

    def on_list_item_activated(self, event):
        self.on_edit_record(event)

    def on_list_selection_changed(self, event):
        self._update_info_window()
        event.Skip()

    def _get_selected_record(self, show_message=True):
        if self.m_list.GetSelectedItemsCount() != 1:
            if show_message:
                wx.MessageBox(_("Select one record first."), _("Info"), wx.OK | wx.ICON_INFORMATION)
            return None

        row = self.m_list.GetSelectedRow()
        if row == wx.NOT_FOUND:
            if show_message:
                wx.MessageBox(_("Select one record first."), _("Info"), wx.OK | wx.ICON_INFORMATION)
            return None

        record_id = self.m_list.GetItemData(self.m_list.RowToItem(row))
        try:
            return row, Records.get_by_id(record_id)
        except Records.DoesNotExist:
            if show_message:
                wx.MessageBox(_("Selected record no longer exists."), _("Error"), wx.OK | wx.ICON_ERROR)
            self.m_list.DeleteItem(row)
            return None

    def _update_info_window(self):
        if not self.m_prj_database.database:
            self.m_info.update_data(RecordTotals(), _("Selection"), RecordTotals())
            return

        total = RecordTotalsCalculator.all()
        selection = self._get_selected_record(show_message=False)
        if selection:
            row, record = selection
            selected = RecordTotalsCalculator.until_record_id(record.record_id)
            selected_title = self._format_record_date(record.date)
        else:
            selected = RecordTotals()
            selected_title = _("Selection")

        self.m_info.update_data(selected, selected_title, total)

    def _update_graph_window(self):
        if not self.m_prj_database.database:
            self.m_graph.update_display([])
            return

        self.m_graph.update_display(RecordCumulativeTotalsCalculator.all())

    def _save_record_data(self, data, record=None):
        db_date = self._wx_date_to_datetime(data.date)
        with self.m_prj_database.database.db.atomic():
            if record is None:
                record = Records.create(
                    date=db_date,
                    hr_base=data.hr_done,
                    hr_maj=data.hr_increased,
                    annual=data.a_total,
                    vac=data.vac_total,
                    comment=data.comment,
                )
            else:
                record.date = db_date
                record.hr_base = data.hr_done
                record.hr_maj = data.hr_increased
                record.annual = data.a_total
                record.vac = data.vac_total
                record.comment = data.comment
                record.save()

            Tagsmix.delete().where(Tagsmix.record == record).execute()
            for tag_id in data.tags_id:
                Tagsmix.get_or_create(record=record, tag=tag_id)

        return record

    def _reload_records_list(self):
        self.m_list.DeleteAllItems()
        for record in Records.select().order_by(Records.date, Records.record_id):
            self._append_record_to_list(record)

    def _append_record_to_list(self, record):
        self.m_list.AppendItem(self._record_to_list_values(record), record.record_id)

    def _update_record_list_row(self, row, record):
        for column, value in enumerate(self._record_to_list_values(record)):
            self.m_list.SetTextValue(value, row, column)
        self.m_list.SetItemData(self.m_list.RowToItem(row), record.record_id)

    def _record_to_list_values(self, record):
        return [
            self._format_record_date(record.date),
            self._format_minutes((record.hr_base or 0) + (record.hr_maj or 0)),
            self._format_minutes(record.annual or 0),
            self._format_minutes(record.vac or 0),
            self._format_record_tags(record),
            record.comment or "",
        ]

    def _format_record_tags(self, record):
        tags = (
            Tags.select()
            .join(Tagsmix)
            .where(Tagsmix.record == record)
            .order_by(Tags.desc)
        )
        return ", ".join(tag.desc for tag in tags)

    def _format_minutes(self, total_minutes):
        if total_minutes == 0:
            return ""

        sign = "-" if total_minutes < 0 else ""
        hours, minutes = TimeConverter.from_total_minutes(abs(total_minutes))
        return "{}{}:{:02d}".format(sign, hours, minutes)

    def _format_record_date(self, value):
        value = self._date_to_datetime(value)
        if not value:
            return ""

        weekdays = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
        return "{} {:02d}.{:02d}.{:02d}".format(
            weekdays[value.weekday()],
            value.day,
            value.month,
            value.year % 100,
        )

    def _wx_date_to_datetime(self, value):
        return self._date_to_datetime(value)

    def _date_to_datetime(self, value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime(value.year, value.month, value.day)
        if isinstance(value, wx.DateTime) and value.IsValid():
            return datetime(value.GetYear(), value.GetMonth() + 1, value.GetDay())
        return None

    def _datetime_to_wx_date(self, value):
        if isinstance(value, wx.DateTime):
            return value
        if isinstance(value, datetime):
            return wx.DateTime.FromDMY(value.day, value.month - 1, value.year)
        return None

    def on_about(self, event):
        frame = FrameAbout(self, program_name=PROG_NAME)
        frame.Show()

    def on_website(self, event):
        wx.LaunchDefaultBrowser("https://github.com/lucsch/KOPP")

    def on_settings(self, event):
        my_auto_load_project_path = self.m_config.Read("auto_load_project", "")
        frame = FrameSettings(self)
        frame.m_auto_load_project_path = my_auto_load_project_path
        if frame.ShowModal() != wx.ID_OK:
            return
        self.m_config.Write("auto_load_project", frame.m_auto_load_project_path)

    def on_view_info(self, event):
        pane = self.m_aui_manager.GetPane(self.m_info)
        pane.Show(event.IsChecked())
        self.m_aui_manager.Update()

    def on_view_graph(self, event):
        pane = self.m_aui_manager.GetPane(self.m_graph)
        pane.Show(event.IsChecked())
        self.m_aui_manager.Update()

    def on_pane_close(self, event):
        if event.GetPane().window == self.m_info:
            self.m_menui_view_info.Check(False)
        if event.GetPane().window == self.m_graph:
            self.m_menui_view_graph.Check(False)
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

        self.m_menui_file_save = wx.MenuItem(self.m_menu_file, wx.ID_ANY, _(u"Save as...") + u"\t" + u"Ctrl+S",
                                             wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu_file.Append(self.m_menui_file_save)

        self.m_menu_file.AppendSeparator()

        self.m_menui_settings = wx.MenuItem(self.m_menu_file, wx.ID_ANY, _(u"Settings...") + u"\t" + u"Ctrl+,",
                                            wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu_file.Append(self.m_menui_settings)

        self.m_menu_file.AppendSeparator()

        self.m_menui_file_exit = wx.MenuItem(self.m_menu_file, wx.ID_EXIT, _(u"Quit"), wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu_file.Append(self.m_menui_file_exit)

        self.m_menubar.Append(self.m_menu_file, _(u"&File"))

        self.m_menu_rec = wx.Menu()
        self.m_menui_rec_add = wx.MenuItem(self.m_menu_rec, wx.ID_ANY, _(u"Add...") + u"\t" + u"Ctrl+N", wx.EmptyString,
                                           wx.ITEM_NORMAL)
        self.m_menu_rec.Append(self.m_menui_rec_add)

        self.m_menui_rec_delete = wx.MenuItem(self.m_menu_rec, wx.ID_ANY, _(u"Delete"), wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu_rec.Append(self.m_menui_rec_delete)

        self.m_menui_rec_edit = wx.MenuItem(self.m_menu_rec, wx.ID_ANY, _(u"Edit...") + u"\t" + u"ENTER",
                                            wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu_rec.Append(self.m_menui_rec_edit)

        self.m_menu_rec.AppendSeparator()

        self.m_menui_rec_export_xlsx = wx.MenuItem( self.m_menu_rec, wx.ID_ANY, _(u"Export to xlsx..."), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_rec.Append( self.m_menui_rec_export_xlsx )

        self.m_menubar.Append(self.m_menu_rec, _(u"Records"))

        self.m_menu_view = wx.Menu()
        self.m_menui_view_info = wx.MenuItem(self.m_menu_view, wx.ID_ANY, _(u"Info window") + u"\t" + u"Ctrl+I",
                                             wx.EmptyString, wx.ITEM_CHECK)
        self.m_menu_view.Append(self.m_menui_view_info)
        self.m_menui_view_info.Check(True)

        self.m_menui_view_graph = wx.MenuItem(self.m_menu_view, wx.ID_ANY,_("Graph Window...") + "\t" + "Ctrl+G",wx.EmptyString,wx.ITEM_CHECK)
        self.m_menu_view.Append(self.m_menui_view_graph)
        self.m_menui_view_graph.Check(True)

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
        self.m_graph = FrameGraph(self)

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
        self.m_aui_manager.AddPane(
            self.m_graph,
            wx.aui.AuiPaneInfo()
            .Name("graph")
            .Caption(_(u"Graph"))
            .Bottom()
            .BestSize(wx.Size(-1, 150))
            .MinSize(wx.Size(200, 100))
            .CloseButton(True)
            .MaximizeButton(False)
            .PaneBorder(False)
            .Dockable(True),
        )

        self.m_aui_manager.Update()
        self.Centre(wx.BOTH)
