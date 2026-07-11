from dataclasses import dataclass

import wx
import wx.html
import os
import sys
from jinja2 import Environment, FileSystemLoader
from kopp.timeconverter import TimeConverter

from kopp.record_totals import RecordTotals

@dataclass
class InfoData:
    title: str = ""
    hr_done_hours: int = 0
    hr_done_minutes: int = 0
    hr_increased_hours: int = 0
    hr_increased_minutes: int = 0
    hr_total_hours: int = 0
    hr_total_minutes: int = 0
    a_hours: int = 0
    a_minutes: int = 0
    vac_hours: int = 0
    vac_minutes: int = 0


class FrameInfo(wx.Panel):
    """Dockable information panel for the main frame."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY)

        self.info_selected = InfoData()
        self.info_total = InfoData()

        self.html_template = self._load_html_template()

        self._create_controls()
        self._update_html()

    def _convert_record_to_info(self, record: RecordTotals, title: str) -> InfoData:
        info = InfoData(title=title)
        if record is not None:
            info.hr_done_hours, info.hr_done_minutes = TimeConverter.from_total_minutes(record.hr_base)
            info.hr_increased_hours, info.hr_increased_minutes = TimeConverter.from_total_minutes(record.hr_maj)
            info.hr_total_hours, info.hr_total_minutes = TimeConverter.from_total_minutes(record.hr_base + record.hr_maj)
            info.a_hours, info.a_minutes = TimeConverter.from_total_minutes(record.annual)
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

    def _load_html_template(self):
        """load the html template in memory from the templates folder"""
        if getattr(sys, 'frozen', False): # if frozen with pyinstaller, MEIPASS is set
            base_folder = sys._MEIPASS
        else:
            base_folder = os.path.dirname(os.path.abspath(__file__))

        template_folder = os.path.join(base_folder, 'templates')
        env = Environment(loader=FileSystemLoader(template_folder))
        return env.get_template('info.html')

    def _update_html(self):
        html_final = self.html_template.render(info_selected=self.info_selected,
                                  info_total=self.info_total)
        self.m_ctrl_html.SetPage(html_final)

    def _create_dummy_html(self):
        # Vos variables de données (exemples)
        titre_selection = "07 Juillet 2026"
        valeur_hr = 60
        valeur_a = 34
        valeur_vac = 28

        # Le template HTML utilisant les f-strings
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #333333;
                background-color: #f9f9f9;
                margin: 15px;
            }}
            h1 {{
                color: #2c3e50;
                font-size: 20px;
                border-bottom: 2px solid #3498db;
                padding-bottom: 5px;
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background-color: #ffffff;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            th {{
                background-color: #34495e;
                color: #ffffff;
                font-weight: bold;
                text-align: left;
                padding: 10px;
            }}
            td {{
                padding: 12px 10px;
                border-bottom: 1px solid #eeeeee;
                font-size: 14px;
            }}
            .label-col {{
                font-weight: bold;
                color: #555555;
                width: 40%;
            }}
            .value-col {{
                text-align: right;
                font-family: monospace;
                font-size: 15px;
                color: #2c3e50;
                font-weight: bold;
            }}
        </style>
        </head>
        <body>

            <h1>{titre_selection}</h1>

            <table>
                <thead>
                    <tr>
                        <th>Métrique</th>
                        <th style="text-align: right;">Valeur (Minutes)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="label-col">HR</td>
                        <td class="value-col">{valeur_hr}</td>
                    </tr>
                    <tr>
                        <td class="label-col">A</td>
                        <td class="value-col">{valeur_a}</td>
                    </tr>
                    <tr>
                        <td class="label-col">VAC</td>
                        <td class="value-col">{valeur_vac}</td>
                    </tr>
                </tbody>
            </table>

        </body>
        </html>
        """

        self.m_ctrl_html.SetPage(html_template)
