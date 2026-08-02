from PySide6 import QtCore, QtGui, QtWidgets
from typing import Dict, Any

LINE_STYLES = {
    "實線 (SolidLine)": QtCore.Qt.SolidLine,
    "虛線 (DashLine)": QtCore.Qt.DashLine,
    "點線 (DotLine)": QtCore.Qt.DotLine,
    "點劃線 (DashDotLine)": QtCore.Qt.DashDotLine
}

LINE_STYLE_NAMES = list(LINE_STYLES.keys())

DEFAULT_INDICATOR_CONFIG = {
    "ma_enabled": True,
    "ma_items": [
        {"enabled": True, "type": "SMA", "period": 5, "color": "#FFD700", "style": "實線 (SolidLine)"},
        {"enabled": True, "type": "SMA", "period": 10, "color": "#FF9800", "style": "實線 (SolidLine)"},
        {"enabled": True, "type": "SMA", "period": 20, "color": "#FFFFFF", "style": "實線 (SolidLine)"},
        {"enabled": True, "type": "SMA", "period": 60, "color": "#00E5FF", "style": "實線 (SolidLine)"},
        {"enabled": True, "type": "SMA", "period": 120, "color": "#E040FB", "style": "實線 (SolidLine)"},
        {"enabled": False, "type": "SMA", "period": 240, "color": "#00E676", "style": "虛線 (DashLine)"},
        {"enabled": False, "type": "SMA", "period": 300, "color": "#FF3B69", "style": "點線 (DotLine)"}
    ],
    "bb_enabled": True,
    "bb_period": 20,
    "bb_k1": 1.0,
    "bb_k2": 2.0,
    "bb_mid_color": "#FFD700",
    "bb_mid_style": "實線 (SolidLine)",
    "bb_b1_color": "#00E5FF",
    "bb_b1_style": "虛線 (DashLine)",
    "bb_b2_color": "#E040FB",
    "bb_b2_style": "點劃線 (DashDotLine)",
    "sub1_type": "成交量 (Volume)",
    "sub2_type": "MACD"
}

class ColorButton(QtWidgets.QPushButton):
    """帶有色彩預覽與調色盤彈出視窗的自訂按鈕"""
    color_changed = QtCore.Signal(str)

    def __init__(self, color_hex: str = "#FFFFFF", parent=None):
        super().__init__(parent)
        self._color = color_hex
        self.clicked.connect(self._choose_color)
        self._update_style()

    def color(self) -> str:
        return self._color

    def set_color(self, color_hex: str):
        self._color = color_hex
        self._update_style()

    def _update_style(self):
        self.setText(self._color)
        # 依色彩亮度決定文字顏色
        bg = QtGui.QColor(self._color)
        text_col = "#000000" if (bg.red()*0.299 + bg.green()*0.587 + bg.blue()*0.114) > 180 else "#FFFFFF"
        self.setStyleSheet(f"background-color: {self._color}; color: {text_col}; font-weight: bold; border-radius: 4px; padding: 4px 10px;")

    def _choose_color(self):
        col = QtWidgets.QColorDialog.getColor(QtGui.QColor(self._color), self, "選擇指標線型顏色")
        if col.isValid():
            self._color = col.name().upper()
            self._update_style()
            self.color_changed.emit(self._color)

class IndicatorSettingsDialog(QtWidgets.QDialog):
    """技術指標詳細設定視窗 (支援 7 組均線 SMA/EMA、布林通道雙層上下限、副圖指標切換與調色盤選色)"""
    config_saved_signal = QtCore.Signal(dict)

    def __init__(self, current_config: Dict[str, Any] = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ 技術指標詳細設定與顏色調色盤 (Indicator Settings)")
        self.resize(780, 620)
        self.config = dict(DEFAULT_INDICATOR_CONFIG)
        if current_config:
            self.config.update(current_config)

        self._init_ui()

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Tab Widget
        self.tabs = QtWidgets.QTabWidget()
        
        # Tab 1: 主圖指標設定
        tab_main = QtWidgets.QWidget()
        self._setup_main_indicators_tab(tab_main)
        self.tabs.addTab(tab_main, "📈 主圖指標設定 (均線 / 布林通道)")

        # Tab 2: 副圖指標設定
        tab_sub = QtWidgets.QWidget()
        self._setup_sub_indicators_tab(tab_sub)
        self.tabs.addTab(tab_sub, "📊 副圖指標設定 (MACD / KDJ / RSI 等)")

        layout.addWidget(self.tabs)

        # 底部控制按鈕
        btn_box = QtWidgets.QHBoxLayout()
        btn_reset = QtWidgets.QPushButton("🔄 恢復預設值")
        btn_reset.setStyleSheet("background-color: #37474F; color: #FFFFFF; font-weight: bold; padding: 8px 16px;")
        btn_reset.clicked.connect(self._reset_defaults)

        btn_cancel = QtWidgets.QPushButton("❌ 取消")
        btn_cancel.setStyleSheet("background-color: #263238; color: #FFFFFF; font-weight: bold; padding: 8px 16px;")
        btn_cancel.clicked.connect(self.reject)

        btn_save = QtWidgets.QPushButton("💾 套用並儲存設定")
        btn_save.setStyleSheet("background-color: #0066FF; color: #FFFFFF; font-weight: bold; padding: 8px 20px;")
        btn_save.clicked.connect(self._save_config)

        btn_box.addWidget(btn_reset)
        btn_box.addStretch()
        btn_box.addWidget(btn_cancel)
        btn_box.addWidget(btn_save)

        layout.addLayout(btn_box)

    def _setup_main_indicators_tab(self, widget: QtWidgets.QWidget):
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(12)

        # 1. 均線設定 Group Box (支援 7 組獨立均線)
        box_ma = QtWidgets.QGroupBox("1. 移動平均線 (Moving Averages - 支援 7 組獨立設定)")
        layout_ma = QtWidgets.QVBoxLayout(box_ma)
        
        self.chk_ma_master = QtWidgets.QCheckBox("顯示移動平均線 (Enable MAs)")
        self.chk_ma_master.setChecked(self.config.get("ma_enabled", True))
        self.chk_ma_master.setStyleSheet("font-weight: bold; color: #00E5FF;")
        layout_ma.addWidget(self.chk_ma_master)

        grid_ma = QtWidgets.QGridLayout()
        grid_ma.addWidget(QtWidgets.QLabel("啟用"), 0, 0)
        grid_ma.addWidget(QtWidgets.QLabel("名稱"), 0, 1)
        grid_ma.addWidget(QtWidgets.QLabel("類型 (SMA/EMA)"), 0, 2)
        grid_ma.addWidget(QtWidgets.QLabel("週期 (Period)"), 0, 3)
        grid_ma.addWidget(QtWidgets.QLabel("顏色 (Color)"), 0, 4)
        grid_ma.addWidget(QtWidgets.QLabel("線型 (Line Style)"), 0, 5)

        self.ma_widgets = []
        ma_items = self.config.get("ma_items", DEFAULT_INDICATOR_CONFIG["ma_items"])

        for i in range(7):
            item_cfg = ma_items[i] if i < len(ma_items) else DEFAULT_INDICATOR_CONFIG["ma_items"][i]
            row = i + 1

            chk = QtWidgets.QCheckBox()
            chk.setChecked(item_cfg.get("enabled", True))

            lbl_name = QtWidgets.QLabel(f"MA {i+1}")
            lbl_name.setStyleSheet("font-weight: bold;")

            cbo_type = QtWidgets.QComboBox()
            cbo_type.addItems(["SMA", "EMA"])
            cbo_type.setCurrentText(item_cfg.get("type", "SMA"))

            spn_period = QtWidgets.QSpinBox()
            spn_period.setRange(1, 1000)
            spn_period.setValue(item_cfg.get("period", 5))

            btn_color = ColorButton(item_cfg.get("color", "#FFFFFF"))

            cbo_style = QtWidgets.QComboBox()
            cbo_style.addItems(LINE_STYLE_NAMES)
            cbo_style.setCurrentText(item_cfg.get("style", "實線 (SolidLine)"))

            grid_ma.addWidget(chk, row, 0)
            grid_ma.addWidget(lbl_name, row, 1)
            grid_ma.addWidget(cbo_type, row, 2)
            grid_ma.addWidget(spn_period, row, 3)
            grid_ma.addWidget(btn_color, row, 4)
            grid_ma.addWidget(cbo_style, row, 5)

            self.ma_widgets.append({
                "chk": chk, "type": cbo_type, "period": spn_period,
                "color": btn_color, "style": cbo_style
            })

        layout_ma.addLayout(grid_ma)
        scroll_layout.addWidget(box_ma)

        # 2. 布林通道 Group Box (支援 2 組上下限)
        box_bb = QtWidgets.QGroupBox("2. 布林通道指標 (Bollinger Bands - 雙層上下限)")
        layout_bb = QtWidgets.QVBoxLayout(box_bb)

        self.chk_bb_master = QtWidgets.QCheckBox("顯示布林通道 (Enable Bollinger Bands)")
        self.chk_bb_master.setChecked(self.config.get("bb_enabled", True))
        self.chk_bb_master.setStyleSheet("font-weight: bold; color: #00E5FF;")
        layout_bb.addWidget(self.chk_bb_master)

        grid_bb = QtWidgets.QGridLayout()

        grid_bb.addWidget(QtWidgets.QLabel("通道計算週期:"), 0, 0)
        self.spn_bb_period = QtWidgets.QSpinBox()
        self.spn_bb_period.setRange(2, 500)
        self.spn_bb_period.setValue(self.config.get("bb_period", 20))
        grid_bb.addWidget(self.spn_bb_period, 0, 1)

        grid_bb.addWidget(QtWidgets.QLabel("第一組標準差倍數 (K1):"), 0, 2)
        self.spn_bb_k1 = QtWidgets.QDoubleSpinBox()
        self.spn_bb_k1.setRange(0.1, 10.0)
        self.spn_bb_k1.setSingleStep(0.1)
        self.spn_bb_k1.setValue(self.config.get("bb_k1", 1.0))
        grid_bb.addWidget(self.spn_bb_k1, 0, 3)

        grid_bb.addWidget(QtWidgets.QLabel("第二組標準差倍數 (K2):"), 0, 4)
        self.spn_bb_k2 = QtWidgets.QDoubleSpinBox()
        self.spn_bb_k2.setRange(0.1, 10.0)
        self.spn_bb_k2.setSingleStep(0.1)
        self.spn_bb_k2.setValue(self.config.get("bb_k2", 2.0))
        grid_bb.addWidget(self.spn_bb_k2, 0, 5)

        # 線條樣式設定
        grid_bb.addWidget(QtWidgets.QLabel("中線 (Middle MA):"), 1, 0)
        self.btn_bb_mid_col = ColorButton(self.config.get("bb_mid_color", "#FFD700"))
        self.cbo_bb_mid_sty = QtWidgets.QComboBox()
        self.cbo_bb_mid_sty.addItems(LINE_STYLE_NAMES)
        self.cbo_bb_mid_sty.setCurrentText(self.config.get("bb_mid_style", "實線 (SolidLine)"))
        grid_bb.addWidget(self.btn_bb_mid_col, 1, 1)
        grid_bb.addWidget(self.cbo_bb_mid_sty, 1, 2, 1, 2)

        grid_bb.addWidget(QtWidgets.QLabel("第一層通道 (Upper1/Lower1):"), 2, 0)
        self.btn_bb_b1_col = ColorButton(self.config.get("bb_b1_color", "#00E5FF"))
        self.cbo_bb_b1_sty = QtWidgets.QComboBox()
        self.cbo_bb_b1_sty.addItems(LINE_STYLE_NAMES)
        self.cbo_bb_b1_sty.setCurrentText(self.config.get("bb_b1_style", "虛線 (DashLine)"))
        grid_bb.addWidget(self.btn_bb_b1_col, 2, 1)
        grid_bb.addWidget(self.cbo_bb_b1_sty, 2, 2, 1, 2)

        grid_bb.addWidget(QtWidgets.QLabel("第二層通道 (Upper2/Lower2):"), 3, 0)
        self.btn_bb_b2_col = ColorButton(self.config.get("bb_b2_color", "#E040FB"))
        self.cbo_bb_b2_sty = QtWidgets.QComboBox()
        self.cbo_bb_b2_sty.addItems(LINE_STYLE_NAMES)
        self.cbo_bb_b2_sty.setCurrentText(self.config.get("bb_b2_style", "點劃線 (DashDotLine)"))
        grid_bb.addWidget(self.btn_bb_b2_col, 3, 1)
        grid_bb.addWidget(self.cbo_bb_b2_sty, 3, 2, 1, 2)

        layout_bb.addLayout(grid_bb)
        scroll_layout.addWidget(box_bb)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def _setup_sub_indicators_tab(self, widget: QtWidgets.QWidget):
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        sub_options = [
            "成交量 (Volume)", "MACD", "KDJ", "RSI", "KD", "WR (威廉指標)", "BIAS (乖離率)", "ATR (真實區間)", "DMI (趨向指標)", "CCI (順勢指標)"
        ]

        # 副圖一選擇
        box_sub1 = QtWidgets.QGroupBox("副圖一 (Sub-Chart 1 Indicator)")
        l1 = QtWidgets.QHBoxLayout(box_sub1)
        l1.addWidget(QtWidgets.QLabel("選擇指標:"))
        self.cbo_sub1 = QtWidgets.QComboBox()
        self.cbo_sub1.addItems(sub_options)
        self.cbo_sub1.setCurrentText(self.config.get("sub1_type", "成交量 (Volume)"))
        l1.addWidget(self.cbo_sub1, stretch=1)
        layout.addWidget(box_sub1)

        # 副圖二選擇
        box_sub2 = QtWidgets.QGroupBox("副圖二 (Sub-Chart 2 Indicator)")
        l2 = QtWidgets.QHBoxLayout(box_sub2)
        l2.addWidget(QtWidgets.QLabel("選擇指標:"))
        self.cbo_sub2 = QtWidgets.QComboBox()
        self.cbo_sub2.addItems(sub_options)
        self.cbo_sub2.setCurrentText(self.config.get("sub2_type", "MACD"))
        l2.addWidget(self.cbo_sub2, stretch=1)
        layout.addWidget(box_sub2)

        # 說明提示
        lbl_tip = QtWidgets.QLabel(
            "💡 提示：修改技術指標參數或調色盤顏色後，點擊「套用並儲存設定」即可立即實時更新 K 線圖與資訊列。"
        )
        lbl_tip.setWordWrap(True)
        lbl_tip.setStyleSheet("color: #FFD700; font-size: 12px; background-color: #1E222A; border-radius: 6px; padding: 10px;")
        layout.addWidget(lbl_tip)

        layout.addStretch()

    def _reset_defaults(self):
        reply = QtWidgets.QMessageBox.question(
            self, "確認恢復預設值", "您確定要將所有技術指標與顏色設定恢復為系統預設值嗎？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.config = dict(DEFAULT_INDICATOR_CONFIG)
            self.accept()

    def _save_config(self):
        new_ma_items = []
        for w in self.ma_widgets:
            new_ma_items.append({
                "enabled": w["chk"].isChecked(),
                "type": w["type"].currentText(),
                "period": w["period"].value(),
                "color": w["color"].color(),
                "style": w["style"].currentText()
            })

        self.config["ma_enabled"] = self.chk_ma_master.isChecked()
        self.config["ma_items"] = new_ma_items
        self.config["bb_enabled"] = self.chk_bb_master.isChecked()
        self.config["bb_period"] = self.spn_bb_period.value()
        self.config["bb_k1"] = self.spn_bb_k1.value()
        self.config["bb_k2"] = self.spn_bb_k2.value()
        self.config["bb_mid_color"] = self.btn_bb_mid_col.color()
        self.config["bb_mid_style"] = self.cbo_bb_mid_sty.currentText()
        self.config["bb_b1_color"] = self.btn_bb_b1_col.color()
        self.config["bb_b1_style"] = self.cbo_bb_b1_sty.currentText()
        self.config["bb_b2_color"] = self.btn_bb_b2_col.color()
        self.config["bb_b2_style"] = self.cbo_bb_b2_sty.currentText()
        self.config["sub1_type"] = self.cbo_sub1.currentText()
        self.config["sub2_type"] = self.cbo_sub2.currentText()

        self.config_saved_signal.emit(self.config)
        self.accept()
