import math
import wx
import wx.lib.plot as plot

import gettext
_ = gettext.gettext

class FrameGraph ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        self._create_controls()

        # 2. Préparation des données (x, y)
        donnees = [(x / 10.0, math.sin(x / 10.0)) for x in range(0, 100)]

        # 3. Création de la ligne/courbe
        ligne = plot.PolyLine(donnees, legend="Sinus", colour="blue", width=2)

        # 4. Création du graphique avec la liste des éléments à afficher
        graphique = plot.PlotGraphics([ligne], "Graphique Sinus", "Axe X", "Axe Y")

        # 5. Affichage du graphique dans le canvas
        self.m_ctrl_plot.Draw(graphique)
        
        #self._create_controls()

    def _create_controls(self):
        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.m_ctrl_plot = plot.PlotCanvas(self, wx.ID_ANY)
        bSizer8.Add(self.m_ctrl_plot, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer8)
        self.Layout()

