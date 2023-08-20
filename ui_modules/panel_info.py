from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame, QSizePolicy

from functions.get_volume_median_with_code_start import get_volume_median_with_code_start


class PanelInfo(QWidget):

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        title_code = QLabel('Code')
        title_code.setContentsMargins(0, 0, 0, 0)
        title_code.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        title_code.setLineWidth(2)
        layout.addWidget(title_code)

        self.disp_code = QLabel()
        self.disp_code.setContentsMargins(0, 0, 0, 0)
        self.disp_code.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.disp_code.setLineWidth(2)
        layout.addWidget(self.disp_code)

        title_volume = QLabel('Volume(median)')
        title_volume.setContentsMargins(0, 0, 0, 0)
        title_volume.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        title_volume.setLineWidth(2)
        layout.addWidget(title_volume)

        self.disp_volume = QLabel()
        self.disp_volume.setContentsMargins(0, 0, 0, 0)
        self.disp_volume.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.disp_volume.setLineWidth(2)
        layout.addWidget(self.disp_volume)

        # 余白のスペーサ
        hpad = QWidget()
        hpad.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        layout.addWidget(hpad)

    def update_ticker(self, code: int, start: int):
        self.disp_code.setText('%d.T' % code)
        volume_median = get_volume_median_with_code_start(code, start)
        self.disp_volume.setText('%d' % volume_median)