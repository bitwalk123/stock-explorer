from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDockWidget, QSlider, QHBoxLayout, QWidget, QLabel, QSizePolicy


class DTADockSlider(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setFeatures(
            QDockWidget.DockWidgetFeature.NoDockWidgetFeatures
        )

        base = QWidget()
        self.setWidget(base)

        layout = QHBoxLayout()
        base.setLayout(layout)

        self.label = label = QLabel()
        label.setStyleSheet("""
            QLabel {font-family: monospace;}
        """)
        label.setMinimumWidth(50)
        label.setAlignment(Qt.AlignmentFlag.AlignRight)
        label.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Preferred
        )
        layout.addWidget(label)

        slider = QSlider()
        slider.setRange(0, 18000)
        slider.setOrientation(
            Qt.Orientation.Horizontal
        )
        slider.setTickPosition(
            QSlider.TickPosition.TicksBothSides
        )
        slider.setTickInterval(600)
        slider.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        slider.valueChanged.connect(self.value_changed)
        layout.addWidget(slider)

        self.value_changed(slider.value())

    def value_changed(self, value: int):
        self.label.setText(str(value))
