#!/usr/bin/env/ python3

import wx

from kopp.framemain import FrameMain


##########################################################
#  MAIN APP CLASS
##########################################################


class KoppApp(wx.App):
    """
    Main application class
    initialize the MainFrame class and the main loop
    """

    def OnInit(self):
        dlg = FrameMain(None)
        dlg.Show(True)
        self.SetTopWindow(dlg)
        return True

app = KoppApp()
app.MainLoop()
