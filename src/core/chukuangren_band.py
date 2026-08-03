# -*- coding: utf-8 -*-
"""
core/chukuangren_band.py — 楚狂人「終極波段策略」引擎 (移植自 StockBuild)
"""
import pandas as pd

PARAM_KEYS = ('x', 'y', 'z', 's1', 's2', 'c', 'f')
MERGED_STOP_PAIRS = (('z', 'y'), ('s2', 's1'))

LONG_PARAM_KEYS = ('x', 'y', 'c', 'f')
SHORT_PARAM_KEYS = ('x', 's1', 'c', 'f')

KIND = 'chukuangren_band'
STRATEGY_NAME = '終極波段策略'
DIRECTIONS = ('做多', '做空')

NOON_CONFIRM_HOUR = 12
NOON_CONFIRM_END_MINUTE = 5


def in_noon_confirm_window(dt):
    if dt is None:
        return False
    try:
        return dt.hour == NOON_CONFIRM_HOUR and dt.minute < NOON_CONFIRM_END_MINUTE
    except AttributeError:
        return False


def param_keys_for(direction):
    return SHORT_PARAM_KEYS if direction == '做空' else LONG_PARAM_KEYS


def params_of(strategy):
    out = {}
    for k in PARAM_KEYS:
        try:
            out[k] = float(strategy.get(f'ck_{k}', 0) or 0)
        except (TypeError, ValueError):
            out[k] = 0.0
    for dst, src in MERGED_STOP_PAIRS:
        out[dst] = out[src]
    return out


def direction_of(strategy):
    d = strategy.get('direction')
    return d if d in DIRECTIONS else '做多'


def default_strategy():
    s = {
        'kind': KIND,
        'name': STRATEGY_NAME,
        'direction': '做多',
        'watch_enabled': True,
        'watch_symbol': '^TWII',
        'watch_trade_type': '指數',
        'watch_timeframe': '日K',
        'stop_loss_pct': 0.0,
        'take_profit_pct': 0.0,
        'stop_loss_abs': 0.0,
        'take_profit_abs': 0.0,
    }
    for k in PARAM_KEYS:
        s[f'ck_{k}'] = 0.0
    return s


def validate(strategy):
    if not str(strategy.get('name', '')).strip():
        return False, "策略名稱不可空白"
    if not str(strategy.get('symbol', '')).strip():
        return False, "執行商品 (做B) 代碼不可空白"
    direction = direction_of(strategy)
    try:
        q = int(strategy.get('qty', 0))
        if q <= 0:
            return False, "數量必須為正整數"
    except (TypeError, ValueError):
        return False, "數量必須為正整數"

    p = params_of(strategy)
    if p['x'] <= 0:
        return False, "進出場分界 X 必須是大於 0 的加權指數點位"
    if direction == '做多':
        if p['y'] <= 0:
            return False, "多單停損點位 Y 必須是大於 0 的加權指數點位"
    else:
        if p['s1'] <= 0:
            return False, "空單停損點位 S1 必須是大於 0 的加權指數點位"
    if p['c'] < 0 or p['f'] < 0:
        return False, "停利啟動門檻 C 與停利步幅 F 不可為負"
    return True, ""


def ensure_runtime(rt):
    rt.setdefault('pending_entry', None)
    rt.setdefault('pending_exit', None)
    rt.setdefault('trail_armed', False)
    rt.setdefault('trail_base', 0.0)
    rt.setdefault('sma20_mode', False)
    rt.setdefault('entry_index_price', 0.0)
    rt.setdefault('last_daily_bar_date', '')
    rt.setdefault('last_confirm_date', '')
    rt.setdefault('armed_intent', None)
    rt.setdefault('armed_at_ts', 0.0)
    return rt


def _position_of(rt):
    st = rt.get('state', 'FLAT')
    return st if st in ('LONG', 'SHORT') else 'FLAT'


def on_daily_close(params, rt, daily_df, direction='做多'):
    ensure_runtime(rt)
    if daily_df is None or len(daily_df) < 20:
        return rt
    today_date = str(daily_df.index[-1]).split(' ')[0]
    if rt.get('last_daily_bar_date') == today_date:
        return rt
    rt['last_daily_bar_date'] = today_date

    col = 'Close' if 'Close' in daily_df else 'close'
    close = float(daily_df[col].iloc[-1])
    sma20 = float(daily_df[col].rolling(20).mean().iloc[-1])
    position = _position_of(rt)
    X, Y, Z, S1, S2, C, F = (params[k] for k in ('x', 'y', 'z', 's1', 's2', 'c', 'f'))

    if position == 'FLAT':
        if rt.get('pending_entry') is None:
            if direction == '做多' and close > X:
                rt['pending_entry'] = {'dir': 'LONG', 'date': today_date}
            elif direction == '做空' and close < X:
                rt['pending_entry'] = {'dir': 'SHORT', 'date': today_date}
        return rt

    if rt.get('pending_exit') is not None:
        return rt

    entry_px = float(rt.get('entry_index_price', 0) or 0)
    if position == 'LONG':
        if close < Y:
            rt['pending_exit'] = {'reason': 'SL', 'date': today_date}
            return rt
        if rt.get('sma20_mode'):
            if not pd.isna(sma20) and close < sma20:
                rt['pending_exit'] = {'reason': 'TP_SMA20', 'date': today_date, 'sma20_ref': sma20}
            return rt
        profit = (close - entry_px) if entry_px > 0 else 0.0
        if entry_px > 0:
            if not rt.get('trail_armed') and profit > C:
                rt['trail_armed'] = True
                rt['trail_base'] = entry_px
            if rt.get('trail_armed') and F > 0:
                n = int((profit - C) // F)
                if n > 0:
                    candidate = entry_px + n * F
                    if candidate > rt.get('trail_base', entry_px):
                        rt['trail_base'] = candidate
            if rt.get('trail_armed') and close < rt.get('trail_base', entry_px):
                rt['pending_exit'] = {'reason': 'TP_POINT', 'date': today_date}
                return rt
        if profit > C and not pd.isna(sma20) and close > sma20:
            rt['sma20_mode'] = True
    else:  # SHORT
        if close > S1:
            rt['pending_exit'] = {'reason': 'SL', 'date': today_date}
            return rt
        if rt.get('sma20_mode'):
            if not pd.isna(sma20) and close > sma20:
                rt['pending_exit'] = {'reason': 'TP_SMA20', 'date': today_date, 'sma20_ref': sma20}
            return rt
        profit = (entry_px - close) if entry_px > 0 else 0.0
        if entry_px > 0:
            if not rt.get('trail_armed') and profit > C:
                rt['trail_armed'] = True
                rt['trail_base'] = entry_px
            if rt.get('trail_armed') and F > 0:
                n = int((profit - C) // F)
                if n > 0:
                    candidate = entry_px - n * F
                    if candidate < rt.get('trail_base', entry_px):
                        rt['trail_base'] = candidate
            if rt.get('trail_armed') and close > rt.get('trail_base', entry_px):
                rt['pending_exit'] = {'reason': 'TP_POINT', 'date': today_date}
                return rt
        if profit > C and not pd.isna(sma20) and close < sma20:
            rt['sma20_mode'] = True
    return rt
