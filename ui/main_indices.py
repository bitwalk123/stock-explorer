from PySide6.QtCore import Qt

from ui.dock_indices import DockIndices
from ui.statusbar_indices import StatusbarIndices
from ui.toolbar_indices import ToolBarIndices
from widgets.charts import Trend
from widgets.tab_panels import TabPanelMain


class MainIndices(TabPanelMain):
    tab_label = '株価指数'

    def __init__(self, parent):
        super().__init__(parent)
        self.toolbar = None
        self.dock_right = None
        self.dock_bottom = None
        self.statusbar = None
        self.sub_good_bad = None

        self.init_ui()

    def init_ui(self):
        # ToolBar
        self.toolbar = toolbar = ToolBarIndices(self)
        self.addToolBar(toolbar)
        # Right Dock
        self.dock_right = dock_right = DockIndices(self)
        #dock_right.tickerSelected.connect(self.on_disp_update)
        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            dock_right
        )
        # StatusBar
        self.statusbar = StatusbarIndices(self)
        self.statusbar.setSizeGripEnabled(True)
        self.setStatusBar(self.statusbar)

        # CandleStick chart as default
        chart = Trend()
        self.setCentralWidget(chart)
