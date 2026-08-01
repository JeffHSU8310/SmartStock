from PySide6 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np
from typing import List, Dict

class DateAxisItem(pg.AxisItem):
    """自訂時間軸 (DateAxisItem: 格式化 X 軸顯示日期時間如 2026-07-31 或 10:30) (圖片 4 需求)"""
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
    """pyqtgraph 原生紅綠 K 棒 (Candlestick Item)"""
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  # list of (t, open, close, min, max)
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        
        pen_red = pg.mkPen('#FF3B69', width=1.2)
        brush_red = pg.mkBrush('#FF3B69')
        pen_green = pg.mkPen('#00E676', width=1.2)
        brush_green = pg.mkBrush('#00E676')

        w = 0.35
        for t, open_p, close_p, low_p, high_p in self.data:
            if close_p >= open_p:
                p.setPen(pen_red)
                p.setBrush(brush_red)
            else:
                p.setPen(pen_green)
                p.setBrush(brush_green)

            p.drawLine(QtCore.QPointF(t, low_p), QtCore.QPointF(t, high_p))
            p.drawRect(QtCore.QRectF(t - w, open_p, w * 2, close_p - open_p))

        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())

class NativeCandlestickChart(QtWidgets.QWidget):
    """Pure Native Qt6 pyqtgraph K 線圖 (支援 DateAxis 時間軸與滑鼠懸停 K棒 資訊高亮)"""
    hover_kbar_signal = QtCore.Signal(dict) # 發送當前懸停的 K棒 數據

    def __init__(self, parent=None):
        super().__init__(parent)
        self.kbars_data = []
        self.dates = []

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

        # 懸停動態十字線 (Crosshair Cursor)
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('#00E5FF', width=1, style=QtCore.Qt.DashLine))
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('#00E5FF', width=1, style=QtCore.Qt.DashLine))
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)

        # 綁定游標跟隨與懸停事件 (圖片 3 需求實作)
        self.win.scene().sigMouseMoved.connect(self.on_mouse_moved)

    def set_data(self, kbars: List[Dict]):
        """填入 K 棒數據並即時重建 DateAxis 時間軸 (圖片 4 需求實作)"""
        if not kbars:
            return

        self.kbars_data = kbars
        self.dates = [kb['datetime'] for kb in kbars]

        self.p1.clear()
        self.p2.clear()

        # 重置時間軸 (DateAxisItem)
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

        # 2. 畫 MA5 (黃) 與 MA20 (紫)
        closes_arr = np.array(closes)
        if len(closes_arr) >= 5:
            ma5 = np.convolve(closes_arr, np.ones(5)/5, mode='valid')
            self.p1.plot(np.arange(4, len(closes_arr)), ma5, pen=pg.mkPen('#FFD700', width=1.5), name='MA5')
        if len(closes_arr) >= 20:
            ma20 = np.convolve(closes_arr, np.ones(20)/20, mode='valid')
            self.p1.plot(np.arange(19, len(closes_arr)), ma20, pen=pg.mkPen('#E040FB', width=1.5), name='MA20')

        # 3. 畫成交量柱狀圖 (Volume Bar)
        x_indices = np.arange(len(volumes))
        colors = ['#FF3B69' if kb['close'] >= kb['open'] else '#00E676' for kb in kbars]
        bargraph = pg.BarGraphItem(x=x_indices, height=volumes, width=0.6, brushes=colors, pens=colors)
        self.p2.addItem(bargraph)

    def on_mouse_moved(self, pos):
        """游標懸停事件：即時發送該根 K 線之開高低收、漲跌與成交量 (圖片 3 需求實作)"""
        if not self.kbars_data:
            return

        mousePoint = self.p1.vb.mapSceneToView(pos)
        idx = int(round(mousePoint.x()))

        if 0 <= idx < len(self.kbars_data):
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

            kb = self.kbars_data[idx]
            prev_close = self.kbars_data[idx - 1]['close'] if idx > 0 else kb['open']
            change = kb['close'] - prev_close
            pct_change = (change / prev_close * 100.0) if prev_close != 0 else 0.0

            info = {
                "datetime": kb['datetime'],
                "open": kb['open'],
                "high": kb['high'],
                "low": kb['low'],
                "close": kb['close'],
                "change": change,
                "pct_change": pct_change,
                "volume": kb['volume']
            }
            self.hover_kbar_signal.emit(info)
