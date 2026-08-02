from PySide6 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np
import pandas as pd
from typing import List, Dict

class DateAxisItem(pg.AxisItem):
    """自訂時間軸 (DateAxisItem: 格式化 X 軸顯示日期時間如 2025-12-01)"""
    def __init__(self, dates: List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dates = dates

    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            idx = int(round(v))
            if 0 <= idx < len(self.dates):
                strings.append(self.dates[idx])
            else:
                strings.append("")
        return strings

class CandlestickItem(pg.GraphicsObject):
    """pyqtgraph 原生紅綠 K 棒 (間隔正好等於一根 K 棒的寬度: w=0.25)"""
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        
        pen_red = pg.mkPen('#FF3B69', width=1.5)
        brush_red = pg.mkBrush('#FF3B69')
        pen_green = pg.mkPen('#00E676', width=1.5)
        brush_green = pg.mkBrush('#00E676')

        w = 0.25
        for t, open_p, close_p, low_p, high_p in self.data:
            if close_p >= open_p:
                p.setPen(pen_red)
                p.setBrush(brush_red)
            else:
                p.setPen(pen_green)
                p.setBrush(brush_green)

            # 1. 畫上下影線 (High to Low)
            p.drawLine(QtCore.QPointF(t, low_p), QtCore.QPointF(t, high_p))

            # 2. 畫 K 棒實體 (Open to Close)
            height = close_p - open_p
            if abs(height) < 1e-5:
                # 漲停/平盤一字線：畫一條橫平的線 (一)
                p.drawLine(QtCore.QPointF(t - w, open_p), QtCore.QPointF(t + w, open_p))
            else:
                p.drawRect(QtCore.QRectF(t - w, open_p, w * 2, height))

        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())

class NativeCandlestickChart(QtWidgets.QWidget):
    """Pure Native Qt6 pyqtgraph 旗艦級 3 層 K 線與 MACD 圖表 (支援游標精準吸附, 垂直 Splitter 自由拖拉高度與 5 大時間快選)"""
    hover_kbar_signal = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.kbars_data = []
        self.dates = []
        self.ma5_vals = []
        self.ma20_vals = []
        self.ma60_vals = []
        self.ma120_vals = []
        self.dif_vals = []
        self.dea_vals = []
        self.macd_bars = []
        self.ref_price = 0.0  # ★ 當日官方參考價 (Reference Price)，由外部傳入 ★

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        pg.setConfigOptions(antialias=True)
        
        # 導入 QSplitter(QtCore.Qt.Vertical) 實現主圖 vs 成交量 vs MACD 上下拖拉高度
        self.chart_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.layout.addWidget(self.chart_splitter)

        self._init_plots()

    def _init_plots(self):
        # 1. 主 K 線畫布 (Plot 1: Price & MAs)
        self.win1 = pg.GraphicsLayoutWidget()
        self.win1.setBackground('#121418')
        self.p1 = self.win1.addPlot(row=0, col=0)
        self.p1.showGrid(x=True, y=True, alpha=0.15)
        self.p1.setLabel('left', 'Price', color='#A0AAB8')
        self.p1.getAxis('bottom').setPen('#2A2E39')
        self.p1.getAxis('left').setPen('#2A2E39')
        self.chart_splitter.addWidget(self.win1)

        # 2. 副圖一：成交量畫布 (Plot 2: Volume)
        self.win2 = pg.GraphicsLayoutWidget()
        self.win2.setBackground('#121418')
        self.p2 = self.win2.addPlot(row=0, col=0)
        self.p2.showGrid(x=True, y=True, alpha=0.15)
        self.p2.setLabel('left', 'Volume', color='#A0AAB8')
        self.p2.setXLink(self.p1)
        self.chart_splitter.addWidget(self.win2)

        # 3. 副圖二：MACD 畫布 (Plot 3: MACD Indicator - DIF, DEA, MACD Bar)
        self.win3 = pg.GraphicsLayoutWidget()
        self.win3.setBackground('#121418')
        self.p3 = self.win3.addPlot(row=0, col=0)
        self.p3.showGrid(x=True, y=True, alpha=0.15)
        self.p3.setLabel('left', 'MACD', color='#A0AAB8')
        self.p3.setXLink(self.p1)
        self.chart_splitter.addWidget(self.win3)

        # 設定初始拖拉比例 (主圖大、兩個副圖小)
        self.chart_splitter.setSizes([480, 120, 120])

        # 十字線 (主圖, 副圖一, 副圖二連動)
        self.vLine1 = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('#00E5FF', width=1, style=QtCore.Qt.DashLine))
        self.hLine1 = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('#00E5FF', width=1, style=QtCore.Qt.DashLine))
        self.p1.addItem(self.vLine1, ignoreBounds=True)
        self.p1.addItem(self.hLine1, ignoreBounds=True)

        self.vLine2 = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('#00E5FF', width=1, style=QtCore.Qt.DashLine))
        self.p2.addItem(self.vLine2, ignoreBounds=True)

        self.vLine3 = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('#00E5FF', width=1, style=QtCore.Qt.DashLine))
        self.p3.addItem(self.vLine3, ignoreBounds=True)

        # 綁定游標懸停事件 (實現精準吸附 K 棒)
        self.win1.scene().sigMouseMoved.connect(self.on_mouse_moved)

    def set_ref_price(self, ref_price: float):
        """★ 設定當日官方參考價 (Reference Price)，用於最新 K 棒漲跌計算 ★"""
        self.ref_price = ref_price

    def set_data(self, kbars: List[Dict]):
        """切換商品時 100% 徹底清空重置數據、DateAxisItem 與 3 層圖表」"""
        self.kbars_data = []
        self.dates = []
        self.ma5_vals = []
        self.ma20_vals = []
        self.ma60_vals = []
        self.ma120_vals = []
        self.dif_vals = []
        self.dea_vals = []
        self.macd_bars = []

        self.p1.clear()
        self.p2.clear()
        self.p3.clear()

        if not kbars:
            return

        self.kbars_data = kbars
        self.dates = [kb['datetime'] for kb in kbars]

        axis_p1 = DateAxisItem(self.dates, orientation='bottom')
        axis_p2 = DateAxisItem(self.dates, orientation='bottom')
        axis_p3 = DateAxisItem(self.dates, orientation='bottom')

        self.p1.setAxisItems({'bottom': axis_p1})
        self.p2.setAxisItems({'bottom': axis_p2})
        self.p3.setAxisItems({'bottom': axis_p3})

        self.p1.addItem(self.vLine1, ignoreBounds=True)
        self.p1.addItem(self.hLine1, ignoreBounds=True)
        self.p2.addItem(self.vLine2, ignoreBounds=True)
        self.p3.addItem(self.vLine3, ignoreBounds=True)

        chart_data = []
        closes = []
        volumes = []

        for i, kb in enumerate(kbars):
            chart_data.append((i, kb['open'], kb['close'], kb['low'], kb['high']))
            closes.append(kb['close'])
            volumes.append(kb['volume'])

        # 1. 畫主圖 K 棒 (w=0.25, 間隔正好等於一根 K 棒寬度)
        item = CandlestickItem(chart_data)
        self.p1.addItem(item)

        # 2. 計算 MA5, MA20, MA60, MA120
        closes_arr = np.array(closes, dtype=float)
        if len(closes_arr) >= 5:
            ma5 = np.convolve(closes_arr, np.ones(5)/5, mode='valid')
            self.ma5_vals = [np.nan]*4 + list(ma5)
            self.p1.plot(self.ma5_vals, pen=pg.mkPen('#FFD700', width=1.5), name='MA5')

        if len(closes_arr) >= 20:
            ma20 = np.convolve(closes_arr, np.ones(20)/20, mode='valid')
            self.ma20_vals = [np.nan]*19 + list(ma20)
            self.p1.plot(self.ma20_vals, pen=pg.mkPen('#FFFFFF', width=1.5), name='MA20')

        if len(closes_arr) >= 60:
            ma60 = np.convolve(closes_arr, np.ones(60)/60, mode='valid')
            self.ma60_vals = [np.nan]*59 + list(ma60)
            self.p1.plot(self.ma60_vals, pen=pg.mkPen('#00E5FF', width=1.5), name='MA60')

        if len(closes_arr) >= 120:
            ma120 = np.convolve(closes_arr, np.ones(120)/120, mode='valid')
            self.ma120_vals = [np.nan]*119 + list(ma120)
            self.p1.plot(self.ma120_vals, pen=pg.mkPen('#E040FB', width=1.5), name='MA120')

        # 3. 畫副圖一成交量柱狀圖 (固定 y0=0)
        v_colors = ['#FF3B69' if c >= o else '#00E676' for o, c in zip([k['open'] for k in kbars], closes)]
        vol_bars = pg.BarGraphItem(x=list(range(len(kbars))), height=volumes, y0=0, width=0.5, brushes=v_colors)
        self.p2.addItem(vol_bars)

        # 4. 計算並繪製副圖二 MACD 指標 (EMA12, EMA26, DIF, DEA, MACD Bar)
        if len(closes_arr) >= 26:
            s_close = pd.Series(closes_arr)
            ema12 = s_close.ewm(span=12, adjust=False).mean()
            ema26 = s_close.ewm(span=26, adjust=False).mean()
            dif = ema12 - ema26
            dea = dif.ewm(span=9, adjust=False).mean()
            macd_bar = (dif - dea) * 2.0

            self.dif_vals = list(dif)
            self.dea_vals = list(dea)
            self.macd_bars = list(macd_bar)

            self.p3.plot(self.dif_vals, pen=pg.mkPen('#00E5FF', width=1.5), name='DIF')
            self.p3.plot(self.dea_vals, pen=pg.mkPen('#FF9800', width=1.5), name='DEA')

            m_colors = ['#FF3B69' if v >= 0 else '#00E676' for v in macd_bar]
            m_bars = pg.BarGraphItem(x=list(range(len(kbars))), height=macd_bar, y0=0, width=0.5, brushes=m_colors)
            self.p3.addItem(m_bars)

        # 5. 預設主圖視野精準縮放至近 1 年預設 (顯示 60 根精選大寬度 K 棒)
        self.set_view_range_months(12)

    def set_view_range_months(self, months: int):
        """修正時間快選按鈕：縮放 X 軸並針對可視區域自適應 Y 軸"""
        if not self.kbars_data:
            return
        
        total_cnt = len(self.kbars_data)
        bars_map = {6: 30, 12: 60, 24: 120, 60: 300, 120: 600}
        bars_count = bars_map.get(months, 30)

        start_idx = max(0, total_cnt - bars_count)
        
        self.p1.setXRange(start_idx, total_cnt, padding=0.01)

        visible_kbars = self.kbars_data[start_idx:total_cnt]
        if visible_kbars:
            lows = [k['low'] for k in visible_kbars]
            highs = [k['high'] for k in visible_kbars]
            min_y, max_y = min(lows), max(highs)
            padding_y = (max_y - min_y) * 0.05 if max_y != min_y else 10.0
            self.p1.setYRange(min_y - padding_y, max_y + padding_y, padding=0)

            vols = [k['volume'] for k in visible_kbars]
            max_v = max(vols) if vols else 1000
            self.p2.setYRange(0, max_v * 1.1, padding=0)

    def on_mouse_moved(self, pos):
        """游標懸停處理：X 軸精準吸附至 K 棒正中央 round(mouse_x)"""
        if not self.kbars_data:
            return

        mouse_point = self.p1.vb.mapSceneToView(pos)
        idx = int(round(mouse_point.x()))

        if 0 <= idx < len(self.kbars_data):
            self.vLine1.setPos(idx)
            self.vLine2.setPos(idx)
            self.vLine3.setPos(idx)
            self.hLine1.setPos(mouse_point.y())

            kb = self.kbars_data[idx]
            open_p = kb['open']
            close_p = kb['close']
            high_p = kb['high']
            low_p = kb['low']
            vol = kb['volume']
            # ★ 漲跌計算：最新一根 K 棒用當日參考價 (Reference Price)，歷史 K 棒用前一根收盤 ★
            is_last_bar = (idx == len(self.kbars_data) - 1)
            if is_last_bar and self.ref_price > 0:
                base_price = self.ref_price
            elif idx > 0:
                base_price = self.kbars_data[idx - 1]['close']
            else:
                base_price = open_p
            change = close_p - base_price
            pct_change = (change / base_price * 100.0) if base_price != 0 else 0.0

            ma5_val = self.ma5_vals[idx] if idx < len(self.ma5_vals) and not np.isnan(self.ma5_vals[idx]) else None
            ma20_val = self.ma20_vals[idx] if idx < len(self.ma20_vals) and not np.isnan(self.ma20_vals[idx]) else None

            dif_val = self.dif_vals[idx] if idx < len(self.dif_vals) else None
            dea_val = self.dea_vals[idx] if idx < len(self.dea_vals) else None

            info = {
                "datetime": kb['datetime'],
                "open": open_p,
                "high": high_p,
                "low": low_p,
                "close": close_p,
                "change": change,
                "pct_change": pct_change,
                "volume": vol,
                "ma5": ma5_val,
                "ma20": ma20_val,
                "dif": dif_val,
                "dea": dea_val
            }
            self.hover_kbar_signal.emit(info)
