import wx
import wx.html

class FrameInfo(wx.Panel):
    """Dockable information panel for the main frame."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY)
        self._create_controls()
        self._create_dummy_html()

    def _create_controls(self):
        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_ctrl_html = wx.html.HtmlWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                              wx.html.HW_SCROLLBAR_AUTO)
        bSizer2.Add(self.m_ctrl_html, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer2)
        self.Layout()

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
