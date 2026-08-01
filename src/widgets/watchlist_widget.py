from PySide6 import QtCore, QtGui, QtWidgets
from typing import List, Dict, Callable

class WatchlistWidget(QtWidgets.QWidget):
    """自選股清單元件 (支援新增、刪除、上移、下移)"""
    stock_selected_signal = QtCore.Signal(str, str) # 發送 (code, name)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.stocks = [
            {"code": "2330", "name": "台積電", "price": 965.0, "pct": 1.58},
            {"code": "2317", "name": "鴻海", "price": 202.5, "pct": 1.76},
            {"code": "2454", "name": "聯發科", "price": 1240.0, "pct": -0.80},
            {"code": "2308", "name": "台達電", "price": 395.0, "pct": 2.07},
            {"code": "2382", "name": "廣達", "price": 288.0, "pct": 1.95},
            {"code": "0050", "name": "元大台灣50", "price": 182.5, "pct": 0.66},
            {"code": "TX00", "name": "台指期主力", "price": 22350.0, "pct": 0.81},
        ]
        self._init_ui()

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # 頂部標題與新增輸入欄
        top_box = QtWidgets.QHBoxLayout()
        self.input_code = QtWidgets.QLineEdit()
        self.input_code.setPlaceholderText("輸入股票代碼 (例: 2330)...")
        btn_add = QtWidgets.QPushButton("➕ 新增")
        btn_add.setStyleSheet("background-color: #00E676; color: #000000; font-weight: bold;")
        btn_add.clicked.connect(self.add_stock)

        top_box.addWidget(self.input_code)
        top_box.addWidget(btn_add)
        layout.addLayout(top_box)

        # 自選列表表格 (QTableWidget)
        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["代碼", "名稱", "成交價", "漲跌幅"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.table)

        # 底部管理控制按鈕列 (刪除, 上移, 下移)
        btn_box = QtWidgets.QHBoxLayout()
        btn_del = QtWidgets.QPushButton("🗑️ 刪除")
        btn_del.setStyleSheet("background-color: #D32F2F; color: #FFFFFF;")
        btn_del.clicked.connect(self.delete_stock)

        btn_up = QtWidgets.QPushButton("⬆️ 上移")
        btn_up.setStyleSheet("background-color: #37474F;")
        btn_up.clicked.connect(self.move_up)

        btn_down = QtWidgets.QPushButton("⬇️ 下移")
        btn_down.setStyleSheet("background-color: #37474F;")
        btn_down.clicked.connect(self.move_down)

        btn_box.addWidget(btn_del)
        btn_box.addWidget(btn_up)
        btn_box.addWidget(btn_down)
        layout.addLayout(btn_box)

        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(len(self.stocks))
        for row, s in enumerate(self.stocks):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(s["code"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(s["name"]))

            price_item = QtWidgets.QTableWidgetItem(f"{s['price']:.2f}")
            pct_item = QtWidgets.QTableWidgetItem(f"{s['pct']:+.2f}%")

            color = '#FF3B69' if s['pct'] >= 0 else '#00E676'
            price_item.setForeground(QtGui.QColor(color))
            pct_item.setForeground(QtGui.QColor(color))

            self.table.setItem(row, 2, price_item)
            self.table.setItem(row, 3, pct_item)

    def on_item_clicked(self, item):
        row = item.row()
        code = self.table.item(row, 0).text()
        name = self.table.item(row, 1).text()
        self.stock_selected_signal.emit(code, name)

    def add_stock(self):
        code = self.input_code.text().strip()
        if not code:
            return
        # 避免重複
        for s in self.stocks:
            if s["code"] == code:
                QtWidgets.QMessageBox.information(self, "提示", f"股票代碼 {code} 已在自選股清單中！")
                return

        # 預設新增股票資料
        self.stocks.append({"code": code, "name": f"股票 {code}", "price": 100.0, "pct": 0.0})
        self.input_code.clear()
        self.refresh_table()

    def delete_stock(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.stocks):
            QtWidgets.QMessageBox.warning(self, "提示", "請先選擇欲刪除的自選股！")
            return
        del self.stocks[row]
        self.refresh_table()

    def move_up(self):
        row = self.table.currentRow()
        if row > 0:
            self.stocks[row], self.stocks[row - 1] = self.stocks[row - 1], self.stocks[row]
            self.refresh_table()
            self.table.selectRow(row - 1)

    def move_down(self):
        row = self.table.currentRow()
        if row >= 0 and row < len(self.stocks) - 1:
            self.stocks[row], self.stocks[row + 1] = self.stocks[row + 1], self.stocks[row]
            self.refresh_table()
            self.table.selectRow(row + 1)
