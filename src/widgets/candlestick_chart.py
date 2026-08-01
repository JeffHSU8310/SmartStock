from PySide6 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np
from typing import List, Dict

class CandlestickItem(pg.GraphicsObject):
    """pyqtgraph 原生紅綠 K 棒 (Candlestick Item)"""
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  # list of (t, open, close, min, max)
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        
        # 台灣股市色系：漲紅 (#FF3B69) / 跌綠 (#00E676)
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

            # 繪製上下影線 (Wick)
            p.drawLine(QtCore.QPointF(t, low_p), QtCore.QPointF(t, high_p))
            # 繪製實體 K 棒 (Body)
            p.drawRect(QtCore.QRectF(t - w, open_p, w * 2, close_p - open_p))

        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())

class NativeCandlestickChart(QtWidgets.QWidget):
    """Pure Native Qt6 pyqtgraph K 線與成交量/技術指標整合圖表"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 全彩暗黑主題畫布 (Dark Theme Graphics Layout)
        pg.setConfigOptions(antialias=True)
        self.win = pg.GraphicsLayoutWidget()
        self.win.setBackground('#121418')
        self.layout.addWidget(self.win)

        # 1. 主 K 線畫布 (Plot 1: KBars + MA)
        self.p1 = self.win.addPlot(row=0, col=0)
        self.p1.showGrid(x=True, y=True, alpha=0.15)
        self.p1.setLabel('left', '股價 (TWD)', color='#A0AAB8')
        self.p1.getAxis('bottom').setPen('#2A2E39')
        self.p1.getAxis('left').setPen('#2A2E39')

        # 2. 成交量畫布 (Plot 2: Volume Bars)
        self.win.nextRow()
        self.p2 = self.win.addPlot(row=1, col=0)
        self.p2.showGrid(x=True, y=True, alpha=0.15)
        self.p2.setLabel('left', '成交量', color='#A0AAB8')
        self.p2.setMaximumHeight(130)
        self.p2.setXLink(self.p1) # 讓 X 軸縮放平移完全連動

        # 十字線 (Crosshair Cursor)
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('#00E5FF', width=1, style=QtCore.Qt.DashLine))
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('#00E5FF', width=1, style=QtCore.Qt.DashLine))
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)

    def set_data(self, kbars: List[Dict]):
        """將 K棒 數據填入 Native 畫布"""
        if not kbars:
            return

        self.p1.clear()
        self.p2.clear()

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

        # 2. 畫 MA5 (亮黃) 與 MA20 (亮紫)
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
