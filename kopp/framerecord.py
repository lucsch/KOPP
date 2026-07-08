#!/usr/bin/env/ python3
import wx
import wx.adv
import gettext

from kopp.database_model import Tags
from kopp.timeconverter import TimeConverter

_ = gettext.gettext

class FrameRecordData:
    def __init__(self):
        self.date = None
        self.hr_done = 0
        self.hr_increased = 0
        self.a_total = 0
        self.vac_total = 0
        self.comment = ""
        self.tags_id = []
        self.database_handle = None


class FrameRecord(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=_(u"Record"), pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.data = FrameRecordData()
        self._create_controls()
        self._bind_events()
        self._update_hr_total()

    def TransferDataToWindow(self):
        self._load_tags()
        if self.data.date:
            self.m_ctrl_date.SetValue(self.data.date)
        hm = TimeConverter.from_total_minutes(self.data.hr_done)
        self.m_ctrl_hrd_h.SetValue(hm[0])
        self.m_ctrl_hrd_m.SetValue(hm[1])
        hm = TimeConverter.from_total_minutes(self.data.hr_increased)
        self.m_ctrl_hri_h.SetValue(hm[0])
        self.m_ctrl_hri_m.SetValue(hm[1])
        self._update_hr_total()
        hm = TimeConverter.from_total_minutes(self.data.a_total)
        self.m_ctrl_a_h.SetValue(hm[0])
        self.m_ctrl_a_m.SetValue(hm[1])
        hm = TimeConverter.from_total_minutes(self.data.vac_total)
        self.m_ctrl_vac_h.SetValue(hm[0])
        self.m_ctrl_vac_m.SetValue(hm[1])
        self.m_ctrl_comment.SetValue(self.data.comment)
        return True

    def TransferDataFromWindow(self):
        self.data.date = self.m_ctrl_date.GetValue()
        self.data.hr_done = TimeConverter.to_total_minutes(self.m_ctrl_hrd_h.GetValue(), self.m_ctrl_hrd_m.GetValue())
        self.data.hr_increased = TimeConverter.to_total_minutes(self.m_ctrl_hri_h.GetValue(), self.m_ctrl_hri_m.GetValue())
        self.data.a_total = TimeConverter.to_total_minutes(self.m_ctrl_a_h.GetValue(), self.m_ctrl_a_m.GetValue())
        self.data.vac_total = TimeConverter.to_total_minutes(self.m_ctrl_vac_h.GetValue(), self.m_ctrl_vac_m.GetValue())
        self.data.comment = self.m_ctrl_comment.GetValue()
        self.data.tags_id = self.get_checked_tag_ids()
        return True

    def _bind_events(self):
        for ctrl in (
            self.m_ctrl_hrd_h,
            self.m_ctrl_hrd_m,
            self.m_ctrl_hri_h,
            self.m_ctrl_hri_m,
        ):
            ctrl.Bind(wx.EVT_SPINCTRL, self.on_hr_value_changed)
            ctrl.Bind(wx.EVT_TEXT, self.on_hr_value_changed)

        self.m_ctrl_btn_tag.Bind(wx.EVT_BUTTON, self.on_add_tag)
        self.m_ctrl_btn_50.Bind(wx.EVT_BUTTON, self.on_add_50)
        self.m_ctrl_btn_100.Bind(wx.EVT_BUTTON, self.on_add_100)

    def on_hr_value_changed(self, event):
        self._update_hr_total()
        event.Skip()

    def _update_hr_total(self):
        hr_done = TimeConverter.to_total_minutes(self.m_ctrl_hrd_h.GetValue(), self.m_ctrl_hrd_m.GetValue())
        hr_increased = TimeConverter.to_total_minutes(self.m_ctrl_hri_h.GetValue(), self.m_ctrl_hri_m.GetValue())
        hours, minutes = TimeConverter.from_total_minutes(hr_done + hr_increased)

        self.m_ctrl_hrtot_h.ChangeValue(str(hours))
        self.m_ctrl_hrtot_m.ChangeValue(str(minutes))

    def on_add_tag(self, event):
        if not self.data.database_handle:
            wx.MessageBox(_("No database is open."), _("Error"), wx.OK | wx.ICON_ERROR)
            return

        with wx.TextEntryDialog(self, _("Tag name:"), _("Add tag")) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return

            tag_name = dlg.GetValue().strip()
            if not tag_name:
                return

        try:
            with self.data.database_handle.db.atomic():
                tag = Tags.select().where(Tags.desc == tag_name).first()
                if tag:
                    created = False
                else:
                    tag = Tags.create(desc=tag_name)
                    created = True
        except Exception as exc:
            wx.MessageBox(_("Failed to create tag: {}").format(exc), _("Error"), wx.OK | wx.ICON_ERROR)
            return

        if not created:
            wx.MessageBox(_("This tag already exists."), _("Info"), wx.OK | wx.ICON_INFORMATION)
            return

        self._add_tag_to_list(tag)

    def _add_tag_to_list(self, tag, checked=True):
        index = self.m_ctrl_list_tags.Append(tag.desc)
        self.m_ctrl_list_tags.SetClientData(index, tag.id)
        self.m_ctrl_list_tags.Check(index, checked)

    def _load_tags(self):
        self.m_ctrl_list_tags.Clear()
        if not self.data.database_handle:
            return

        selected_tags = set(self.data.tags_id)
        for tag in Tags.select().order_by(Tags.desc):
            self._add_tag_to_list(tag, tag.id in selected_tags)

    def get_checked_tag_ids(self):
        tag_ids = []
        for index in range(self.m_ctrl_list_tags.GetCount()):
            if self.m_ctrl_list_tags.IsChecked(index):
                tag_ids.append(self.m_ctrl_list_tags.GetClientData(index))
        return tag_ids

    def on_add_50(self, event):
        min_done = TimeConverter.to_total_minutes(self.m_ctrl_hrd_h.GetValue(), self.m_ctrl_hrd_m.GetValue())
        min_done = int(min_done * 0.5)
        hours, minutes = TimeConverter.from_total_minutes(min_done)
        self.m_ctrl_hri_h.SetValue(hours)
        self.m_ctrl_hri_m.SetValue(minutes)
        self.on_hr_value_changed(event)

    def on_add_100(self, event):
        self.m_ctrl_hri_h.SetValue(self.m_ctrl_hrd_h.GetValue())
        self.m_ctrl_hri_m.SetValue(self.m_ctrl_hrd_m.GetValue())
        self.on_hr_value_changed(event)

    def _create_controls(self):
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, _(u"Date:"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)

        bSizer4.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_date = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition,
                                                 wx.DefaultSize, wx.adv.DP_DEFAULT | wx.adv.DP_DROPDOWN)
        bSizer4.Add(self.m_ctrl_date, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer3.Add(bSizer4, 0, wx.EXPAND, 5)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"HR")), wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(0, 4, 0, 0)
        fgSizer1.AddGrowableCol(1)
        fgSizer1.AddGrowableCol(3)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText2 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"HR done: (H:M)"), wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)

        fgSizer1.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_hrd_h = wx.SpinCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1000, 0)
        fgSizer1.Add(self.m_ctrl_hrd_h, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_staticText3 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, _(u":"), wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        fgSizer1.Add(self.m_staticText3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_hrd_m = wx.SpinCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 59, 0)
        fgSizer1.Add(self.m_ctrl_hrd_m, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        fgSizer1.Add((0, 0), 1, wx.EXPAND, 5)

        self.m_ctrl_btn_50 = wx.Button(sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"+50%"), wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        fgSizer1.Add(self.m_ctrl_btn_50, 0, wx.ALL | wx.EXPAND, 5)

        fgSizer1.Add((0, 0), 1, wx.EXPAND, 5)

        self.m_ctrl_btn_100 = wx.Button(sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"+100%"), wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        fgSizer1.Add(self.m_ctrl_btn_100, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText4 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"HR Increased (H:M):"),
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)

        fgSizer1.Add(self.m_staticText4, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_hri_h = wx.SpinCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1000, 0)
        fgSizer1.Add(self.m_ctrl_hri_h, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_staticText5 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, _(u":"), wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)

        fgSizer1.Add(self.m_staticText5, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_hri_m = wx.SpinCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 59, 0)
        fgSizer1.Add(self.m_ctrl_hri_m, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_staticText7 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"HR Total (H:M) :"),
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)

        fgSizer1.Add(self.m_staticText7, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_hrtot_h = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.DefaultSize, wx.TE_READONLY)
        fgSizer1.Add(self.m_ctrl_hrtot_h, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_staticText8 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, _(u":"), wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)

        fgSizer1.Add(self.m_staticText8, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_hrtot_m = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.DefaultSize, wx.TE_READONLY)
        fgSizer1.Add(self.m_ctrl_hrtot_m, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        sbSizer1.Add(fgSizer1, 1, wx.EXPAND, 5)

        bSizer6.Add(sbSizer1, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"A")), wx.VERTICAL)

        fgSizer2 = wx.FlexGridSizer(0, 4, 0, 0)
        fgSizer2.AddGrowableCol(1)
        fgSizer2.AddGrowableCol(3)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText9 = wx.StaticText(sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"A Total (H:M):"), wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)

        fgSizer2.Add(self.m_staticText9, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_a_h = wx.SpinCtrl(sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                      wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1000, 0)
        fgSizer2.Add(self.m_ctrl_a_h, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_staticText10 = wx.StaticText(sbSizer2.GetStaticBox(), wx.ID_ANY, _(u":"), wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)

        fgSizer2.Add(self.m_staticText10, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_a_m = wx.SpinCtrl(sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                      wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 59, 0)
        fgSizer2.Add(self.m_ctrl_a_m, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        sbSizer2.Add(fgSizer2, 1, wx.EXPAND, 5)

        bSizer6.Add(sbSizer2, 0, wx.EXPAND | wx.ALL, 5)

        sbSizer21 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"VAC")), wx.VERTICAL)

        fgSizer21 = wx.FlexGridSizer(0, 4, 0, 0)
        fgSizer21.AddGrowableCol(1)
        fgSizer21.AddGrowableCol(3)
        fgSizer21.SetFlexibleDirection(wx.BOTH)
        fgSizer21.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText91 = wx.StaticText(sbSizer21.GetStaticBox(), wx.ID_ANY, _(u"Vac Total (H:M):"),
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText91.Wrap(-1)

        fgSizer21.Add(self.m_staticText91, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_vac_h = wx.SpinCtrl(sbSizer21.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1000, 0)
        fgSizer21.Add(self.m_ctrl_vac_h, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        self.m_staticText101 = wx.StaticText(sbSizer21.GetStaticBox(), wx.ID_ANY, _(u":"), wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.m_staticText101.Wrap(-1)

        fgSizer21.Add(self.m_staticText101, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_vac_m = wx.SpinCtrl(sbSizer21.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 59, 0)
        fgSizer21.Add(self.m_ctrl_vac_m, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        sbSizer21.Add(fgSizer21, 1, wx.EXPAND, 5)

        bSizer6.Add(sbSizer21, 0, wx.EXPAND | wx.ALL, 5)

        sbSizer7 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"Comment")), wx.VERTICAL)

        self.m_ctrl_comment = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.DefaultSize, wx.TE_MULTILINE)
        sbSizer7.Add(self.m_ctrl_comment, 1, wx.ALL | wx.EXPAND, 5)

        bSizer6.Add(sbSizer7, 1, wx.EXPAND | wx.ALL, 5)

        bSizer5.Add(bSizer6, 2, wx.EXPAND, 5)

        sbSizer6 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"Tags")), wx.VERTICAL)

        m_ctrl_list_tagsChoices = []
        self.m_ctrl_list_tags = wx.CheckListBox(sbSizer6.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                m_ctrl_list_tagsChoices, 0)
        sbSizer6.Add(self.m_ctrl_list_tags, 1, wx.ALL | wx.EXPAND, 5)

        self.m_ctrl_btn_tag = wx.Button(sbSizer6.GetStaticBox(), wx.ID_ANY, _(u"Add..."), wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        sbSizer6.Add(self.m_ctrl_btn_tag, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        bSizer5.Add(sbSizer6, 1, wx.ALL | wx.EXPAND, 5)

        bSizer3.Add(bSizer5, 1, wx.EXPAND, 5)

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1Save = wx.Button(self, wx.ID_OK)
        m_sdbSizer1.AddButton(self.m_sdbSizer1Save)
        self.m_sdbSizer1Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer1.AddButton(self.m_sdbSizer1Cancel)
        m_sdbSizer1.Realize()

        bSizer3.Add(m_sdbSizer1, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer3)
        self.Layout()
        bSizer3.Fit(self)

        self.Centre(wx.BOTH)
