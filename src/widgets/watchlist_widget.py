from PySide6 import QtCore, QtGui, QtWidgets
from typing import List, Dict

COMMON_SYMBOL_NAMES = {
    "2330": "台積電", "2317": "鴻海", "2454": "聯發科", "2308": "台達電",
    "2382": "廣達", "0050": "元大台灣50", "0056": "元大高股息",
    "00878": "國泰永續高股息", "00919": "群益台灣精選高息", "00929": "復華台灣科技優息",
    "00940": "元大台灣價值高息", "2881": "富邦金", "2882": "國泰金",
    "TX00": "台指期主力", "MX00": "小台期主力", "TM00": "微台期主力"
}

DEFAULT_GROUPS_DATA = {
    "預設自選": [
        ("2330", "台積電"), ("2317", "鴻海"), ("2454", "聯發科"),
        ("2308", "台達電"), ("2382", "廣達"), ("0050", "元大台灣50"),
        ("0056", "元大高股息"), ("TX00", "台指期主力")
    ],
    "核心庫存": [
        ("2330", "台積電"), ("2454", "聯發科"), ("0050", "元大台灣50")
    ],
    "ETF追蹤": [
        ("0050", "元大台灣50"), ("0056", "元大高股息"), ("00878", "國泰永續高股息"),
        ("00919", "群益台灣精選高息"), ("00929", "復華台灣科技優息")
    ],
    "期貨權證": [
        ("TX00", "台指期主力")
    ],
    "觀察清單": [
        ("2308", "台達電"), ("2382", "廣達")
    ]
}

class WatchlistWidget(QtWidgets.QWidget):
    """自選股多群組管理元件 (支援自訂群組名稱、新增/修改/刪除群組與快照更新)"""
    stock_selected_signal = QtCore.Signal(str, str) # 發送 (股票代碼, 股票名稱)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.groups_data = dict(DEFAULT_GROUPS_DATA)
        self.current_group_name = "預設自選"

        self._init_ui()
        self._load_group_stocks(self.current_group_name)

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # 1. 頂部群組控制列 (群組下拉選單 + ⚙️ 管理菜單)
        group_box = QtWidgets.QHBoxLayout()
        group_box.addWidget(QtWidgets.QLabel("📁 群組:"))
        
        self.combo_groups = QtWidgets.QComboBox()
        self.combo_groups.setStyleSheet("background-color: #1E222A; color: #00E5FF; font-weight: bold; padding: 4px 8px;")
        for g_name in self.groups_data.keys():
            self.combo_groups.addItem(g_name)
        self.combo_groups.currentTextChanged.connect(self.on_group_changed)
        group_box.addWidget(self.combo_groups, stretch=1)

        # ⚙️ 群組管理選單按鈕
        self.btn_group_menu = QtWidgets.QPushButton("⚙️ 管理")
        self.btn_group_menu.setStyleSheet("background-color: #1E222A; color: #FFFFFF; font-size: 12px; padding: 4px 8px;")
        self._setup_group_menu()
        group_box.addWidget(self.btn_group_menu)

        layout.addLayout(group_box)

        # 2. 股票代碼輸入欄與➕新增按鈕
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

        # 3. 自選股表格 (代碼, 名稱, 成交價, 漲跌幅)
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

        # 4. 底部控制欄 (刪除 / 上移 / 下移)
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

    def _setup_group_menu(self):
        """配置⚙️群組管理彈出菜單 (暗黑底亮白字，淺底純黑字貫徹鐵律)"""
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #1E222A;
                color: #FFFFFF;
                border: 1px solid #2C323F;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                background-color: transparent;
                color: #FFFFFF;
                padding: 8px 24px;
                border-radius: 4px;
                font-weight: bold;
            }
            QMenu::item:selected {
                background-color: #0066FF;
                color: #FFFFFF;
            }
        """)
        
        act_add = menu.addAction("➕ 新增群組...")
        act_add.triggered.connect(self.create_new_group)

        act_rename = menu.addAction("✏️ 重新命名當前群組...")
        act_rename.triggered.connect(self.rename_current_group)

        act_del = menu.addAction("🗑️ 刪除當前群組")
        act_del.triggered.connect(self.delete_current_group)

        self.btn_group_menu.setMenu(menu)

    def create_new_group(self):
        """➕ 新增群組對話框"""
        text, ok = QtWidgets.QInputDialog.getText(self, "新增自選股群組", "請輸入新群組名稱:")
        if ok and text.strip():
            g_name = text.strip()
            if g_name in self.groups_data:
                QtWidgets.QMessageBox.information(self, "提醒", f"群組 [{g_name}] 已存在！")
                return
            self.groups_data[g_name] = []
            self.combo_groups.addItem(g_name)
            self.combo_groups.setCurrentText(g_name)

    def rename_current_group(self):
        """✏️ 重新命名當前群組"""
        curr = self.combo_groups.currentText()
        text, ok = QtWidgets.QInputDialog.getText(self, "修改群組名稱", f"請輸入 [{curr}] 的新名稱:", text=curr)
        if ok and text.strip() and text.strip() != curr:
            new_name = text.strip()
            if new_name in self.groups_data:
                QtWidgets.QMessageBox.information(self, "提醒", f"群組 [{new_name}] 已存在！")
                return
            self.groups_data[new_name] = self.groups_data.pop(curr)
            idx = self.combo_groups.currentIndex()
            self.combo_groups.setItemText(idx, new_name)
            self.current_group_name = new_name

    def delete_current_group(self):
        """🗑️ 刪除當前群組"""
        if len(self.groups_data) <= 1:
            QtWidgets.QMessageBox.warning(self, "警告", "無法刪除！系統至少需要保留一個自選股群組。")
            return
        
        curr = self.combo_groups.currentText()
        reply = QtWidgets.QMessageBox.question(
            self, "確認刪除群組", f"您確定要刪除自選股群組 [{curr}] 嗎？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.groups_data.pop(curr, None)
            idx = self.combo_groups.currentIndex()
            self.combo_groups.removeItem(idx)

    def on_group_changed(self, group_name: str):
        """切換群組事件」"""
        if not group_name or group_name not in self.groups_data:
            return
        self.current_group_name = group_name
        self._load_group_stocks(group_name)

    def _load_group_stocks(self, group_name: str):
        """載入特定群組股票至 QTableWidget"""
        self.table.setRowCount(0)
        stock_list = self.groups_data.get(group_name, [])
        for code, name in stock_list:
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
                if name:
                    curr_name_item = self.table.item(row, 1)
                    if not curr_name_item or curr_name_item.text().startswith("股票 ") or curr_name_item.text() != name:
                        item_name = QtWidgets.QTableWidgetItem(name)
                        item_name.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        self.table.setItem(row, 1, item_name)

                item_price = QtWidgets.QTableWidgetItem(f"{price:.2f}")
                item_price.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                item_price.setForeground(QtGui.QColor("#FF3B69" if pct_change >= 0 else "#00E676"))
                self.table.setItem(row, 2, item_price)

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
        
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == code:
                QtWidgets.QMessageBox.information(self, "提醒", f"股票代碼 {code} 已在當前群組 [{self.current_group_name}] 清單中！")
                self.input_code.clear()
                return

        name = COMMON_SYMBOL_NAMES.get(code, f"股票 {code}")
        self._insert_row(code, name, "--", "--")
        
        # 更新群組記憶
        if self.current_group_name in self.groups_data:
            self.groups_data[self.current_group_name].append((code, name))

        self.input_code.clear()
        
        new_row = self.table.rowCount() - 1
        self.table.selectRow(new_row)

    def delete_stock(self):
        row = self.table.currentRow()
        if row >= 0:
            item_code = self.table.item(row, 0)
            if item_code:
                code_to_del = item_code.text()
                if self.current_group_name in self.groups_data:
                    self.groups_data[self.current_group_name] = [
                        (c, n) for c, n in self.groups_data[self.current_group_name] if c != code_to_del
                    ]
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
