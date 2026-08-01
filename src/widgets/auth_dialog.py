import os
import sys
from PySide6 import QtCore, QtGui, QtWidgets

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from src.utils.config_manager import ConfigManager
except ImportError:
    from utils.config_manager import ConfigManager

class AuthDialog(QtWidgets.QDialog):
    """永豐金 Shioaji API 登入與 CA 憑證驗證 Modal 視窗 (含 API Key 記憶功能)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔐 登入永豐金證券 API (含 CA 憑證驗證)")
        self.setFixedSize(560, 420)
        self.setModal(True)

        self.auth_data = None
        self._init_ui()
        self._load_saved_credentials()

    def _init_ui(self):
        # 高質感深色 Modal 視窗 QSS
        self.setStyleSheet("""
            QDialog {
                background-color: #16191E;
                color: #FFFFFF;
                font-family: "Microsoft JhengHei", "Segoe UI", sans-serif;
            }
            QLabel {
                color: #B0BEC5;
                font-weight: bold;
                font-size: 13px;
            }
            QLineEdit {
                background-color: #1E222A;
                border: 1px solid #2C323F;
                border-radius: 6px;
                padding: 8px 12px;
                color: #FFFFFF;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #00E5FF;
            }
            QCheckBox {
                color: #00E5FF;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton {
                background-color: #FF9800;
                color: #FFFFFF;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #FFA726;
            }
            QPushButton:pressed {
                background-color: #F57C00;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # 頂部標題說明
        title = QtWidgets.QLabel("🔐 永豐金證券 Shioaji API 實盤/憑證登入 (Rule 14 規範)")
        title.setStyleSheet("font-size: 15px; color: #00E5FF; margin-bottom: 6px;")
        layout.addWidget(title)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(QtWidgets.QLabel("身分證字號 (Person ID):"), 0, 0)
        self.input_person_id = QtWidgets.QLineEdit()
        self.input_person_id.setPlaceholderText("例如: H122511000")
        grid.addWidget(self.input_person_id, 0, 1)

        grid.addWidget(QtWidgets.QLabel("API Key:"), 1, 0)
        self.input_api_key = QtWidgets.QLineEdit()
        self.input_api_key.setPlaceholderText("請輸入永豐金 API Key")
        grid.addWidget(self.input_api_key, 1, 1)

        grid.addWidget(QtWidgets.QLabel("Secret Key:"), 2, 0)
        self.input_secret_key = QtWidgets.QLineEdit()
        self.input_secret_key.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_secret_key.setPlaceholderText("請輸入永豐金 Secret Key")
        grid.addWidget(self.input_secret_key, 2, 1)

        grid.addWidget(QtWidgets.QLabel(".pfx 憑證檔案路徑:"), 3, 0)
        ca_layout = QtWidgets.QHBoxLayout()
        self.input_ca_path = QtWidgets.QLineEdit()
        self.input_ca_path.setPlaceholderText("例如: E:/永豐API/Sinopac.pfx")
        btn_browse = QtWidgets.QPushButton("瀏覽...")
        btn_browse.setStyleSheet("background-color: #263238; padding: 6px 12px; font-size: 12px;")
        btn_browse.clicked.connect(self._browse_ca_file)
        ca_layout.addWidget(self.input_ca_path)
        ca_layout.addWidget(btn_browse)
        grid.addLayout(ca_layout, 3, 1)

        grid.addWidget(QtWidgets.QLabel("憑證密碼 (CA Password):"), 4, 0)
        self.input_ca_pwd = QtWidgets.QLineEdit()
        self.input_ca_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_ca_pwd.setPlaceholderText("請輸入 .pfx 憑證密碼")
        grid.addWidget(self.input_ca_pwd, 4, 1)

        layout.addLayout(grid)

        # 記憶 API KEY 功能勾選 (記憶設定)
        self.chk_remember = QtWidgets.QCheckBox("☑️ 記憶 API Key 與憑證設定 (安全儲存於本地 config.json)")
        layout.addWidget(self.chk_remember)

        # 底部按鈕
        btn_layout = QtWidgets.QHBoxLayout()
        btn_cancel = QtWidgets.QPushButton("取消")
        btn_cancel.setStyleSheet("background-color: #37474F;")
        btn_cancel.clicked.connect(self.reject)

        btn_submit = QtWidgets.QPushButton("🔥 驗證憑證並連線 (Activate CA & Login)")
        btn_submit.clicked.connect(self._on_submit)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_submit)
        layout.addLayout(btn_layout)

    def _browse_ca_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "選擇永豐金 CA 憑證檔案", "", "PFX Files (*.pfx);;All Files (*)")
        if file_path:
            self.input_ca_path.setText(file_path)

    def _load_saved_credentials(self):
        cfg = ConfigManager.load_config()
        if cfg.get("remember"):
            self.chk_remember.setChecked(True)
            self.input_person_id.setText(cfg.get("person_id", ""))
            self.input_api_key.setText(cfg.get("api_key", ""))
            self.input_secret_key.setText(cfg.get("secret_key", ""))
            self.input_ca_path.setText(cfg.get("ca_path", ""))
            self.input_ca_pwd.setText(cfg.get("ca_password", ""))

    def _on_submit(self):
        api_key = self.input_api_key.text().strip()
        secret_key = self.input_secret_key.text().strip()

        if not api_key or not secret_key:
            QtWidgets.QMessageBox.warning(self, "提示", "請至少輸入永豐金 API Key 與 Secret Key！")
            return

        remember = self.chk_remember.isChecked()
        cfg_data = {
            "remember": remember,
            "person_id": self.input_person_id.text().strip() if remember else "",
            "api_key": api_key if remember else "",
            "secret_key": secret_key if remember else "",
            "ca_path": self.input_ca_path.text().strip() if remember else "",
            "ca_password": self.input_ca_pwd.text().strip() if remember else ""
        }

        if remember:
            ConfigManager.save_config(cfg_data)
        else:
            ConfigManager.clear_config()

        self.auth_data = {
            "person_id": self.input_person_id.text().strip(),
            "api_key": api_key,
            "secret_key": secret_key,
            "ca_path": self.input_ca_path.text().strip(),
            "ca_password": self.input_ca_pwd.text().strip()
        }
        self.accept()
