# -*- coding: utf-8 -*-
"""
core/custom_strategy.py — 量化自訂策略執行器 (移植自 StockBuild)
"""
import pandas as pd

class StrategyError(Exception):
    pass


class Ctx:
    """傳給量化策略 on_bar 的環境物件。"""

    BUY = 'BUY'
    SELL = 'SELL'
    CLOSE = 'CLOSE'
    HOLD = 'HOLD'

    def __init__(self, df, position, params=None, state=None, entry_price=0.0, bars_in_position=0, full_df=None):
        self.df = df
        self.position = position
        self._params = params or {}
        self.param_reads = {}
        self.state = state if isinstance(state, dict) else {}
        self.entry_price = float(entry_price or 0.0)
        self.bars_in_position = int(bars_in_position or 0)
        self._logs = []
        self.full_df = full_df if full_df is not None else df

    def log(self, msg):
        if len(self._logs) < 5:
            self._logs.append(str(msg)[:200])

    @property
    def close(self):
        return float(self.df['Close'].iloc[-1]) if 'Close' in self.df else float(self.df['close'].iloc[-1])

    @property
    def open(self):
        return float(self.df['Open'].iloc[-1]) if 'Open' in self.df else float(self.df['open'].iloc[-1])

    @property
    def high(self):
        return float(self.df['High'].iloc[-1]) if 'High' in self.df else float(self.df['high'].iloc[-1])

    @property
    def low(self):
        return float(self.df['Low'].iloc[-1]) if 'Low' in self.df else float(self.df['low'].iloc[-1])

    @property
    def volume(self):
        col = 'Volume' if 'Volume' in self.df else ('volume' if 'volume' in self.df else None)
        return float(self.df[col].iloc[-1]) if col else 0.0

    @property
    def time(self):
        return self.df.index[-1]

    def param(self, key, default=None):
        hit = key in self._params
        val = self._params.get(key, default)
        self.param_reads[key] = {'value': val, 'from_params': hit, 'default': default}
        return val

    def sma(self, n=20):
        col = 'Close' if 'Close' in self.df else 'close'
        return float(self.df[col].rolling(int(n)).mean().iloc[-1])

    def ema(self, n=20):
        col = 'Close' if 'Close' in self.df else 'close'
        return float(self.df[col].ewm(span=int(n), adjust=False).mean().iloc[-1])

    def buy(self):
        return self.BUY

    def sell(self):
        return self.SELL

    def close_position(self):
        return self.CLOSE

    def hold(self):
        return self.HOLD
