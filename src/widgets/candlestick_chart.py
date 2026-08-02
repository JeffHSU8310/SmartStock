from PySide6 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np
import pandas as pd
from typing import List, Dict, Any

try:
    from src.widgets.indicator_settings_dialog import DEFAULT_INDICATOR_CONFIG, LINE_STYLES
except ImportError:
    from widgets.indicator_settings_dialog import DEFAULT_INDICATOR_CONFIG, LINE_STYLES

LINE_STYLES_MAP = {
    "實線 (SolidLine)": QtCore.Qt.SolidLine,
    "虛線 (DashLine)": QtCore.Qt.DashLine,
    "點線 (DotLine)": QtCore.Qt.DotLine,
    "點劃線 (DashDotLine)": QtCore.Qt.DashDotLine
}

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
    """Pure Native Qt6 pyqtgraph 旗艦級 3 層 K 線圖 (支援 7 組均線 SMA/EMA、雙層布林通道、多種副圖指標 KDJ/MACD/RSI/Volume/KD/WR/BIAS/ATR/DMI/CCI)"""
    hover_kbar_signal = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.kbars_data = []
        self.dates = []
        self.ref_price = 0.0  # ★ 當日官方參考價 (Reference Price) ★
        self.indicator_config = dict(DEFAULT_INDICATOR_CONFIG)

        # 儲存計算結果 (用於 hover 顯示)
        self.computed_ma = []       # list of dict: {name, period, color, vals}
        self.computed_bb = {}       # {mid, u1, l1, u2, l2}
        self.computed_sub1 = {}     # {type, data_dict}
        self.computed_sub2 = {}     # {type, data_dict}

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        pg.setConfigOptions(antialias=True)
        
        # 導入 QSplitter(QtCore.Qt.Vertical) 實現主圖 vs 副圖一 vs 副圖二 上下拖拉高度
        self.chart_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.layout.addWidget(self.chart_splitter)

        self._init_plots()

    def _init_plots(self):
        # 1. 主 K 線畫布 (Plot 1: Price, MAs & Bollinger Bands)
        self.win1 = pg.GraphicsLayoutWidget()
        self.win1.setBackground('#121418')
        self.p1 = self.win1.addPlot(row=0, col=0)
        self.p1.showGrid(x=True, y=True, alpha=0.15)
        self.p1.setLabel('left', 'Price', color='#A0AAB8')
        self.p1.getAxis('bottom').setPen('#2A2E39')
        self.p1.getAxis('left').setPen('#2A2E39')
        self.chart_splitter.addWidget(self.win1)

        # 2. 副圖一畫布 (Plot 2: Sub-Chart 1 - Volume / MACD / KDJ / RSI etc.)
        self.win2 = pg.GraphicsLayoutWidget()
        self.win2.setBackground('#121418')
        self.p2 = self.win2.addPlot(row=0, col=0)
        self.p2.showGrid(x=True, y=True, alpha=0.15)
        self.p2.setLabel('left', 'Sub 1', color='#A0AAB8')
        self.p2.setXLink(self.p1)
        self.chart_splitter.addWidget(self.win2)

        # 3. 副圖二畫布 (Plot 3: Sub-Chart 2 - MACD / KDJ / RSI etc.)
        self.win3 = pg.GraphicsLayoutWidget()
        self.win3.setBackground('#121418')
        self.p3 = self.win3.addPlot(row=0, col=0)
        self.p3.showGrid(x=True, y=True, alpha=0.15)
        self.p3.setLabel('left', 'Sub 2', color='#A0AAB8')
        self.p3.setXLink(self.p1)
        self.chart_splitter.addWidget(self.win3)

        # 設定初始拖拉比例
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
        """設定當日官方參考價 (Reference Price)，用於最新 K 棒漲跌計算"""
        self.ref_price = ref_price

    def set_indicator_config(self, config: Dict[str, Any]):
        """更新技術指標與顏色設定並重繪圖表"""
        self.indicator_config = dict(config)
        if self.kbars_data:
            self.set_data(self.kbars_data)

    def set_data(self, kbars: List[Dict]):
        """切換商品或更新數據時 100% 徹底清空重置數據、DateAxisItem 與指標圖表"""
        self.kbars_data = []
        self.dates = []
        self.computed_ma = []
        self.computed_bb = {}
        self.computed_sub1 = {}
        self.computed_sub2 = {}

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
        highs = []
        lows = []
        opens = []
        volumes = []

        for i, kb in enumerate(kbars):
            chart_data.append((i, kb['open'], kb['close'], kb['low'], kb['high']))
            opens.append(kb['open'])
            closes.append(kb['close'])
            highs.append(kb['high'])
            lows.append(kb['low'])
            volumes.append(kb['volume'])

        df = pd.DataFrame({
            'open': opens, 'close': closes, 'high': highs, 'low': lows, 'volume': volumes
        })
        s_close = df['close']

        # 1. 畫主圖 K 棒
        item = CandlestickItem(chart_data)
        self.p1.addItem(item)

        # 2. 計算與繪製主圖 7 組均線 (MA1 ~ MA7)
        if self.indicator_config.get("ma_enabled", True):
            ma_items = self.indicator_config.get("ma_items", DEFAULT_INDICATOR_CONFIG["ma_items"])
            for idx_ma, item_cfg in enumerate(ma_items):
                if not item_cfg.get("enabled", True):
                    continue

                period = item_cfg.get("period", 5)
                ma_type = item_cfg.get("type", "SMA").upper()
                color_hex = item_cfg.get("color", "#FFFFFF")
                style_str = item_cfg.get("style", "實線 (SolidLine)")
                pen_style = LINE_STYLES_MAP.get(style_str, QtCore.Qt.SolidLine)

                if len(s_close) >= period:
                    if ma_type == "EMA":
                        ma_ser = s_close.ewm(span=period, adjust=False).mean()
                    else:
                        ma_ser = s_close.rolling(window=period).mean()

                    vals = list(ma_ser)
                    label_name = f"{ma_type}{period}"
                    
                    pen = pg.mkPen(color_hex, width=1.5, style=pen_style)
                    self.p1.plot(vals, pen=pen, name=label_name)

                    self.computed_ma.append({
                        "name": label_name,
                        "period": period,
                        "color": color_hex,
                        "vals": vals
                    })

        # 3. 計算與繪製布林通道 (Bollinger Bands - 雙層上下限)
        if self.indicator_config.get("bb_enabled", True):
            bb_period = self.indicator_config.get("bb_period", 20)
            bb_k1 = self.indicator_config.get("bb_k1", 1.0)
            bb_k2 = self.indicator_config.get("bb_k2", 2.0)

            if len(s_close) >= bb_period:
                mid_ser = s_close.rolling(window=bb_period).mean()
                std_ser = s_close.rolling(window=bb_period).std()

                u1_ser = mid_ser + bb_k1 * std_ser
                l1_ser = mid_ser - bb_k1 * std_ser
                u2_ser = mid_ser + bb_k2 * std_ser
                l2_ser = mid_ser - bb_k2 * std_ser

                mid_vals, u1_vals, l1_vals, u2_vals, l2_vals = list(mid_ser), list(u1_ser), list(l1_ser), list(u2_ser), list(l2_ser)

                # 畫中線
                mid_pen = pg.mkPen(self.indicator_config.get("bb_mid_color", "#FFD700"), width=1.5, style=LINE_STYLES_MAP.get(self.indicator_config.get("bb_mid_style", "實線 (SolidLine)"), QtCore.Qt.SolidLine))
                self.p1.plot(mid_vals, pen=mid_pen, name=f"BB_Mid({bb_period})")

                # 畫第一層 (Upper1/Lower1)
                b1_pen = pg.mkPen(self.indicator_config.get("bb_b1_color", "#00E5FF"), width=1.2, style=LINE_STYLES_MAP.get(self.indicator_config.get("bb_b1_style", "虛線 (DashLine)"), QtCore.Qt.DashLine))
                self.p1.plot(u1_vals, pen=b1_pen, name=f"BB_Upper1({bb_k1}σ)")
                self.p1.plot(l1_vals, pen=b1_pen, name=f"BB_Lower1({bb_k1}σ)")

                # 畫第二層 (Upper2/Lower2)
                b2_pen = pg.mkPen(self.indicator_config.get("bb_b2_color", "#E040FB"), width=1.2, style=LINE_STYLES_MAP.get(self.indicator_config.get("bb_b2_style", "點劃線 (DashDotLine)"), QtCore.Qt.DashDotLine))
                self.p1.plot(u2_vals, pen=b2_pen, name=f"BB_Upper2({bb_k2}σ)")
                self.p1.plot(l2_vals, pen=b2_pen, name=f"BB_Lower2({bb_k2}σ)")

                self.computed_bb = {
                    "mid": mid_vals, "u1": u1_vals, "l1": l1_vals, "u2": u2_vals, "l2": l2_vals,
                    "k1": bb_k1, "k2": bb_k2
                }

        # 4. 計算與繪製副圖一 (Sub-Chart 1)
        sub1_type = self.indicator_config.get("sub1_type", "成交量 (Volume)")
        self._render_sub_chart(self.p2, sub1_type, df, is_sub1=True)

        # 5. 計算與繪製副圖二 (Sub-Chart 2)
        sub2_type = self.indicator_config.get("sub2_type", "MACD")
        self._render_sub_chart(self.p3, sub2_type, df, is_sub1=False)

        # 6. 預設視野縮放至近 1 年 (顯示 60 根精選 K 棒)
        self.set_view_range_months(12)

    def _render_sub_chart(self, plot_item: pg.PlotItem, indicator_name: str, df: pd.DataFrame, is_sub1: bool = True):
        """根據選擇之技術指標渲染副圖畫布 (支援 Volume, MACD, KDJ, RSI, KD, WR, BIAS, ATR, DMI, CCI)"""
        plot_item.setLabel('left', indicator_name.split()[0], color='#A0AAB8')
        s_close = df['close']
        s_open = df['open']
        s_high = df['high']
        s_low = df['low']
        s_vol = df['volume']
        n_bars = len(df)

        store_dict = {}

        if "成交量" in indicator_name or "Volume" in indicator_name:
            v_colors = ['#FF3B69' if c >= o else '#00E676' for o, c in zip(s_open, s_close)]
            vol_bars = pg.BarGraphItem(x=list(range(n_bars)), height=s_vol, y0=0, width=0.5, brushes=v_colors)
            plot_item.addItem(vol_bars)
            # 成交量均線 (MA5, MA10)
            if len(s_vol) >= 5:
                vma5 = list(s_vol.rolling(5).mean())
                plot_item.plot(vma5, pen=pg.mkPen('#FFD700', width=1.2), name="VMA5")
                store_dict["vma5"] = vma5
            if len(s_vol) >= 10:
                vma10 = list(s_vol.rolling(10).mean())
                plot_item.plot(vma10, pen=pg.mkPen('#00E5FF', width=1.2), name="VMA10")
                store_dict["vma10"] = vma10

        elif "MACD" in indicator_name:
            if len(s_close) >= 26:
                ema12 = s_close.ewm(span=12, adjust=False).mean()
                ema26 = s_close.ewm(span=26, adjust=False).mean()
                dif = ema12 - ema26
                dea = dif.ewm(span=9, adjust=False).mean()
                macd_bar = (dif - dea) * 2.0

                dif_vals, dea_vals, bar_vals = list(dif), list(dea), list(macd_bar)
                plot_item.plot(dif_vals, pen=pg.mkPen('#00E5FF', width=1.5), name='DIF')
                plot_item.plot(dea_vals, pen=pg.mkPen('#FF9800', width=1.5), name='DEA')

                m_colors = ['#FF3B69' if v >= 0 else '#00E676' for v in bar_vals]
                m_bars = pg.BarGraphItem(x=list(range(n_bars)), height=bar_vals, y0=0, width=0.5, brushes=m_colors)
                plot_item.addItem(m_bars)

                store_dict = {"dif": dif_vals, "dea": dea_vals, "bar": bar_vals}

        elif "KDJ" in indicator_name or "KD" in indicator_name:
            if len(s_close) >= 9:
                low_min = s_low.rolling(9).min()
                high_max = s_high.rolling(9).max()
                rsv = (s_close - low_min) / (high_max - low_min).replace(0, np.nan) * 100.0
                rsv = rsv.fillna(50.0)
                k_ser = rsv.ewm(com=2, adjust=False).mean()
                d_ser = k_ser.ewm(com=2, adjust=False).mean()
                j_ser = 3.0 * k_ser - 2.0 * d_ser

                k_vals, d_vals, j_vals = list(k_ser), list(d_ser), list(j_ser)
                plot_item.plot(k_vals, pen=pg.mkPen('#FFD700', width=1.5), name='K')
                plot_item.plot(d_vals, pen=pg.mkPen('#00E5FF', width=1.5), name='D')
                if "KDJ" in indicator_name:
                    plot_item.plot(j_vals, pen=pg.mkPen('#E040FB', width=1.5), name='J')

                store_dict = {"k": k_vals, "d": d_vals, "j": j_vals}

        elif "RSI" in indicator_name:
            if len(s_close) >= 24:
                def _calc_rsi(series, period):
                    delta = series.diff()
                    gain = delta.clip(lower=0)
                    loss = -delta.clip(upper=0)
                    avg_g = gain.ewm(com=period-1, adjust=False).mean()
                    avg_l = loss.ewm(com=period-1, adjust=False).mean()
                    rs = avg_g / avg_l.replace(0, np.nan)
                    return (100.0 - (100.0 / (1.0 + rs))).fillna(50.0)

                rsi6 = list(_calc_rsi(s_close, 6))
                rsi12 = list(_calc_rsi(s_close, 12))
                rsi24 = list(_calc_rsi(s_close, 24))

                plot_item.plot(rsi6, pen=pg.mkPen('#FFD700', width=1.5), name='RSI6')
                plot_item.plot(rsi12, pen=pg.mkPen('#00E5FF', width=1.5), name='RSI12')
                plot_item.plot(rsi24, pen=pg.mkPen('#E040FB', width=1.5), name='RSI24')

                store_dict = {"rsi6": rsi6, "rsi12": rsi12, "rsi24": rsi24}

        elif "WR" in indicator_name or "威廉" in indicator_name:
            if len(s_close) >= 14:
                h14 = s_high.rolling(14).max()
                l14 = s_low.rolling(14).min()
                wr = (h14 - s_close) / (h14 - l14).replace(0, np.nan) * 100.0
                wr_vals = list(wr.fillna(0.0))
                plot_item.plot(wr_vals, pen=pg.mkPen('#00E5FF', width=1.5), name='WR14')
                store_dict = {"wr": wr_vals}

        elif "BIAS" in indicator_name or "乖離率" in indicator_name:
            if len(s_close) >= 24:
                b6 = list(((s_close - s_close.rolling(6).mean()) / s_close.rolling(6).mean() * 100.0).fillna(0.0))
                b12 = list(((s_close - s_close.rolling(12).mean()) / s_close.rolling(12).mean() * 100.0).fillna(0.0))
                b24 = list(((s_close - s_close.rolling(24).mean()) / s_close.rolling(24).mean() * 100.0).fillna(0.0))

                plot_item.plot(b6, pen=pg.mkPen('#FFD700', width=1.5), name='BIAS6')
                plot_item.plot(b12, pen=pg.mkPen('#00E5FF', width=1.5), name='BIAS12')
                plot_item.plot(b24, pen=pg.mkPen('#E040FB', width=1.5), name='BIAS24')
                store_dict = {"bias6": b6, "bias12": b12, "bias24": b24}

        elif "ATR" in indicator_name or "真實區間" in indicator_name:
            if len(s_close) >= 14:
                prev_c = s_close.shift(1)
                tr = pd.concat([s_high - s_low, (s_high - prev_c).abs(), (s_low - prev_c).abs()], axis=1).max(axis=1)
                atr = list(tr.rolling(14).mean().fillna(0.0))
                plot_item.plot(atr, pen=pg.mkPen('#00E5FF', width=1.5), name='ATR14')
                store_dict = {"atr": atr}

        elif "CCI" in indicator_name:
            if len(s_close) >= 14:
                tp = (s_high + s_low + s_close) / 3.0
                ma_tp = tp.rolling(14).mean()
                md = (tp - ma_tp).abs().rolling(14).mean()
                cci = list(((tp - ma_tp) / (0.015 * md.replace(0, np.nan))).fillna(0.0))
                plot_item.plot(cci, pen=pg.mkPen('#FF9800', width=1.5), name='CCI14')
                store_dict = {"cci": cci}

        else:
            # 預設副圖降級顯示成交量
            v_colors = ['#FF3B69' if c >= o else '#00E676' for o, c in zip(s_open, s_close)]
            vol_bars = pg.BarGraphItem(x=list(range(n_bars)), height=s_vol, y0=0, width=0.5, brushes=v_colors)
            plot_item.addItem(vol_bars)

        if is_sub1:
            self.computed_sub1 = {"type": indicator_name, "data": store_dict}
        else:
            self.computed_sub2 = {"type": indicator_name, "data": store_dict}

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
        """游標懸停處理：X 軸精準吸附至 K 棒正中央 round(mouse_x) 並匯出所有指標數據」"""
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

            is_last_bar = (idx == len(self.kbars_data) - 1)
            if is_last_bar and self.ref_price > 0:
                base_price = self.ref_price
            elif idx > 0:
                base_price = self.kbars_data[idx - 1]['close']
            else:
                base_price = open_p
            change = close_p - base_price
            pct_change = (change / base_price * 100.0) if base_price != 0 else 0.0

            # 抓取該索引點上所有啟用的 MA 數值
            ma_snapshot = []
            for item in self.computed_ma:
                v_list = item["vals"]
                if idx < len(v_list) and not np.isnan(v_list[idx]):
                    ma_snapshot.append({
                        "name": item["name"],
                        "val": v_list[idx],
                        "color": item["color"]
                    })

            # 抓取布林通道數值
            bb_snapshot = {}
            if self.computed_bb:
                mid_l = self.computed_bb.get("mid", [])
                u1_l = self.computed_bb.get("u1", [])
                l1_l = self.computed_bb.get("l1", [])
                if idx < len(mid_l) and not np.isnan(mid_l[idx]):
                    bb_snapshot = {
                        "mid": mid_l[idx],
                        "u1": u1_l[idx] if idx < len(u1_l) else None,
                        "l1": l1_l[idx] if idx < len(l1_l) else None
                    }

            # 抓取副圖一數值
            sub1_snapshot = {"type": self.computed_sub1.get("type", ""), "vals": {}}
            d1 = self.computed_sub1.get("data", {})
            for k_key, v_arr in d1.items():
                if idx < len(v_arr) and not np.isnan(v_arr[idx]):
                    sub1_snapshot["vals"][k_key] = v_arr[idx]

            # 抓取副圖二數值
            sub2_snapshot = {"type": self.computed_sub2.get("type", ""), "vals": {}}
            d2 = self.computed_sub2.get("data", {})
            for k_key, v_arr in d2.items():
                if idx < len(v_arr) and not np.isnan(v_arr[idx]):
                    sub2_snapshot["vals"][k_key] = v_arr[idx]

            info = {
                "datetime": kb['datetime'],
                "open": open_p,
                "high": high_p,
                "low": low_p,
                "close": close_p,
                "change": change,
                "pct_change": pct_change,
                "volume": vol,
                "ma_list": ma_snapshot,
                "bb_info": bb_snapshot,
                "sub1_info": sub1_snapshot,
                "sub2_info": sub2_snapshot
            }
            self.hover_kbar_signal.emit(info)
