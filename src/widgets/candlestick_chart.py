from PySide6 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np
from typing import List, Dict

class DateAxisItem(pg.AxisItem):
    """自訂時間軸 (DateAxisItem: 格式化 X 軸顯示日期時間如 2026-07-31 或 10:30)"""
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
    """pyqtgraph 原生紅綠 K 棒 (徹底還原標準漲停一字線與實體 K 棒)"""
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

        w = 0.30
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
            # 徹底廢除 height = 0.25 硬拉高度代碼！當 open == close 時畫橫向一字線 (一)
            if abs(height) < 1e-5:
                # 漲停一字線 / 十字線 / 平盤一字線：畫一條橫平的線 (一)
                p.drawLine(QtCore.QPointF(t - w, open_p), QtCore.QPointF(t + w, open_p))
            else:
                p.drawRect(QtCore.QRectF(t - w, open_p, w * 2, height))

        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())

class NativeCandlestickChart(QtWidgets.QWidget):
    """Pure Native Qt6 pyqtgraph K 線圖 (支援切換商品 Y軸 AutoRange 完全重置)"""
    hover_kbar_signal = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.kbars_data = []
        self.dates = []
        self.ma5_vals = []
        self.ma20_vals = []

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        pg.setConfigOptions(antialias=True)
        self.win = pg.GraphicsLayoutWidget()
        self.win.setBackground('#121418')
        self.layout.addWidget(self.win)

        self._init_plots()

    def _init_plots(self):
        # 1. 主 K 線畫布 (Plot 1)
        self.p1 = self.win.addPlot(row=0, col=0)
        self.p1.showGrid(x=True, y=True, alpha=0.15)
        self.p1.setLabel('left', '股價 (TWD)', color='#A0AAB8')
        self.p1.getAxis('bottom').setPen('#2A2E39')
        self.p1.getAxis('left').setPen('#2A2E39')

        # 2. 副圖成交量畫布 (Plot 2)
        self.win.nextRow()
        self.p2 = self.win.addPlot(row=1, col=0)
        self.p2.showGrid(x=True, y=True, alpha=0.15)
        self.p2.setLabel('left', '成交量', color='#A0AAB8')
        self.p2.setMaximumHeight(130)
        self.p2.setXLink(self.p1)

        # 懸停動態十字線
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('#00E5FF', width=1, style=QtCore.Qt.DashLine))
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('#00E5FF', width=1, style=QtCore.Qt.DashLine))
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)

        # 綁定游標懸停事件
        self.win.scene().sigMouseMoved.connect(self.on_mouse_moved)

    def set_data(self, kbars: List[Dict]):
        """切換商品時 100% 重置數據、DateAxisItem 與 Y 軸 AutoRange"""
        self.kbars_data = []
        self.dates = []
        self.ma5_vals = []
        self.ma20_vals = []

        if not kbars:
            self.p1.clear()
            self.p2.clear()
            return

        self.kbars_data = kbars
        self.dates = [kb['datetime'] for kb in kbars]

        self.p1.clear()
        self.p2.clear()

        # 重建時間軸 DateAxisItem
        date_axis_main = DateAxisItem(self.dates, orientation='bottom')
        date_axis_sub = DateAxisItem(self.dates, orientation='bottom')

        self.p1.setAxisItems({'bottom': date_axis_main})
        self.p2.setAxisItems({'bottom': date_axis_sub})

        # 重新加入十字線
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)

        chart_data = []
        closes = []
        volumes = []

        for i, kb in enumerate(kbars):
            chart_data.append((i, kb['open'], kb['close'], kb['low'], kb['high']))
            closes.append(kb['close'])
            volumes.append(kb['volume'])

        # 1. 畫 K 棒
        item = CandlestickItem(chart_data)
        self.p1.addItem(item)

        # 2. 計算 MA5 與 MA20 技術指標 (使用 np.nan 替代 None 以完全符合 pyqtgraph 要求)
        closes_arr = np.array(closes, dtype=float)
        if len(closes_arr) >= 5:
            ma5 = np.convolve(closes_arr, np.ones(5)/5, mode='valid')
            self.ma5_vals = [np.nan]*4 + list(ma5)
            self.p1.plot(self.ma5_vals, pen=pg.mkPen('#FFD700', width=1.5), name='MA5')

        if len(closes_arr) >= 20:
            ma20 = np.convolve(closes_arr, np.ones(20)/20, mode='valid')
            self.ma20_vals = [np.nan]*19 + list(ma20)
            self.p1.plot(self.ma20_vals, pen=pg.mkPen('#E040FB', width=1.5), name='MA20')

        # 3. 畫成交量副圖 (柱狀圖)
        v_colors = ['#FF3B69' if c >= o else '#00E676' for o, c in zip([k['open'] for k in kbars], closes)]
        vol_bars = pg.BarGraphItem(x=list(range(len(kbars))), height=volumes, width=0.6, brushes=v_colors)
        self.p2.addItem(vol_bars)

        # 4. 重置 Y 軸 AutoRange 讓畫面 100% 適應當前價格刻度
        self.p1.enableAutoRange(axis='y', enable=True)
        self.p1.autoRange()
        self.p2.enableAutoRange(axis='y', enable=True)
        self.p2.autoRange()

    def on_mouse_moved(self, pos):
        """游標懸停事件處理：更新十字線位置並發送 Hover K棒 詳細資訊"""
        if not self.kbars_data:
            return

        mouse_point = self.p1.vb.mapSceneToView(pos)
        idx = int(round(mouse_point.x()))

        if 0 <= idx < len(self.kbars_data):
            self.vLine.setPos(mouse_point.x())
            self.hLine.setPos(mouse_point.y())

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

            # 計算 MA 趨勢箭頭
            ma5_arrow = "➡️"
            if idx > 0 and ma5_val and self.ma5_vals[idx-1] and not np.isnan(self.ma5_vals[idx-1]):
                ma5_arrow = "⬆️" if ma5_val > self.ma5_vals[idx-1] else ("⬇️" if ma5_val < self.ma5_vals[idx-1] else "➡️")

            ma20_arrow = "➡️"
            if idx > 0 and ma20_val and self.ma20_vals[idx-1] and not np.isnan(self.ma20_vals[idx-1]):
                ma20_arrow = "⬆️" if ma20_val > self.ma20_vals[idx-1] else ("⬇️" if ma20_val < self.ma20_vals[idx-1] else "➡️")

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
                "ma5_arrow": ma5_arrow,
                "ma20": ma20_val,
                "ma20_arrow": ma20_arrow
            }
            self.hover_kbar_signal.emit(info)
