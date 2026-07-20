from datetime import datetime

import wx
import wx.lib.plot as plot

import gettext
_ = gettext.gettext


class DatePlotCanvas(plot.PlotCanvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._date_ticks = []

    def set_date_ticks(self, dates):
        self._date_ticks = [self._date_to_x(date) for date in dates if date is not None]

    def _xticks(self, lower, upper):
        if not self._date_ticks:
            return super()._xticks(lower, upper)

        ticks = [tick for tick in sorted(set(self._date_ticks)) if lower <= tick <= upper]
        if len(ticks) > 6:
            step = (len(ticks) - 1) / 5
            ticks = [ticks[round(index * step)] for index in range(6)]

        return [(tick, datetime.fromordinal(int(tick)).strftime("%d.%m.%y")) for tick in ticks]

    @staticmethod
    def _date_to_x(value):
        if isinstance(value, datetime):
            return value.date().toordinal()
        return value.toordinal()


class FrameGraph ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        self._create_controls()
        self.update_display()

    def _create_controls(self):
        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.m_ctrl_plot = DatePlotCanvas(self, wx.ID_ANY)
        bSizer8.Add(self.m_ctrl_plot, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(bSizer8)
        self.Layout()

    def update_display(self, cumulative_totals=None):
        cumulative_totals = cumulative_totals or []
        self.m_ctrl_plot.set_date_ticks([total.date for total in cumulative_totals])

        hr_total_points = self._points_for(cumulative_totals, "hr_total")
        annual_points = self._points_for(cumulative_totals, "annual")
        vac_points = self._points_for(cumulative_totals, "vac")

        lines = []
        if hr_total_points:
            lines.append(plot.PolyLine(hr_total_points, legend="hr_total", colour="blue", width=2))
        if annual_points:
            lines.append(plot.PolyLine(annual_points, legend="annual", colour="green", width=2))
        if vac_points:
            lines.append(plot.PolyLine(vac_points, legend="vac", colour="red", width=2))

        if not lines:
            self.m_ctrl_plot.Clear()
            return

        graphics = plot.PlotGraphics(lines, _("Cumulative totals"), _("Date"), _("Hours"))
        self.m_ctrl_plot.Draw(graphics, self._x_axis(hr_total_points), None)

    def _points_for(self, cumulative_totals, name):
        return [
            (DatePlotCanvas._date_to_x(total.date), getattr(total, name) / 60)
            for total in cumulative_totals
            if total.date is not None
        ]

    def _x_axis(self, points):
        if not points:
            return None

        x_values = [point[0] for point in points]
        if len(set(x_values)) == 1:
            x_value = x_values[0]
            return (x_value - 1, x_value + 1)
        return None
