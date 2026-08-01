from PySide6 import QtCore, QtGui, QtWidgets
from typing import Dict, List

def get_twse_tick_size(code: str, price: float) -> float:
    """
    台灣證券交易所 (TWSE) / 櫃買中心 (TPEx) 官方 Tick 升降單位計算器 (Rule 19 實作)
    區分：一般股票 (Equities) vs ETF (指數股票型基金受益憑證) 專屬雙軌規範
    """
    is_etf = code.startswith("00")
    
    if is_etf:
        # ★ TWSE ETF 專屬特規升降單位 ★
        if price < 50.0:
            return 0.01  # 未滿 50 元跳動 0.01 元 (例: 0056 在 49.40元)
        else:
            return 0.05  # 50 元以上跳動 0.05 元 (例: 0050 在 102.85元)
    else:
        # ★ 一般股票 (Equities) 官方級距 ★
        if price < 10.0:
            return 0.01
        elif price < 50.0:
            return 0.05
        elif price < 100.0:
            return 0.10
        elif price < 500.0:
            return 0.50  # 100~500 元跳動 0.50 元 (例: 鴻海 250.5元)
        elif price < 1000.0:
            return 1.00
        else:
            return 5.00  # 1000 元以上跳動 5.00 元 (例: 台積電 2425元、聯發科 3555元)

class FiveBidsWidget(QtWidgets.QWidget):
    """即時五檔委買 / 委賣報價欄 (符合 TWSE 官方股票與 ETF 跳動單位)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QtWidgets.QTableWidget(5, 4)
        self.table.setHorizontalHeaderLabels(["買張", "買價 (Bid)", "賣價 (Ask)", "賣張"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        layout.addWidget(self.table)
        self.set_mock_bids("2330", 2425.0)

    def set_mock_bids(self, code: str = "2330", base_price: float = 2425.0):
        """依據 TWSE 官方 Tick 升降單位計算並動態填入 5 檔委買與委賣價"""
        tick_size = get_twse_tick_size(code, base_price)

        bids_qty = [63, 51, 39, 27, 15]
        asks_qty = [23, 38, 53, 68, 83]

        for i in range(5):
            # 賣價 (Ask 1 ~ 5) 高於當前價
            ask_price = base_price + (i + 1) * tick_size
            # 買價 (Bid 1 ~ 5) 低於或等於當前價
            bid_price = base_price - i * tick_size

            # 買張 (欄 0)
            item_b_qty = QtWidgets.QTableWidgetItem(str(bids_qty[i]))
            item_b_qty.setTextAlignment(QtCore.Qt.AlignCenter)
            item_b_qty.setForeground(QtGui.QColor("#8C9BAE"))
            self.table.setItem(i, 0, item_b_qty)

            # 買價 (欄 1)
            fmt = ".2f" if tick_size < 1.0 else ".1f"
            item_bid = QtWidgets.QTableWidgetItem(f"{bid_price:{fmt}}")
            item_bid.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            item_bid.setForeground(QtGui.QColor("#FF3B69"))
            item_bid.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
            self.table.setItem(i, 1, item_bid)

            # 賣價 (欄 2)
            item_ask = QtWidgets.QTableWidgetItem(f"{ask_price:{fmt}}")
            item_ask.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            item_ask.setForeground(QtGui.QColor("#00E676"))
            item_ask.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
            self.table.setItem(i, 2, item_ask)

            # 賣張 (欄 3)
            item_a_qty = QtWidgets.QTableWidgetItem(str(asks_qty[i]))
            item_a_qty.setTextAlignment(QtCore.Qt.AlignCenter)
            item_a_qty.setForeground(QtGui.QColor("#8C9BAE"))
            self.table.setItem(i, 3, item_a_qty)
