import datetime
from PySide6 import QtCore, QtGui, QtWidgets

class MessageConsoleWidget(QtWidgets.QWidget):
    """系統訊息與 API 訂閱日誌欄 (Message Console Widget)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 標題列
        header = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("💻 系統廣播與 API 訂閱日誌欄 (Message Console)")
        title.setStyleSheet("font-weight: bold; color: #8C9BAE; font-size: 12px;")
        header.addWidget(title)

        header.addStretch()
        btn_clear = QtWidgets.QPushButton("🧹 清空日誌")
        btn_clear.setStyleSheet("background-color: #263238; font-size: 11px; padding: 3px 8px;")
        btn_clear.clicked.connect(self.clear_logs)
        header.addWidget(btn_clear)
        layout.addLayout(header)

        # 日誌終端視窗 (QTextEdit)
        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #0E1013;
                color: #00E5FF;
                font-family: "Consolas", "Courier New", monospace;
                font-size: 12px;
                border: 1px solid #1E222A;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.text_edit)

        self.log_info("SmartStock 系統核心引擎初始化完畢！")
        self.log_info("已成功連結永豐金 Shioaji API 實盤報價與 K線訂閱服務。")

    def log_info(self, msg: str):
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        self.text_edit.append(f"<span style='color:#8C9BAE;'>[{now_str}]</span> <span style='color:#00E5FF;'>[INFO]</span> {msg}")

    def log_success(self, msg: str):
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        self.text_edit.append(f"<span style='color:#8C9BAE;'>[{now_str}]</span> <span style='color:#00E676;'>[SUCCESS]</span> {msg}")

    def log_warning(self, msg: str):
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        self.text_edit.append(f"<span style='color:#8C9BAE;'>[{now_str}]</span> <span style='color:#FF9800;'>[WARN]</span> {msg}")

    def clear_logs(self):
        self.text_edit.clear()
