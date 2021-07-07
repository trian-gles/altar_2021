# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from random import randrange

results = {}
app = wx.App(False)
###########################################################################
## Class AltarFrame
###########################################################################


class AltarFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 487), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.title = wx.StaticText(self, wx.ID_ANY, u"ALTAR Menu", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        self.title.Wrap(-1)
        self.title.SetFont(wx.Font(14, 75, 90, 90, False, "ＭＳ Ｐゴシック"))

        bSizer1.Add(self.title, 0, wx.ALL | wx.EXPAND, 5)

        self.username_label = wx.StaticText(self, wx.ID_ANY, u"Username:", wx.DefaultPosition, wx.DefaultSize,
                                            wx.ALIGN_CENTRE)
        self.username_label.Wrap(-1)
        bSizer1.Add(self.username_label, 0, wx.ALL | wx.EXPAND, 5)

        self.username_entry = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.username_entry, 0, wx.ALL | wx.EXPAND, 5)

        self.config_label = wx.StaticText(self, wx.ID_ANY, u"Player Configuration:", wx.DefaultPosition, wx.DefaultSize,
                                          0)
        self.config_label.Wrap(-1)
        bSizer1.Add(self.config_label, 0, wx.ALL, 5)

        player_configChoices = [u"SINGLE PLAYER", u"LAN", u"REMOTE"]
        self.player_config = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, player_configChoices, 0)
        self.player_config.SetSelection(0)
        bSizer1.Add(self.player_config, 0, wx.ALL | wx.EXPAND, 5)

        self.audio_chk = wx.CheckBox(self, wx.ID_ANY, u"Audio", wx.DefaultPosition, wx.DefaultSize, 0)
        self.audio_chk.SetValue(True)
        bSizer1.Add(self.audio_chk, 0, wx.ALL | wx.EXPAND, 5)

        self.project_chk = wx.CheckBox(self, wx.ID_ANY, u"Projector", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.project_chk, 0, wx.ALL, 5)

        self.fullscreen_chk = wx.CheckBox(self, wx.ID_ANY, u"Fullscreen", wx.DefaultPosition, wx.DefaultSize, 0)
        self.fullscreen_chk.SetValue(True)
        bSizer1.Add(self.fullscreen_chk, 0, wx.ALL, 5)

        self.admin_chk = wx.CheckBox(self, wx.ID_ANY, u"Admin", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.admin_chk, 0, wx.ALL, 5)

        self.submit_btn = wx.Button(self, wx.ID_ANY, u"Submit", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.submit_btn, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.submit_btn.Bind(wx.EVT_BUTTON, self.action)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def action(self, event):
        results["username"] = self.username_entry.GetValue()
        if not results["username"]:
            results["username"] = str({randrange(0, 100000)})

        results["audio"] = self.audio_chk.GetValue()
        results["local"] = self.player_config.GetCurrentSelection()
        results["admin"] = self.admin_chk.GetValue()
        results["project"] = self.project_chk.GetValue()
        results["fullscreen"] = self.fullscreen_chk.GetValue()
        wx.Exit()


def main() -> dict:
    frame = AltarFrame(None)
    frame.Show(True)
    app.MainLoop()
    return results

if __name__ == "__main__":
    print(main())