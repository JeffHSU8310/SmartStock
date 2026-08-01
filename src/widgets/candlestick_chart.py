from PySide6 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np
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
    """pyqtgraph 原生紅綠 K 棒 (拉開適當間距 w=0.32，對齊專業高對比樣式)"""
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

        w = 0.32
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
    """Pure Native Qt6 pyqtgraph 旗艦級 3 層 K 線與 MACD 圖表 (支援游標精準吸附與 5 大時間快選)"""
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

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        pg.setConfigOptions(antialias=True)
        self.win = pg.GraphicsLayoutWidget()
        self.win.setBackground('#121418')
        self.layout.addWidget(self.win)

        self._init_plots()

    def _init_plots(self):
        # 1. 主 K 線畫布 (Plot 1: Price & MAs)
        self.p1 = self.win.addPlot(row=0, col=0)
        self.p1.showGrid(x=True, y=True, alpha=0.15)
        self.p1.setLabel('left', 'Price', color='#A0AAB8')
        self.p1.getAxis('bottom').setPen('#2A2E39')
        self.p1.getAxis('left').setPen('#2A2E39')

        # 2. 副圖一：成交量畫布 (Plot 2: Volume)
        self.win.nextRow()
        self.p2 = self.win.addPlot(row=1, col=0)
        self.p2.showGrid(x=True, y=True, alpha=0.15)
        self.p2.setLabel('left', 'Volume', color='#A0AAB8')
        self.p2.setMaximumHeight(110)
        self.p2.setXLink(self.p1)

        # 3. 副圖二：MACD 畫布 (Plot 3: MACD Indicator - DIF, DEA, MACD Bar)
        self.win.nextRow()
        self.p3 = self.win.addPlot(row=2, col=0)
        self.p3.showGrid(x=True, y=True, alpha=0.15)
        self.p3.setLabel('left', 'MACD', color='#A0AAB8')
        self.p3.setMaximumHeight(110)
        self.p3.setXLink(self.p1)

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
        self.win.scene().sigMouseMoved.connect(self.on_mouse_moved)

    def set_data(self, kbars: List[Dict]):
        """切換商品時 100% 重置數據、DateAxisItem 與 3 層圖表」"""
        self.kbars_data = []
        self.dates = []
        self.ma5_vals = []
        self.ma20_vals = []
        self.ma60_vals = []
        self.ma120_vals = []
        self.dif_vals = []
        self.dea_vals = []
        self.macd_bars = []

        if not kbars:
            self.p1.clear()
            self.p2.clear()
            self.p3.clear()
            return

        self.kbars_data = kbars
        self.dates = [kb['datetime'] for kb in kbars]

        self.p1.clear()
        self.p2.clear()
        self.p3.clear()

        # 重建時間軸 DateAxisItem
        axis_p1 = DateAxisItem(self.dates, orientation='bottom')
        axis_p2 = DateAxisItem(self.dates, orientation='bottom')
        axis_p3 = DateAxisItem(self.dates, orientation='bottom')

        self.p1.setAxisItems({'bottom': axis_p1})
        self.p2.setAxisItems({'bottom': axis_p2})
        self.p3.setAxisItems({'bottom': axis_p3})

        # 重新加入十字線
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

        # 1. 畫主圖 K 棒
        item = CandlestickItem(chart_data)
        self.p1.addItem(item)

        # 2. 計算 MA5, MA20, MA60, MA120 (以 np.nan 防禦 pyqtgraph)
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

        # 3. 畫副圖一成交量柱狀圖
        v_colors = ['#FF3B69' if c >= o else '#00E676' for o, c in zip([k['open'] for k in kbars], closes)]
        vol_bars = pg.BarGraphItem(x=list(range(len(kbars))), height=volumes, width=0.6, brushes=v_colors)
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

            # 畫 DIF 快線 (天藍) 與 DEA 慢線 (橙黃)
            self.p3.plot(self.dif_vals, pen=pg.mkPen('#00E5FF', width=1.5), name='DIF')
            self.p3.plot(self.dea_vals, pen=pg.mkPen('#FF9800', width=1.5), name='DEA')

            # 畫 MACD 柱狀圖 (正值紅柱、負值綠柱)
            m_colors = ['#FF3B69' if v >= 0 else '#00E676' for v in macd_bar]
            m_bars = pg.BarGraphItem(x=list(range(len(kbars))), height=macd_bar, width=0.5, brushes=m_colors)
            self.p3.addItem(m_bars)

        # 5. ★ 預設顯示 6 個月視野 (視區間約 120 根日 K) ★
        total_cnt = len(kbars)
        start_idx = max(0, total_cnt - 120)
        self.p1.setXRange(start_idx, total_cnt, padding=0.02)
        self.p1.enableAutoRange(axis='y', enable=True)
        self.p1.autoRange()

    def set_view_range_months(self, months: int):
        """時間視角快選按鈕 (6個月 / 1年 / 2年 / 5年 / 10年) 瞬間精準縮放"""
        if not self.kbars_data:
            return
        
        total_cnt = len(self.kbars_data)
        bars_count = int(months * 20) # 1 個月約 20 個交易日
        
        start_idx = max(0, total_cnt - bars_count)
        self.p1.setXRange(start_idx, total_cnt, padding=0.02)
        self.p1.enableAutoRange(axis='y', enable=True)
        self.p1.autoRange()

    def on_mouse_moved(self, pos):
        """游標懸停處理：X 軸精準吸附至 K 棒正中央 round(mouse_x)"""
        if not self.kbars_data:
            return

        mouse_point = self.p1.vb.mapSceneToView(pos)
        # 精準四捨五入吸附 K 棒正中央
        idx = int(round(mouse_point.x()))

        if 0 <= idx < len(self.kbars_data):
            # 十字線完美精準對齊正中央
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
            change = close_p - open_p
            pct_change = (change / open_p * 100.0) if open_p != 0 else 0.0

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
