import os
import json
import logging
try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets

if not hasattr(QtCore, 'Signal'):
    QtCore.Signal = getattr(QtCore, 'pyqtSignal', None)
if not hasattr(QtCore, 'Slot'):
    QtCore.Slot = getattr(QtCore, 'pyqtSlot', None)
from typing import Dict, Any

CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "config", "indicator_config.json")

QtPenStyle = getattr(QtCore.Qt, 'PenStyle', QtCore.Qt)
LINE_STYLES = {
    "實線 (SolidLine)": getattr(QtPenStyle, 'SolidLine', None),
    "虛線 (DashLine)": getattr(QtPenStyle, 'DashLine', None),
    "點線 (DotLine)": getattr(QtPenStyle, 'DotLine', None),
    "點劃線 (DashDotLine)": getattr(QtPenStyle, 'DashDotLine', None)
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
    # 布林通道 第一層與第二層獨立啟用 CheckBox
    "bb_b1_enabled": True,
    "bb_b2_enabled": True,
    # 布林通道 4 條獨立倍數設定 (Upper1, Lower1, Upper2, Lower2)
    "bb_u1_k": 1.0,
    "bb_l1_k": 1.0,
    "bb_u2_k": 2.0,
    "bb_l2_k": 2.0,
    "bb_mid_color": "#FFD700",
    "bb_mid_style": "實線 (SolidLine)",
    "bb_b1_color": "#00E5FF",
    "bb_b1_style": "虛線 (DashLine)",
    "bb_b2_color": "#E040FB",
    "bb_b2_style": "點劃線 (DashDotLine)",
    # 副圖一預設永遠為成交量 (Volume)
    "sub1_type": "成交量 (Volume)",
    "sub2_type": "MACD",
    # 副圖技術指標自訂參數
    "macd_fast": 12, "macd_slow": 26, "macd_signal": 9,
    "kdj_n": 9, "kdj_m1": 3, "kdj_m2": 3,
    "rsi_p1": 6, "rsi_p2": 12, "rsi_p3": 24,
    "vma_p1": 5, "vma_p2": 10,
    "wr_p": 14,
    "bias_p1": 6, "bias_p2": 12, "bias_p3": 24,
    "atr_p": 14,
    "cci_p": 14
}

def load_indicator_config_from_json() -> Dict[str, Any]:
    """從 config/indicator_config.json 讀取持久化設定檔，無檔案則回傳預設值"""
    config = dict(DEFAULT_INDICATOR_CONFIG)
    try:
        if os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                config.update(saved)
                logging.info(f"Loaded indicator config from {CONFIG_FILE_PATH}")
    except Exception as e:
        logging.warning(f"Failed to load indicator config: {e}")
    return config

def save_indicator_config_to_json(config: Dict[str, Any]):
    """將技術指標設定持久化寫入 config/indicator_config.json"""
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)
        with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        logging.info(f"Saved indicator config to {CONFIG_FILE_PATH}")
    except Exception as e:
        logging.error(f"Failed to save indicator config: {e}")

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
        bg = QtGui.QColor(self._color)
        # 貫徹鐵律：淺色背景字體一律強制純黑 #000000
        text_col = "#000000" if (bg.red()*0.299 + bg.green()*0.587 + bg.blue()*0.114) > 150 else "#FFFFFF"
        self.setStyleSheet(f"background-color: {self._color}; color: {text_col}; font-weight: bold; border-radius: 4px; padding: 4px 10px; border: 1px solid #555555;")

    def _choose_color(self):
        col = QtWidgets.QColorDialog.getColor(QtGui.QColor(self._color), self, "選擇指標線型顏色")
        if col.isValid():
            self._color = col.name().upper()
            self._update_style()
            self.color_changed.emit(self._color)

class IndicatorSettingsDialog(QtWidgets.QDialog):
    """技術指標詳細設定視窗 (支援 7 組均線 SMA/EMA、布林第一層第二層獨立啟用、獨立 4 上下限倍數與持久化)"""
    config_saved_signal = QtCore.Signal(dict)

    def __init__(self, current_config: Dict[str, Any] = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ 技術指標詳細設定與顏色調色盤 (Indicator Settings v1.0.41)")
        self.resize(880, 750)
        self.config = load_indicator_config_from_json()
        if current_config:
            self.config.update(current_config)

        self._setup_dialog_qss()
        self._init_ui()

    def _setup_dialog_qss(self):
        """套用高科技極致暗黑 QSS 主題 (貫徹淺底純黑字高對比鐵律)"""
        qss = """
        QDialog {
            background-color: #121418;
            color: #FFFFFF;
            font-family: "Microsoft JhengHei", "Segoe UI", sans-serif;
            font-size: 13px;
        }
        QTabWidget::pane {
            border: 1px solid #2C323F;
            background-color: #16191E;
            border-radius: 6px;
        }
        QTabBar::tab {
            background-color: #1E222A;
            color: #8C9BAE;
            padding: 10px 22px;
            margin-right: 4px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            font-weight: bold;
        }
        QTabBar::tab:selected {
            background-color: #0066FF;
            color: #FFFFFF;
        }
        QGroupBox {
            border: 1px solid #2C323F;
            border-radius: 8px;
            margin-top: 14px;
            font-weight: bold;
            color: #00E5FF;
            background-color: #16191E;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 6px;
            background-color: #16191E;
        }
        QLabel {
            color: #E0E6ED;
        }
        QCheckBox {
            color: #FFFFFF;
            font-weight: bold;
        }
        QSpinBox, QDoubleSpinBox {
            background-color: #1E222A;
            color: #00E5FF;
            border: 1px solid #2C323F;
            border-radius: 4px;
            padding: 4px 8px;
            font-weight: bold;
        }
        QComboBox {
            background-color: #1E222A;
            color: #FFFFFF;
            border: 1px solid #2C323F;
            border-radius: 4px;
            padding: 4px 8px;
            font-weight: bold;
        }
        QComboBox QAbstractItemView {
            background-color: #16191E;
            color: #FFFFFF;
            selection-background-color: #0066FF;
            selection-color: #FFFFFF;
        }
        QScrollArea {
            border: none;
            background-color: #121418;
        }
        """
        self.setStyleSheet(qss)

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Tab Widget
        self.tabs = QtWidgets.QTabWidget()
        
        # Tab 1: 主圖指標設定
        tab_main = QtWidgets.QWidget()
        self._setup_main_indicators_tab(tab_main)
        self.tabs.addTab(tab_main, "📈 主圖指標設定 (7組均線 / 布林第一層與第二層獨立啟用)")

        # Tab 2: 副圖指標設定
        tab_sub = QtWidgets.QWidget()
        self._setup_sub_indicators_tab(tab_sub)
        self.tabs.addTab(tab_sub, "📊 副圖指標設定 (自訂參數與類別)")

        layout.addWidget(self.tabs)

        # 底部控制按鈕
        btn_box = QtWidgets.QHBoxLayout()
        btn_reset = QtWidgets.QPushButton("🔄 恢復預設值")
        btn_reset.setStyleSheet("background-color: #37474F; color: #FFFFFF; font-weight: bold; padding: 8px 16px; border-radius: 6px;")
        btn_reset.clicked.connect(self._reset_defaults)

        btn_cancel = QtWidgets.QPushButton("❌ 取消")
        btn_cancel.setStyleSheet("background-color: #263238; color: #FFFFFF; font-weight: bold; padding: 8px 16px; border-radius: 6px;")
        btn_cancel.clicked.connect(self.reject)

        btn_save = QtWidgets.QPushButton("💾 套用並永久儲存設定")
        btn_save.setStyleSheet("background-color: #0066FF; color: #FFFFFF; font-weight: bold; padding: 8px 20px; border-radius: 6px;")
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

        # 1. 均線設定 Group Box
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
            lbl_name.setStyleSheet("font-weight: bold; color: #00E5FF;")

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

        # 2. 布林通道 Group Box (支援第一層與第二層獨立啟用 Checkbox)
        box_bb = QtWidgets.QGroupBox("2. 布林通道指標 (Bollinger Bands - 支援第一層與第二層獨立勾選啟用)")
        layout_bb = QtWidgets.QVBoxLayout(box_bb)

        self.chk_bb_master = QtWidgets.QCheckBox("顯示布林通道主開關 (Enable Bollinger Bands)")
        self.chk_bb_master.setChecked(self.config.get("bb_enabled", True))
        self.chk_bb_master.setStyleSheet("font-weight: bold; color: #00E5FF;")
        layout_bb.addWidget(self.chk_bb_master)

        grid_bb = QtWidgets.QGridLayout()

        grid_bb.addWidget(QtWidgets.QLabel("通道計算週期:"), 0, 0)
        self.spn_bb_period = QtWidgets.QSpinBox()
        self.spn_bb_period.setRange(2, 500)
        self.spn_bb_period.setValue(self.config.get("bb_period", 20))
        grid_bb.addWidget(self.spn_bb_period, 0, 1)

        # 第一層獨立啟用與獨立倍數
        self.chk_bb_b1 = QtWidgets.QCheckBox("啟用第一層通道 (Upper1/Lower1)")
        self.chk_bb_b1.setChecked(self.config.get("bb_b1_enabled", True))
        self.chk_bb_b1.setStyleSheet("font-weight: bold; color: #00E5FF;")
        grid_bb.addWidget(self.chk_bb_b1, 1, 0, 1, 2)

        grid_bb.addWidget(QtWidgets.QLabel("第一層上限倍數 (Upper 1 K):"), 2, 0)
        self.spn_bb_u1_k = QtWidgets.QDoubleSpinBox()
        self.spn_bb_u1_k.setRange(0.1, 10.0)
        self.spn_bb_u1_k.setSingleStep(0.1)
        self.spn_bb_u1_k.setValue(self.config.get("bb_u1_k", 1.0))
        grid_bb.addWidget(self.spn_bb_u1_k, 2, 1)

        grid_bb.addWidget(QtWidgets.QLabel("第一層下限倍數 (Lower 1 K):"), 2, 2)
        self.spn_bb_l1_k = QtWidgets.QDoubleSpinBox()
        self.spn_bb_l1_k.setRange(0.1, 10.0)
        self.spn_bb_l1_k.setSingleStep(0.1)
        self.spn_bb_l1_k.setValue(self.config.get("bb_l1_k", 1.0))
        grid_bb.addWidget(self.spn_bb_l1_k, 2, 3)

        # 第二層獨立啟用與獨立倍數
        self.chk_bb_b2 = QtWidgets.QCheckBox("啟用第二層通道 (Upper2/Lower2)")
        self.chk_bb_b2.setChecked(self.config.get("bb_b2_enabled", True))
        self.chk_bb_b2.setStyleSheet("font-weight: bold; color: #E040FB;")
        grid_bb.addWidget(self.chk_bb_b2, 3, 0, 1, 2)

        grid_bb.addWidget(QtWidgets.QLabel("第二層上限倍數 (Upper 2 K):"), 4, 0)
        self.spn_bb_u2_k = QtWidgets.QDoubleSpinBox()
        self.spn_bb_u2_k.setRange(0.1, 10.0)
        self.spn_bb_u2_k.setSingleStep(0.1)
        self.spn_bb_u2_k.setValue(self.config.get("bb_u2_k", 2.0))
        grid_bb.addWidget(self.spn_bb_u2_k, 4, 1)

        grid_bb.addWidget(QtWidgets.QLabel("第二層下限倍數 (Lower 2 K):"), 4, 2)
        self.spn_bb_l2_k = QtWidgets.QDoubleSpinBox()
        self.spn_bb_l2_k.setRange(0.1, 10.0)
        self.spn_bb_l2_k.setSingleStep(0.1)
        self.spn_bb_l2_k.setValue(self.config.get("bb_l2_k", 2.0))
        grid_bb.addWidget(self.spn_bb_l2_k, 4, 3)

        # 線條色彩與線型
        grid_bb.addWidget(QtWidgets.QLabel("中線 (Middle MA):"), 5, 0)
        self.btn_bb_mid_col = ColorButton(self.config.get("bb_mid_color", "#FFD700"))
        self.cbo_bb_mid_sty = QtWidgets.QComboBox()
        self.cbo_bb_mid_sty.addItems(LINE_STYLE_NAMES)
        self.cbo_bb_mid_sty.setCurrentText(self.config.get("bb_mid_style", "實線 (SolidLine)"))
        grid_bb.addWidget(self.btn_bb_mid_col, 5, 1)
        grid_bb.addWidget(self.cbo_bb_mid_sty, 5, 2, 1, 2)

        grid_bb.addWidget(QtWidgets.QLabel("第一層通道 (Upper1/Lower1):"), 6, 0)
        self.btn_bb_b1_col = ColorButton(self.config.get("bb_b1_color", "#00E5FF"))
        self.cbo_bb_b1_sty = QtWidgets.QComboBox()
        self.cbo_bb_b1_sty.addItems(LINE_STYLE_NAMES)
        self.cbo_bb_b1_sty.setCurrentText(self.config.get("bb_b1_style", "虛線 (DashLine)"))
        grid_bb.addWidget(self.btn_bb_b1_col, 6, 1)
        grid_bb.addWidget(self.cbo_bb_b1_sty, 6, 2, 1, 2)

        grid_bb.addWidget(QtWidgets.QLabel("第二層通道 (Upper2/Lower2):"), 7, 0)
        self.btn_bb_b2_col = ColorButton(self.config.get("bb_b2_color", "#E040FB"))
        self.cbo_bb_b2_sty = QtWidgets.QComboBox()
        self.cbo_bb_b2_sty.addItems(LINE_STYLE_NAMES)
        self.cbo_bb_b2_sty.setCurrentText(self.config.get("bb_b2_style", "點劃線 (DashDotLine)"))
        grid_bb.addWidget(self.btn_bb_b2_col, 7, 1)
        grid_bb.addWidget(self.cbo_bb_b2_sty, 7, 2, 1, 2)

        layout_bb.addLayout(grid_bb)
        scroll_layout.addWidget(box_bb)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def _setup_sub_indicators_tab(self, widget: QtWidgets.QWidget):
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(12)

        sub_options = [
            "成交量 (Volume)", "MACD", "KDJ", "RSI", "KD", "WR (威廉指標)", "BIAS (乖離率)", "ATR (真實區間)", "DMI (趨向指標)", "CCI (順勢指標)"
        ]

        # 1. 副圖選擇 Group Box
        box_sub_sel = QtWidgets.QGroupBox("1. 副圖指標類別選擇 (副圖一預設固定為成交量)")
        g1 = QtWidgets.QGridLayout(box_sub_sel)
        
        g1.addWidget(QtWidgets.QLabel("副圖一 (Upper Sub-Chart):"), 0, 0)
        self.cbo_sub1 = QtWidgets.QComboBox()
        self.cbo_sub1.addItems(sub_options)
        self.cbo_sub1.setCurrentText(self.config.get("sub1_type", "成交量 (Volume)"))
        g1.addWidget(self.cbo_sub1, 0, 1)

        g1.addWidget(QtWidgets.QLabel("副圖二 (Lower Sub-Chart):"), 1, 0)
        self.cbo_sub2 = QtWidgets.QComboBox()
        self.cbo_sub2.addItems(sub_options)
        self.cbo_sub2.setCurrentText(self.config.get("sub2_type", "MACD"))
        g1.addWidget(self.cbo_sub2, 1, 1)

        scroll_layout.addWidget(box_sub_sel)

        # 2. 副圖技術指標自訂參數 Group Box
        box_params = QtWidgets.QGroupBox("2. 副圖技術指標自訂參數 (Custom Indicator Parameters)")
        g2 = QtWidgets.QGridLayout(box_params)

        # MACD 參數
        g2.addWidget(QtWidgets.QLabel("MACD 快線 (EMA Fast):"), 0, 0)
        self.spn_macd_fast = QtWidgets.QSpinBox()
        self.spn_macd_fast.setRange(2, 200)
        self.spn_macd_fast.setValue(self.config.get("macd_fast", 12))
        g2.addWidget(self.spn_macd_fast, 0, 1)

        g2.addWidget(QtWidgets.QLabel("MACD 慢線 (EMA Slow):"), 0, 2)
        self.spn_macd_slow = QtWidgets.QSpinBox()
        self.spn_macd_slow.setRange(2, 200)
        self.spn_macd_slow.setValue(self.config.get("macd_slow", 26))
        g2.addWidget(self.spn_macd_slow, 0, 3)

        g2.addWidget(QtWidgets.QLabel("MACD 訊號線 (Signal):"), 0, 4)
        self.spn_macd_sig = QtWidgets.QSpinBox()
        self.spn_macd_sig.setRange(2, 200)
        self.spn_macd_sig.setValue(self.config.get("macd_signal", 9))
        g2.addWidget(self.spn_macd_sig, 0, 5)

        # KDJ / KD 參數
        g2.addWidget(QtWidgets.QLabel("KDJ 週期 (N):"), 1, 0)
        self.spn_kdj_n = QtWidgets.QSpinBox()
        self.spn_kdj_n.setRange(2, 200)
        self.spn_kdj_n.setValue(self.config.get("kdj_n", 9))
        g2.addWidget(self.spn_kdj_n, 1, 1)

        g2.addWidget(QtWidgets.QLabel("KDJ 平滑1 (M1):"), 1, 2)
        self.spn_kdj_m1 = QtWidgets.QSpinBox()
        self.spn_kdj_m1.setRange(1, 100)
        self.spn_kdj_m1.setValue(self.config.get("kdj_m1", 3))
        g2.addWidget(self.spn_kdj_m1, 1, 3)

        g2.addWidget(QtWidgets.QLabel("KDJ 平滑2 (M2):"), 1, 4)
        self.spn_kdj_m2 = QtWidgets.QSpinBox()
        self.spn_kdj_m2.setRange(1, 100)
        self.spn_kdj_m2.setValue(self.config.get("kdj_m2", 3))
        g2.addWidget(self.spn_kdj_m2, 1, 5)

        # RSI 參數
        g2.addWidget(QtWidgets.QLabel("RSI 週期 1:"), 2, 0)
        self.spn_rsi_p1 = QtWidgets.QSpinBox()
        self.spn_rsi_p1.setRange(2, 200)
        self.spn_rsi_p1.setValue(self.config.get("rsi_p1", 6))
        g2.addWidget(self.spn_rsi_p1, 2, 1)

        g2.addWidget(QtWidgets.QLabel("RSI 週期 2:"), 2, 2)
        self.spn_rsi_p2 = QtWidgets.QSpinBox()
        self.spn_rsi_p2.setRange(2, 200)
        self.spn_rsi_p2.setValue(self.config.get("rsi_p2", 12))
        g2.addWidget(self.spn_rsi_p2, 2, 3)

        g2.addWidget(QtWidgets.QLabel("RSI 週期 3:"), 2, 4)
        self.spn_rsi_p3 = QtWidgets.QSpinBox()
        self.spn_rsi_p3.setRange(2, 200)
        self.spn_rsi_p3.setValue(self.config.get("rsi_p3", 24))
        g2.addWidget(self.spn_rsi_p3, 2, 5)

        # Volume MA 參數
        g2.addWidget(QtWidgets.QLabel("量均線 VMA1:"), 3, 0)
        self.spn_vma_p1 = QtWidgets.QSpinBox()
        self.spn_vma_p1.setRange(1, 200)
        self.spn_vma_p1.setValue(self.config.get("vma_p1", 5))
        g2.addWidget(self.spn_vma_p1, 3, 1)

        g2.addWidget(QtWidgets.QLabel("量均線 VMA2:"), 3, 2)
        self.spn_vma_p2 = QtWidgets.QSpinBox()
        self.spn_vma_p2.setRange(1, 200)
        self.spn_vma_p2.setValue(self.config.get("vma_p2", 10))
        g2.addWidget(self.spn_vma_p2, 3, 3)

        # WR & ATR & CCI 參數
        g2.addWidget(QtWidgets.QLabel("威廉 WR 週期:"), 4, 0)
        self.spn_wr_p = QtWidgets.QSpinBox()
        self.spn_wr_p.setRange(2, 200)
        self.spn_wr_p.setValue(self.config.get("wr_p", 14))
        g2.addWidget(self.spn_wr_p, 4, 1)

        g2.addWidget(QtWidgets.QLabel("ATR 週期:"), 4, 2)
        self.spn_atr_p = QtWidgets.QSpinBox()
        self.spn_atr_p.setRange(2, 200)
        self.spn_atr_p.setValue(self.config.get("atr_p", 14))
        g2.addWidget(self.spn_atr_p, 4, 3)

        g2.addWidget(QtWidgets.QLabel("CCI 週期:"), 4, 4)
        self.spn_cci_p = QtWidgets.QSpinBox()
        self.spn_cci_p.setRange(2, 200)
        self.spn_cci_p.setValue(self.config.get("cci_p", 14))
        g2.addWidget(self.spn_cci_p, 4, 5)

        scroll_layout.addWidget(box_params)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def _reset_defaults(self):
        reply = QtWidgets.QMessageBox.question(
            self, "確認恢復預設值", "您確定要將所有技術指標與顏色設定恢復為系統預設值嗎？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.config = dict(DEFAULT_INDICATOR_CONFIG)
            save_indicator_config_to_json(self.config)
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

        # 布林通道 第一層與第二層獨立啟用與獨立倍數
        self.config["bb_b1_enabled"] = self.chk_bb_b1.isChecked()
        self.config["bb_b2_enabled"] = self.chk_bb_b2.isChecked()
        self.config["bb_u1_k"] = self.spn_bb_u1_k.value()
        self.config["bb_l1_k"] = self.spn_bb_l1_k.value()
        self.config["bb_u2_k"] = self.spn_bb_u2_k.value()
        self.config["bb_l2_k"] = self.spn_bb_l2_k.value()

        self.config["bb_mid_color"] = self.btn_bb_mid_col.color()
        self.config["bb_mid_style"] = self.cbo_bb_mid_sty.currentText()
        self.config["bb_b1_color"] = self.btn_bb_b1_col.color()
        self.config["bb_b1_style"] = self.cbo_bb_b1_sty.currentText()
        self.config["bb_b2_color"] = self.btn_bb_b2_col.color()
        self.config["bb_b2_style"] = self.cbo_bb_b2_sty.currentText()
        self.config["sub1_type"] = self.cbo_sub1.currentText()
        self.config["sub2_type"] = self.cbo_sub2.currentText()

        # 儲存副圖指標自訂參數
        self.config["macd_fast"] = self.spn_macd_fast.value()
        self.config["macd_slow"] = self.spn_macd_slow.value()
        self.config["macd_signal"] = self.spn_macd_sig.value()
        self.config["kdj_n"] = self.spn_kdj_n.value()
        self.config["kdj_m1"] = self.spn_kdj_m1.value()
        self.config["kdj_m2"] = self.spn_kdj_m2.value()
        self.config["rsi_p1"] = self.spn_rsi_p1.value()
        self.config["rsi_p2"] = self.spn_rsi_p2.value()
        self.config["rsi_p3"] = self.spn_rsi_p3.value()
        self.config["vma_p1"] = self.spn_vma_p1.value()
        self.config["vma_p2"] = self.spn_vma_p2.value()
        self.config["wr_p"] = self.spn_wr_p.value()
        self.config["atr_p"] = self.spn_atr_p.value()
        self.config["cci_p"] = self.spn_cci_p.value()

        # 永久自動寫入 config/indicator_config.json
        save_indicator_config_to_json(self.config)

        self.config_saved_signal.emit(self.config)
        self.accept()
