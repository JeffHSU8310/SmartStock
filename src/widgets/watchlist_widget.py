from PySide6 import QtCore, QtGui, QtWidgets
from typing import List, Dict

COMMON_SYMBOL_NAMES = {
    "2330": "台積電", "2317": "鴻海", "2454": "聯發科", "2308": "台達電",
    "2382": "廣達", "0050": "元大台灣50", "0056": "元大高股息",
    "00878": "國泰永續高股息", "00919": "群益台灣精選高息", "00929": "復華台灣科技優息",
    "00940": "元大台灣價值高息", "2881": "富邦金", "2882": "國泰金",
    "TX00": "台指期主力", "MX00": "小台期主力", "TM00": "微台期主力"
}

class WatchlistWidget(QtWidgets.QWidget):
    """自選股管理元件 (支援動態全真快照更新 update_quote 與排序增刪)"""
    stock_selected_signal = QtCore.Signal(str, str) # 發送 (股票代碼, 股票名稱)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._load_default_stocks()

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # 頂部控制欄 (輸入代碼 + 新增按鈕)
        input_box = QtWidgets.QHBoxLayout()
        self.input_code = QtWidgets.QLineEdit()
        self.input_code.setPlaceholderText("輸入股票代碼 (例: 00878)...")
        self.input_code.returnPressed.connect(self.add_stock)
        input_box.addWidget(self.input_code)

        btn_add = QtWidgets.QPushButton("➕ 新增")
        btn_add.setStyleSheet("background-color: #00E676; color: #121418; font-weight: bold;")
        btn_add.clicked.connect(self.add_stock)
        input_box.addWidget(btn_add)

        layout.addLayout(input_box)

        # 自選股表格 (代碼, 名稱, 成交價, 漲跌幅)
        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["代碼", "名稱", "成交價", "漲跌幅"])
        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.itemSelectionChanged.connect(self.on_row_selected)
        layout.addWidget(self.table)

        # 底部控制欄 (刪除 / 上移 / 下移)
        btn_box = QtWidgets.QHBoxLayout()
        btn_del = QtWidgets.QPushButton("🗑️ 刪除")
        btn_del.setStyleSheet("background-color: #FF3B69; color: #FFFFFF;")
        btn_del.clicked.connect(self.delete_stock)

        btn_up = QtWidgets.QPushButton("⬆️ 上移")
        btn_up.setStyleSheet("background-color: #1E222A; color: #FFFFFF;")
        btn_up.clicked.connect(self.move_up)

        btn_down = QtWidgets.QPushButton("⬇️ 下移")
        btn_down.setStyleSheet("background-color: #1E222A; color: #FFFFFF;")
        btn_down.clicked.connect(self.move_down)

        btn_box.addWidget(btn_del)
        btn_box.addWidget(btn_up)
        btn_box.addWidget(btn_down)
        layout.addLayout(btn_box)

    def _load_default_stocks(self):
        """初始自選股清單 (完全廢除寫死的假價格，成交價預設待全真 API 寫入)"""
        default_list = [
            ("2330", "台積電"),
            ("2317", "鴻海"),
            ("2454", "聯發科"),
            ("2308", "台達電"),
            ("2382", "廣達"),
            ("0050", "元大台灣50"),
            ("0056", "元大高股息"),
            ("TX00", "台指期主力")
        ]
        for code, name in default_list:
            self._insert_row(code, name, "--", "--")

    def _insert_row(self, code: str, name: str, price: str = "--", pct: str = "--"):
        row = self.table.rowCount()
        self.table.insertRow(row)

        item_code = QtWidgets.QTableWidgetItem(code)
        item_code.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.setItem(row, 0, item_code)

        item_name = QtWidgets.QTableWidgetItem(name)
        item_name.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.table.setItem(row, 1, item_name)

        item_price = QtWidgets.QTableWidgetItem(price)
        item_price.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.table.setItem(row, 2, item_price)

        item_pct = QtWidgets.QTableWidgetItem(pct)
        item_pct.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.table.setItem(row, 3, item_pct)

    def update_quote(self, code: str, price: float, pct_change: float, name: str = ""):
        """全真快照動態更新自選股列表之名稱、價格與漲跌幅 (高亮顯示顏色)"""
        for row in range(self.table.rowCount()):
            item_code = self.table.item(row, 0)
            if item_code and item_code.text() == code:
                # 0. 更新商品中文名稱 (若傳回真實名稱且當前名稱仍為舊預設)
                if name:
                    curr_name_item = self.table.item(row, 1)
                    if not curr_name_item or curr_name_item.text().startswith("股票 ") or curr_name_item.text() != name:
                        item_name = QtWidgets.QTableWidgetItem(name)
                        item_name.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.table.setItem(row, 1, item_name)

                # 1. 更新成交價
                item_price = QtWidgets.QTableWidgetItem(f"{price:.2f}")
                item_price.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                item_price.setForeground(QtGui.QColor("#FF3B69" if pct_change >= 0 else "#00E676"))
                self.table.setItem(row, 2, item_price)

                # 2. 更新漲跌幅
                sign = "+" if pct_change >= 0 else ""
                item_pct = QtWidgets.QTableWidgetItem(f"{sign}{pct_change:.2f}%")
                item_pct.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                item_pct.setForeground(QtGui.QColor("#FF3B69" if pct_change >= 0 else "#00E676"))
                self.table.setItem(row, 3, item_pct)
                break

    def add_stock(self):
        code = self.input_code.text().strip().upper()
        if not code:
            return
        
        # 避免重複新增
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == code:
                QtWidgets.QMessageBox.information(self, "提醒", f"股票代碼 {code} 已在自選股清單中！")
                self.input_code.clear()
                return

        name = COMMON_SYMBOL_NAMES.get(code, f"股票 {code}")

        self._insert_row(code, name, "--", "--")
        self.input_code.clear()
        
        # 自動選中新新增的行並觸發連動切換
        new_row = self.table.rowCount() - 1
        self.table.selectRow(new_row)

    def delete_stock(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)

    def move_up(self):
        row = self.table.currentRow()
        if row > 0:
            self._swap_rows(row, row - 1)
            self.table.selectRow(row - 1)

    def move_down(self):
        row = self.table.currentRow()
        if row < self.table.rowCount() - 1:
            self._swap_rows(row, row + 1)
            self.table.selectRow(row + 1)

    def _swap_rows(self, row1: int, row2: int):
        for col in range(4):
            item1 = self.table.takeItem(row1, col)
            item2 = self.table.takeItem(row2, col)
            self.table.setItem(row1, col, item2)
            self.table.setItem(row2, col, item1)

    def on_row_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            item_code = self.table.item(row, 0)
            item_name = self.table.item(row, 1)
            if item_code and item_name:
                self.stock_selected_signal.emit(item_code.text(), item_name.text())
