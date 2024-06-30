from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDockWidget, QSlider


class DTADockSlider(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        slider = QSlider()
        slider.setRange(0, 18000)
        slider.setOrientation(Qt.Orientation.Horizontal)
        slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        slider.setTickInterval(600)
        slider.valueChanged.connect(self.value_changed)
        self.setWidget(slider)

    def value_changed(self, value: int):
        print(value)
