#!/usr/bin/env/ python3

import wx

import gettext
_ = gettext.gettext

class FrameSettings ( wx.Dialog ):
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Settings"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

        self._create_controls()

    def _create_controls(self):
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        sbSizer6 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _(u"Auto load project")), wx.HORIZONTAL)

        self.m_staticText12 = wx.StaticText(sbSizer6.GetStaticBox(), wx.ID_ANY, _(u"Project:"), wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)

        sbSizer6.Add(self.m_staticText12, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_ctrl_filepicker = wx.FilePickerCtrl(sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                   _(u"Select a file"), _(u"*.kdb"), wx.DefaultPosition,
                                                   wx.Size(300, -1),
                                                   wx.FLP_DEFAULT_STYLE | wx.FLP_FILE_MUST_EXIST | wx.FLP_OPEN | wx.FLP_USE_TEXTCTRL)
        sbSizer6.Add(self.m_ctrl_filepicker, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer7.Add(sbSizer6, 1, wx.ALL | wx.EXPAND, 5)

        m_sdbSizer2 = wx.StdDialogButtonSizer()
        self.m_sdbSizer2OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer2.AddButton(self.m_sdbSizer2OK)
        self.m_sdbSizer2Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer2.AddButton(self.m_sdbSizer2Cancel)
        m_sdbSizer2.Realize()

        bSizer7.Add(m_sdbSizer2, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer7)
        self.Layout()
        bSizer7.Fit(self)

        self.Centre(wx.BOTH)