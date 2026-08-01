from PySide6 import QtCore, QtGui, QtWidgets

class OrderToolbarWidget(QtWidgets.QWidget):
    """快捷下單工具欄元件 (支援實盤 / 模擬帳戶選擇)"""
    order_submitted_signal = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        title = QtWidgets.QLabel("⚡ 快捷下單工具欄 (Quick Order)")
        title.setStyleSheet("font-weight: bold; color: #FFD700; font-size: 12px;")
        layout.addWidget(title)

        grid = QtWidgets.QGridLayout()

        # 1. 新增帳戶選擇列 (圖片 3 需求修復)
        grid.addWidget(QtWidgets.QLabel("下單帳戶:"), 0, 0)
        self.combo_account = QtWidgets.QComboBox()
        self.combo_account.addItems([
            "🟢 永豐金實盤帳戶 (SinoPac Real)",
            "🟡 智慧模擬/虛擬交易帳戶 (Paper Trading)"
        ])
        self.combo_account.setStyleSheet("color: #00E5FF; font-weight: bold;")
        grid.addWidget(self.combo_account, 0, 1, 1, 3)

        # 2. 商品與委託條件
        grid.addWidget(QtWidgets.QLabel("商品代碼:"), 1, 0)
        self.input_code = QtWidgets.QLineEdit("2330")
        grid.addWidget(self.input_code, 1, 1)

        grid.addWidget(QtWidgets.QLabel("委託類型:"), 1, 2)
        self.combo_type = QtWidgets.QComboBox()
        self.combo_type.addItems(["ROD (當日有效)", "IOC (立即成交否則取消)", "FOK (立即全部成交否則取消)"])
        grid.addWidget(self.combo_type, 1, 3)

        grid.addWidget(QtWidgets.QLabel("委託價格:"), 2, 0)
        self.input_price = QtWidgets.QLineEdit("965.0")
        grid.addWidget(self.input_price, 2, 1)

        grid.addWidget(QtWidgets.QLabel("委託張數:"), 2, 2)
        self.input_qty = QtWidgets.QLineEdit("1")
        grid.addWidget(self.input_qty, 2, 3)

        layout.addLayout(grid)

        # 買進與賣出按鈕
        btn_box = QtWidgets.QHBoxLayout()
        btn_buy = QtWidgets.QPushButton("🔴 買進下單 (BUY)")
        btn_buy.setStyleSheet("background-color: #FF3B69; font-size: 13px; font-weight: bold; padding: 10px;")
        btn_buy.clicked.connect(lambda: self.submit_order("BUY"))

        btn_sell = QtWidgets.QPushButton("🟢 賣出下單 (SELL)")
        btn_sell.setStyleSheet("background-color: #00E676; color: #000000; font-size: 13px; font-weight: bold; padding: 10px;")
        btn_sell.clicked.connect(lambda: self.submit_order("SELL"))

        btn_box.addWidget(btn_buy)
        btn_box.addWidget(btn_sell)
        layout.addLayout(btn_box)

    def set_symbol(self, code: str, price: float = 965.0):
        self.input_code.setText(code)
        self.input_price.setText(f"{price:.1f}")

    def submit_order(self, action: str):
        order_info = {
            "account": self.combo_account.currentText(),
            "action": action,
            "code": self.input_code.text().strip(),
            "price": self.input_price.text().strip(),
            "qty": self.input_qty.text().strip(),
            "type": self.combo_type.currentText().split()[0]
        }
        self.order_submitted_signal.emit(order_info)
