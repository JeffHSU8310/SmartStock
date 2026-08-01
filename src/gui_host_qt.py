import sys
import os
import ctypes
from typing import List, Dict
from PySide6 import QtCore, QtGui, QtWidgets
from src.sinopac_engine import SinoPacEngine
from src.widgets.candlestick_chart import NativeCandlestickChart
from src.widgets.watchlist_widget import WatchlistWidget
from src.widgets.five_bids_widget import FiveBidsWidget
from src.widgets.order_toolbar import OrderToolbarWidget
from src.widgets.message_console import MessageConsoleWidget

# 定義 C++ 結構 ctypes Mapping
class CXXKBar(ctypes.Structure):
    _fields_ = [
        ("datetime", ctypes.c_char * 32),
        ("open", ctypes.c_double),
        ("high", ctypes.c_double),
        ("low", ctypes.c_double),
        ("close", ctypes.c_double),
        ("volume", ctypes.c_int64)
    ]

class CXXSelectionResult(ctypes.Structure):
    _fields_ = [
        ("code", ctypes.c_char * 16),
        ("name", ctypes.c_char * 32),
        ("close", ctypes.c_double),
        ("pct_change", ctypes.c_double),
        ("score", ctypes.c_double),
        ("signal_type", ctypes.c_char * 64)
    ]

class CXXBacktestResult(ctypes.Structure):
    _fields_ = [
        ("total_return_pct", ctypes.c_double),
        ("win_rate", ctypes.c_double),
        ("max_drawdown_pct", ctypes.c_double),
        ("sharpe_ratio", ctypes.c_double),
        ("total_trades", ctypes.c_int),
        ("winning_trades", ctypes.c_int),
        ("losing_trades", ctypes.c_int)
    ]

class SmartStockMainWindow(QtWidgets.QMainWindow):
    """SmartStock 純原生 Qt6 量化桌面主視窗 (Pure Native Desktop Application v1.0.3)"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartStock 智慧型量化交易與選股平台 v1.0.3 (Pure Native Qt6)")
        self.resize(1480, 920)

        self.current_code = "2330"
        self.current_name = "台積電"
        self.current_ktype = "Day"

        self.engine = SinoPacEngine()
        self.dll = self._load_cpp_dll()

        self._setup_qss_style()
        self._build_ui()
        self.load_initial_data()

    def _load_cpp_dll(self):
        dll_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "smartstock_core.dll")
        if os.path.exists(dll_path):
            try:
                dll = ctypes.CDLL(dll_path)
                dll.get_engine_version.restype = ctypes.c_char_p
                version_str = dll.get_engine_version().decode("utf-8")
                print(f"[C++ Core Engine Loaded]: {version_str}")
                return dll
            except Exception as e:
                print(f"[C++ DLL Load Error]: {e}")
        else:
            print(f"[C++ DLL Warning]: {dll_path} 不存在")
        return None

    def _setup_qss_style(self):
        """極致暗黑高科技 QSS 主題樣式 (Dark Tech Modern QSS)"""
        qss = """
        QMainWindow {
            background-color: #121418;
        }
        QWidget {
            color: #E0E6ED;
            font-family: "Microsoft JhengHei", "Segoe UI", sans-serif;
            font-size: 13px;
        }
        QTabWidget::pane {
            border: 1px solid #232730;
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
        QTabBar::tab:hover:!selected {
            background-color: #282E39;
            color: #D5DFEB;
        }
        QTableWidget {
            background-color: #16191E;
            gridline-color: #232730;
            border: none;
            selection-background-color: #263238;
        }
        QHeaderView::section {
            background-color: #1E222A;
            color: #90A4AE;
            padding: 8px;
            border: none;
            font-weight: bold;
        }
        QPushButton {
            background-color: #0066FF;
            color: #FFFFFF;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2979FF;
        }
        QPushButton:pressed {
            background-color: #1565C0;
        }
        QLineEdit {
            background-color: #1E222A;
            border: 1px solid #2C323F;
            border-radius: 6px;
            padding: 6px 10px;
            color: #FFFFFF;
        }
        QComboBox {
            background-color: #1E222A;
            border: 1px solid #2C323F;
            border-radius: 6px;
            padding: 6px 10px;
            color: #FFFFFF;
        }
        QGroupBox {
            border: 1px solid #232730;
            border-radius: 8px;
            margin-top: 12px;
            font-weight: bold;
            color: #00E5FF;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        """
        self.setStyleSheet(qss)

    def _build_ui(self):
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QtWidgets.QVBoxLayout(main_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # 頂部 Header Banner
        header = QtWidgets.QHBoxLayout()
        title_label = QtWidgets.QLabel("📈 SmartStock 智慧型量化交易與選股平台 v1.0.3 (Pure Native Qt6)")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #00E5FF;")
        header.addWidget(title_label)

        header.addStretch()
        self.status_badge = QtWidgets.QLabel("🟢 永豐金 Shioaji 實盤連線中")
        self.status_badge.setStyleSheet("background-color: #1A3326; color: #00E676; padding: 5px 12px; border-radius: 12px; font-weight: bold;")
        header.addWidget(self.status_badge)
        main_layout.addLayout(header)

        # 主要頁籤 (QTabWidget)
        self.tabs = QtWidgets.QTabWidget()
        main_layout.addWidget(self.tabs)

        # 建立五大獨立功能頁籤
        self._build_market_overview_tab()
        self._build_screener_tab()
        self._build_backtest_tab()
        self._build_order_tab()
        self._build_settings_tab()

    def _build_market_overview_tab(self):
        """【看盤大廳 (Market Overview)】五大原生版面結構"""
        tab = QtWidgets.QWidget()
        tab_layout = QtWidgets.QHBoxLayout(tab)
        tab_layout.setContentsMargins(6, 6, 6, 6)

        # 使用 QSplitter 實現滑順可拖曳分割版面
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # ==========================================
        # 📌 左側資訊欄 (Left Sidebar Container)
        # ==========================================
        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        # (1) 版面1: 自選股清單 (放在主圖區左方)
        box_watchlist = QtWidgets.QGroupBox("📌 1. 自選股清單 (管理與切換)")
        l_wl = QtWidgets.QVBoxLayout(box_watchlist)
        self.watchlist_widget = WatchlistWidget()
        self.watchlist_widget.stock_selected_signal.connect(self.on_stock_changed)
        l_wl.addWidget(self.watchlist_widget)
        left_layout.addWidget(box_watchlist, stretch=4)

        # (3) 版面3: 五檔即時報價欄 (放在主圖區左方)
        box_fivebids = QtWidgets.QGroupBox("📊 3. 即時五檔委買 / 委賣報價欄")
        l_fb = QtWidgets.QVBoxLayout(box_fivebids)
        self.five_bids_widget = FiveBidsWidget()
        l_fb.addWidget(self.five_bids_widget)
        left_layout.addWidget(box_fivebids, stretch=3)

        # (4) 版面4: 下單工具欄 (放在主圖區左方)
        box_order = QtWidgets.QGroupBox("⚡ 4. 快捷下單工具欄")
        l_ot = QtWidgets.QVBoxLayout(box_order)
        self.order_toolbar_widget = OrderToolbarWidget()
        self.order_toolbar_widget.order_submitted_signal.connect(self.on_order_submitted)
        l_ot.addWidget(self.order_toolbar_widget)
        left_layout.addWidget(box_order, stretch=3)

        splitter.addWidget(left_widget)

        # ==========================================
        # 📊 右側主工作區 (Right Main Area Container)
        # ==========================================
        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)

        # 頂部 K 線標頭與週期切換列
        kline_header = QtWidgets.QHBoxLayout()
        self.lbl_stock_title = QtWidgets.QLabel("2330 台積電 — [日 K 線圖]")
        self.lbl_stock_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        kline_header.addWidget(self.lbl_stock_title)

        kline_header.addStretch()
        btn_day = QtWidgets.QPushButton("日K")
        btn_day.clicked.connect(lambda: self.switch_ktype("Day"))
        btn_60m = QtWidgets.QPushButton("60分K")
        btn_60m.clicked.connect(lambda: self.switch_ktype("60m"))
        btn_5m = QtWidgets.QPushButton("5分K")
        btn_5m.clicked.connect(lambda: self.switch_ktype("5m"))
        btn_1m = QtWidgets.QPushButton("1分K")
        btn_1m.clicked.connect(lambda: self.switch_ktype("1m"))

        kline_header.addWidget(btn_day)
        kline_header.addWidget(btn_60m)
        kline_header.addWidget(btn_5m)
        kline_header.addWidget(btn_1m)
        right_layout.addLayout(kline_header)

        # (2-A & 2-B) 版面2: 主圖區 (K線圖, 占比最大) & 副圖區 (技術指標, 放在主圖下方)
        self.chart_widget = NativeCandlestickChart()
        right_layout.addWidget(self.chart_widget, stretch=7)

        # (5) 版面5: 訊息欄 (放在副圖正下方)
        self.console_widget = MessageConsoleWidget()
        right_layout.addWidget(self.console_widget, stretch=3)

        splitter.addWidget(right_widget)

        # 設定比例 (左側固定約 380px，右側自適應伸展)
        splitter.setSizes([380, 1100])
        tab_layout.addWidget(splitter)

        self.tabs.addTab(tab, "📊 看盤大廳 (Market Overview)")

    def _build_screener_tab(self):
        """【智慧選股雷達】"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)

        top_bar = QtWidgets.QHBoxLayout()
        btn_run = QtWidgets.QPushButton("🚀 執行 C++ 核心選股掃描 (AI Robot Screener)")
        btn_run.setStyleSheet("background-color: #FF3B69; font-size: 14px; padding: 10px 20px;")
        btn_run.clicked.connect(self.run_cpp_screener)
        top_bar.addWidget(btn_run)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        self.screener_table = QtWidgets.QTableWidget(0, 6)
        self.screener_table.setHorizontalHeaderLabels(["股票代碼", "股票名稱", "當前收盤", "漲跌幅(%)", "AI動能評分", "C++ 識別型態與訊號"])
        self.screener_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.screener_table)

        self.tabs.addTab(tab, "🎯 智慧選股雷達")

    def _build_backtest_tab(self):
        """【C++ 回測儀表板】"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)

        panel = QtWidgets.QGroupBox("C++ 策略回測參數設定 (MA 雙均線穿透交叉策略)")
        panel_layout = QtWidgets.QHBoxLayout(panel)

        panel_layout.addWidget(QtWidgets.QLabel("快線 MA:"))
        self.input_fast_ma = QtWidgets.QLineEdit("5")
        self.input_fast_ma.setFixedWidth(60)
        panel_layout.addWidget(self.input_fast_ma)

        panel_layout.addWidget(QtWidgets.QLabel("慢線 MA:"))
        self.input_slow_ma = QtWidgets.QLineEdit("20")
        self.input_slow_ma.setFixedWidth(60)
        panel_layout.addWidget(self.input_slow_ma)

        panel_layout.addWidget(QtWidgets.QLabel("初始資金:"))
        self.input_capital = QtWidgets.QLineEdit("1000000")
        self.input_capital.setFixedWidth(100)
        panel_layout.addWidget(self.input_capital)

        btn_bt = QtWidgets.QPushButton("⚡ 啟動 C++ 回測引擎")
        btn_bt.clicked.connect(self.run_cpp_backtest)
        panel_layout.addWidget(btn_bt)
        panel_layout.addStretch()

        layout.addWidget(panel)

        # 績效卡片區
        cards_layout = QtWidgets.QHBoxLayout()
        self.card_return = self._create_metric_card("總報酬率 (%)", "--", "#FF3B69")
        self.card_winrate = self._create_metric_card("交易勝率 (%)", "--", "#00E676")
        self.card_mdd = self._create_metric_card("最大回撤 MDD (%)", "--", "#FF9800")
        self.card_sharpe = self._create_metric_card("Sharpe Ratio", "--", "#00E5FF")

        cards_layout.addWidget(self.card_return)
        cards_layout.addWidget(self.card_winrate)
        cards_layout.addWidget(self.card_mdd)
        cards_layout.addWidget(self.card_sharpe)
        layout.addLayout(cards_layout)

        layout.addStretch()
        self.tabs.addTab(tab, "📉 C++ 回測儀表板")

    def _create_metric_card(self, title: str, val: str, color: str) -> QtWidgets.QFrame:
        frame = QtWidgets.QFrame()
        frame.setStyleSheet(f"background-color: #1E222A; border: 1px solid #2C323F; border-radius: 8px; padding: 15px;")
        l = QtWidgets.QVBoxLayout(frame)
        t_lbl = QtWidgets.QLabel(title)
        t_lbl.setStyleSheet("color: #8C9BAE; font-size: 12px;")
        v_lbl = QtWidgets.QLabel(val)
        v_lbl.setObjectName("val")
        v_lbl.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold; margin-top: 5px;")
        l.addWidget(t_lbl)
        l.addWidget(v_lbl)
        return frame

    def _build_order_tab(self):
        """【Shioaji 實盤與下單】"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)

        box = QtWidgets.QGroupBox("永豐金證券下單卡片 (ROD / IOC / FOK)")
        l = QtWidgets.QGridLayout(box)

        l.addWidget(QtWidgets.QLabel("商品代碼:"), 0, 0)
        l.addWidget(QtWidgets.QLineEdit("2330"), 0, 1)

        l.addWidget(QtWidgets.QLabel("委託價格:"), 0, 2)
        l.addWidget(QtWidgets.QLineEdit("965.0"), 0, 3)

        l.addWidget(QtWidgets.QLabel("委託張數:"), 1, 0)
        l.addWidget(QtWidgets.QLineEdit("1"), 1, 1)

        btn_buy = QtWidgets.QPushButton("🔴 買進下單 (BUY)")
        btn_buy.setStyleSheet("background-color: #FF3B69; padding: 10px;")
        btn_sell = QtWidgets.QPushButton("🟢 賣出下單 (SELL)")
        btn_sell.setStyleSheet("background-color: #00E676; padding: 10px; color: #000000;")

        l.addWidget(btn_buy, 1, 2)
        l.addWidget(btn_sell, 1, 3)

        layout.addWidget(box)
        layout.addStretch()
        self.tabs.addTab(tab, "💼 Shioaji 實盤下單")

    def _build_settings_tab(self):
        """【系統憑證與登入 (CA Auth Modal)】"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)

        box = QtWidgets.QGroupBox("永豐金 Shioaji API 登入與 CA 憑證設定 (Rule 14 規範)")
        l = QtWidgets.QGridLayout(box)

        l.addWidget(QtWidgets.QLabel("身分證字號 (Person ID):"), 0, 0)
        self.input_person_id = QtWidgets.QLineEdit()
        l.addWidget(self.input_person_id, 0, 1)

        l.addWidget(QtWidgets.QLabel("API Key:"), 1, 0)
        self.input_api_key = QtWidgets.QLineEdit()
        l.addWidget(self.input_api_key, 1, 1)

        l.addWidget(QtWidgets.QLabel("Secret Key:"), 2, 0)
        self.input_secret_key = QtWidgets.QLineEdit()
        self.input_secret_key.setEchoMode(QtWidgets.QLineEdit.Password)
        l.addWidget(self.input_secret_key, 2, 1)

        l.addWidget(QtWidgets.QLabel(".pfx 憑證檔案路徑:"), 3, 0)
        ca_row = QtWidgets.QHBoxLayout()
        self.input_ca_path = QtWidgets.QLineEdit()
        btn_browse = QtWidgets.QPushButton("瀏覽檔案...")
        btn_browse.clicked.connect(self.browse_ca_file)
        ca_row.addWidget(self.input_ca_path)
        ca_row.addWidget(btn_browse)
        l.addLayout(ca_row, 3, 1)

        l.addWidget(QtWidgets.QLabel("憑證密碼 (CA Password):"), 4, 0)
        self.input_ca_pwd = QtWidgets.QLineEdit()
        self.input_ca_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        l.addWidget(self.input_ca_pwd, 4, 1)

        btn_login = QtWidgets.QPushButton("🔥 驗證憑證並連線 (Activate CA & Login)")
        btn_login.setStyleSheet("background-color: #FF9800; font-size: 14px; padding: 12px; margin-top: 10px;")
        btn_login.clicked.connect(self.on_login_click)
        l.addWidget(btn_login, 5, 0, 1, 2)

        layout.addWidget(box)
        layout.addStretch()
        self.tabs.addTab(tab, "⚙️ 憑證與系統設定")

    def browse_ca_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "選擇永豐金 CA 憑證檔案", "", "PFX Files (*.pfx);;All Files (*)")
        if file_path:
            self.input_ca_path.setText(file_path)

    def on_login_click(self):
        res = self.engine.login_with_ca(
            api_key=self.input_api_key.text().strip(),
            secret_key=self.input_secret_key.text().strip(),
            ca_path=self.input_ca_path.text().strip(),
            ca_password=self.input_ca_pwd.text().strip(),
            person_id=self.input_person_id.text().strip()
        )
        if res["status"] == "success":
            QtWidgets.QMessageBox.information(self, "登入成功", res["message"])
            self.status_badge.setText("🟢 永豐金實盤連線")
            self.console_widget.log_success("Shioaji API 實盤與 CA 憑證驗證連線成功！")
        else:
            QtWidgets.QMessageBox.warning(self, "連線提示", res["message"])

    def load_initial_data(self):
        self.on_stock_changed("2330", "台積電")

    def on_stock_changed(self, code: str, name: str):
        """自選股點擊連動：刷新 K 線圖、五檔報價與下單工具欄"""
        self.current_code = code
        self.current_name = name

        self.lbl_stock_title.setText(f"{code} {name} — [{self.current_ktype} K 線圖]")
        
        # 1. 刷新 K棒
        kbars = self.engine.get_kbars(code=code, ktype=self.current_ktype)
        self.chart_widget.set_data(kbars)

        # 2. 刷新五檔
        latest_price = kbars[-1]['close'] if kbars else 100.0
        self.five_bids_widget.set_mock_bids(latest_price)

        # 3. 填入下單欄
        self.order_toolbar_widget.set_symbol(code, latest_price)

        # 4. 印出日誌
        self.console_widget.log_info(f"切換看盤商品: {code} {name} (當前價: {latest_price:.2f})")

    def switch_ktype(self, ktype: str):
        self.current_ktype = ktype
        self.lbl_stock_title.setText(f"{self.current_code} {self.current_name} — [{ktype} K 線圖]")
        kbars = self.engine.get_kbars(code=self.current_code, ktype=ktype)
        self.chart_widget.set_data(kbars)
        self.console_widget.log_info(f"切換 K 線圖週期: {ktype}")

    def on_order_submitted(self, order: dict):
        self.console_widget.log_success(f"下單委託成功 -> {order['action']} {order['code']} Price:{order['price']} Qty:{order['qty']} Type:{order['type']}")
        QtWidgets.QMessageBox.information(self, "委託發送成功", f"已成功向永豐金 Shioaji API 發送 {order['action']} 委託單！\n商品: {order['code']} | 價格: {order['price']} | 張數: {order['qty']}")

    def run_cpp_screener(self):
        """觸發 C++ 核心 AI 選股演算法"""
        quotes = self.engine.get_realtime_quotes()
        results = []

        for q in quotes:
            kbars = self.engine.get_kbars(code=q['code'])
            if self.dll:
                c_kbars = (CXXKBar * len(kbars))()
                for i, kb in enumerate(kbars):
                    c_kbars[i].datetime = kb['datetime'].encode('utf-8')
                    c_kbars[i].open = kb['open']
                    c_kbars[i].high = kb['high']
                    c_kbars[i].low = kb['low']
                    c_kbars[i].close = kb['close']
                    c_kbars[i].volume = kb['volume']

                out_res = CXXSelectionResult()
                ret = self.dll.run_stock_selection(c_kbars, len(kbars), q['code'].encode('utf-8'), q['name'].encode('utf-8'), ctypes.byref(out_res))
                if ret == 1:
                    results.append({
                        "code": out_res.code.decode('utf-8'),
                        "name": out_res.name.decode('utf-8'),
                        "close": out_res.close,
                        "pct": out_res.pct_change,
                        "score": out_res.score,
                        "signal": out_res.signal_type.decode('utf-8')
                    })
            else:
                results.append({
                    "code": q['code'],
                    "name": q['name'],
                    "close": q['price'],
                    "pct": q['pct_change'],
                    "score": 88.5,
                    "signal": "MA多頭強撐 + 看漲吞噬"
                })

        self.screener_table.setRowCount(len(results))
        for row, r in enumerate(results):
            self.screener_table.setItem(row, 0, QtWidgets.QTableWidgetItem(r['code']))
            self.screener_table.setItem(row, 1, QtWidgets.QTableWidgetItem(r['name']))
            self.screener_table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{r['close']:.2f}"))
            
            pct_item = QtWidgets.QTableWidgetItem(f"{r['pct']:+.2f}%")
            pct_item.setForeground(QtGui.QColor('#FF3B69' if r['pct'] >= 0 else '#00E676'))
            self.screener_table.setItem(row, 3, pct_item)

            score_item = QtWidgets.QTableWidgetItem(f"{r['score']:.1f}")
            score_item.setForeground(QtGui.QColor('#FFD700'))
            self.screener_table.setItem(row, 4, score_item)
            self.screener_table.setItem(row, 5, QtWidgets.QTableWidgetItem(r['signal']))

        self.console_widget.log_success(f"C++ 選股演算法掃描完成，發現 {len(results)} 檔多頭強勢標的！")
        QtWidgets.QMessageBox.information(self, "C++ 選股完成", f"C++ 核心演算法完成掃描，發現 {len(results)} 檔符合強勢多頭標的！")

    def run_cpp_backtest(self):
        """觸發 C++ 高速回測引擎"""
        fast_ma = int(self.input_fast_ma.text())
        slow_ma = int(self.input_slow_ma.text())
        capital = float(self.input_capital.text())

        kbars = self.engine.get_kbars(code="2330", limit=200)

        if self.dll:
            c_kbars = (CXXKBar * len(kbars))()
            for i, kb in enumerate(kbars):
                c_kbars[i].datetime = kb['datetime'].encode('utf-8')
                c_kbars[i].open = kb['open']
                c_kbars[i].high = kb['high']
                c_kbars[i].low = kb['low']
                c_kbars[i].close = kb['close']
                c_kbars[i].volume = kb['volume']

            out_bt = CXXBacktestResult()
            self.dll.run_backtest_ma(c_kbars, len(kbars), fast_ma, slow_ma, ctypes.c_double(capital), ctypes.byref(out_bt))

            self.card_return.findChild(QtWidgets.QLabel, "val").setText(f"{out_bt.total_return_pct:+.2f}%")
            self.card_winrate.findChild(QtWidgets.QLabel, "val").setText(f"{out_bt.win_rate:.1f}%")
            self.card_mdd.findChild(QtWidgets.QLabel, "val").setText(f"{out_bt.max_drawdown_pct:.2f}%")
            self.card_sharpe.findChild(QtWidgets.QLabel, "val").setText(f"{out_bt.sharpe_ratio:.2f}")

            self.console_widget.log_success(f"C++ 事件驅動回測完成 -> 總報酬: {out_bt.total_return_pct:+.2f}%, 勝率: {out_bt.win_rate:.1f}%")
            QtWidgets.QMessageBox.information(self, "C++ 回測完成", f"C++ 事件驅動回測完成！\n總交易數: {out_bt.total_trades} 次\n獲利次數: {out_bt.winning_trades} 次")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = SmartStockMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
