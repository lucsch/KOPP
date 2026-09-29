import os
import sys

import wx
import wx.html
from jinja2 import Environment, FileSystemLoader

from kopp.infodataimporter import InfoData
from kopp.record_totals import RecordTotals
from kopp.timeconverter import TimeConverter


def load_html_template(template_name: str):
    """Load the HTML template in memory from the templates folder."""
    if getattr(sys, 'frozen', False):  # if frozen with pyinstaller, MEIPASS is set
        base_folder = sys._MEIPASS
    else:
        base_folder = os.path.dirname(os.path.abspath(__file__))

    template_folder = os.path.join(base_folder, 'templates')
    env = Environment(loader=FileSystemLoader(template_folder))
    return env.get_template(template_name)

class FrameInfo(wx.Panel):
    """Dockable information panel for the main frame."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY)

        self.info_selected = InfoData()
        self.info_total = InfoData()

        self.html_template = load_html_template('info.html')

        self._create_controls()
        self._update_html()

    def _convert_record_to_info(self, record: RecordTotals, title: str) -> InfoData:
        info = InfoData(title=title)
        if record is not None:
            info.hr_done_hours, info.hr_done_minutes = TimeConverter.from_total_minutes(record.hr_base)
            info.hr_increased_hours, info.hr_increased_minutes = TimeConverter.from_total_minutes(record.hr_maj)
            info.hr_total_hours, info.hr_total_minutes = TimeConverter.from_total_minutes(record.hr_base + record.hr_maj)
            info.a_hours, info.a_minutes = TimeConverter.from_total_minutes(record.annual)
            info.piquet_hours, info.piquet_minutes = TimeConverter.from_total_minutes(record.piquet)
            info.vac_hours, info.vac_minutes = TimeConverter.from_total_minutes(record.vac)
        return info

    def update_data(self, record_data_selected: RecordTotals, record_data_selected_txt: str, record_data_total: RecordTotals):
        # Update the info data for the selected records
        self.info_selected = self._convert_record_to_info(record_data_selected, record_data_selected_txt)
        self.info_total = self._convert_record_to_info(record_data_total, "Total Records")
        self._update_html()

    def _create_controls(self):
        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_ctrl_html = wx.html.HtmlWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                              wx.html.HW_SCROLLBAR_AUTO)
        bSizer2.Add(self.m_ctrl_html, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer2)
        self.Layout()

    def _update_html(self):
        html_final = self.html_template.render(info_selected=self.info_selected,
                                  info_total=self.info_total)
        self.m_ctrl_html.SetPage(html_final)
