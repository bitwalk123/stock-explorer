from PySide6.QtWidgets import QDockWidget, QWidget

from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


class DockNavigator(QDockWidget):

    def __init__(self, parent, canvas):
        super().__init__(parent)
        self.parent = parent
        self.setTitleBarWidget(QWidget(None))
        self.setContentsMargins(0, 0, 0, 0)
        navtoolbar = NavigationToolbar(canvas, self)
        self.setWidget(navtoolbar)
