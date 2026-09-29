import gettext

import wx

from kopp.timeconverter import TimeConverter

_ = gettext.gettext


class FrameCalculator(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=_("Calculator"),
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )

        self._create_controls()
        for ctrl in [
            self.m_ctrl_hour1_h,
            self.m_ctrl_hour1_m,
            self.m_ctrl_hour2_h,
            self.m_ctrl_hour2_m,
        ]:
            ctrl.Bind(wx.EVT_SPINCTRL, self.on_update_results)

    def on_update_results(self,event):
        h1 = self.m_ctrl_hour1_h.GetValue()
        m1 = self.m_ctrl_hour1_m.GetValue()
        h2 = self.m_ctrl_hour2_h.GetValue()
        m2 = self.m_ctrl_hour2_m.GetValue()

        total_minutes = TimeConverter.to_total_minutes(h1, m1) + TimeConverter.to_total_minutes(h2, m2)
        tot_h, tot_m = TimeConverter.from_total_minutes(total_minutes)

        self.m_ctrl_total_h.SetValue(str(tot_h))
        self.m_ctrl_total_m.SetValue(str(tot_m))

    def _create_controls(self):
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer13 = wx.BoxSizer(wx.VERTICAL)

        fgSizer5 = wx.FlexGridSizer(0, 4, 0, 0)
        fgSizer5.AddGrowableCol(1)
        fgSizer5.AddGrowableCol(3)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText15 = wx.StaticText(
            self, wx.ID_ANY, _("Hour 1 (H:M)"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText15.Wrap(-1)

        fgSizer5.Add(self.m_staticText15, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_hour1_h = wx.SpinCtrl(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(200, -1),
            wx.SP_ARROW_KEYS,
            -1000,
            1000,
            0,
        )
        fgSizer5.Add(self.m_ctrl_hour1_h, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_staticText16 = wx.StaticText(
            self, wx.ID_ANY, _(":"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText16.Wrap(-1)

        fgSizer5.Add(self.m_staticText16, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_hour1_m = wx.SpinCtrl(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(200, -1),
            wx.SP_ARROW_KEYS,
            -1000,
            1000,
            0,
        )
        fgSizer5.Add(self.m_ctrl_hour1_m, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_staticText18 = wx.StaticText(
            self, wx.ID_ANY, _("Hour 2 (H:M)"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText18.Wrap(-1)

        fgSizer5.Add(self.m_staticText18, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_hour2_h = wx.SpinCtrl(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.SP_ARROW_KEYS,
            -1000,
            1000,
            0,
        )
        fgSizer5.Add(self.m_ctrl_hour2_h, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_staticText19 = wx.StaticText(
            self, wx.ID_ANY, _(":"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText19.Wrap(-1)

        fgSizer5.Add(self.m_staticText19, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_hour2_m = wx.SpinCtrl(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.SP_ARROW_KEYS,
            -1000,
            1000,
            0,
        )
        fgSizer5.Add(self.m_ctrl_hour2_m, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_staticText20 = wx.StaticText(
            self, wx.ID_ANY, _("Total (H:M)"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText20.Wrap(-1)

        fgSizer5.Add(self.m_staticText20, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_total_h = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0
        )
        fgSizer5.Add(self.m_ctrl_total_h, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_staticText21 = wx.StaticText(
            self, wx.ID_ANY, _(":"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText21.Wrap(-1)

        fgSizer5.Add(self.m_staticText21, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_total_m = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0
        )
        fgSizer5.Add(self.m_ctrl_total_m, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        bSizer13.Add(fgSizer5, 1, wx.EXPAND, 5)

        m_sdbSizer3 = wx.StdDialogButtonSizer()
        self.m_sdbSizer3OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer3.AddButton(self.m_sdbSizer3OK)
        self.m_sdbSizer3Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer3.AddButton(self.m_sdbSizer3Cancel)
        m_sdbSizer3.Realize()

        bSizer13.Add(m_sdbSizer3, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer13)
        self.Layout()
        bSizer13.Fit(self)

        self.Centre(wx.BOTH)
