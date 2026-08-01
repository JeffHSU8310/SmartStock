from PySide6 import QtCore, QtGui, QtWidgets

class FiveBidsWidget(QtWidgets.QWidget):
    """五檔即時報價欄元件 (Five-Bids & Ask Panel)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 標題
        title = QtWidgets.QLabel("📊 即時五檔委買 / 委賣報價 (Five-Bids)")
        title.setStyleSheet("font-weight: bold; color: #00E5FF; font-size: 12px;")
        layout.addWidget(title)

        # 五檔報價表格 (QTableWidget)
        self.table = QtWidgets.QTableWidget(5, 4)
        self.table.setHorizontalHeaderLabels(["買張", "買價 (Bid)", "賣價 (Ask)", "賣張"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)
        self.set_mock_bids(965.0)

    def set_mock_bids(self, price: float = 965.0):
        """填入模擬五檔報價數據"""
        for i in range(5):
            bid_p = price - (i + 1) * 0.5
            ask_p = price + (i + 1) * 0.5
            bid_v = (5 - i) * 12 + 3
            ask_v = (i + 1) * 15 + 8

            item_bid_v = QtWidgets.QTableWidgetItem(str(bid_v))
            item_bid_p = QtWidgets.QTableWidgetItem(f"{bid_p:.1f}")
            item_ask_p = QtWidgets.QTableWidgetItem(f"{ask_p:.1f}")
            item_ask_v = QtWidgets.QTableWidgetItem(str(ask_v))

            item_bid_p.setForeground(QtGui.QColor('#FF3B69'))
            item_ask_p.setForeground(QtGui.QColor('#00E676'))

            self.table.setItem(i, 0, item_bid_v)
            self.table.setItem(i, 1, item_bid_p)
            self.table.setItem(i, 2, item_ask_p)
            self.table.setItem(i, 3, item_ask_v)
