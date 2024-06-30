from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDockWidget, QSlider


class DTADockSlider(QDockWidget):
    def __init__(self):
        super().__init__()
        slider = QSlider()
        slider.setOrientation(Qt.Orientation.Horizontal)
        self.setWidget(slider)


