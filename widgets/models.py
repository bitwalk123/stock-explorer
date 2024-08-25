from typing import Any, Union

import numpy as np
import pandas as pd
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)


class PandasModel(QAbstractTableModel):
    __version__ = '0.0.1'

    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self._df = df

    def columnCount(self, index: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        if index == QModelIndex():
            return len(self._df.columns)

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        value = self._df.iloc[row, col]

        if role == Qt.ItemDataRole.DisplayRole:
            return str(value)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if (type(value) is np.int64) | (type(value) is np.float64):
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            else:
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

    def getDataFrame(self) -> pd.DataFrame:
        return self._df

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._df.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._df.index[section])

    def rowCount(self, index: Union[QModelIndex, QPersistentModelIndex] = ...) -> int:
        if index == QModelIndex():
            return len(self._df)
