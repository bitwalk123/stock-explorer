#!/usr/bin/env python
# coding: utf-8
# Reference
# https://doc.qt.io/qtforpython/examples/example_external__pandas.html
from typing import Any

import numpy as np
import pandas as pd
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)


class TblPredictModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        return self._dataframe.shape[0]

    def columnCount(self, parent=QModelIndex()) -> int:
        return self._dataframe.shape[1]

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        row = index.row()
        col = index.column()
        value = self._dataframe.iloc[row, col]

        if role == Qt.ItemDataRole.DisplayRole:
            if type(value) is str:
                return value
            elif type(value) is np.float64:
                if self._dataframe.columns[col] == 'R2':
                    return '%.3f' % value
                else:
                    return '%.1f' % value
            else:
                return str(value)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if (type(value) is np.int64) | (type(value) is np.float64):
                flag = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            else:
                flag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            return flag

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return section + 1

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if orientation == Qt.Vertical:
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

        return None
