# -*- coding: utf-8 -*-
"""
core/tick_rules.py — 台股/期貨跳動單位 (tick) 規則與價格格式化 (恪遵 Rule 19 TWSE 升降單位雙軌權威規定)
"""

def get_tick(price: float, asset_type: str, raw_symbol: str) -> float:
    """
    回傳台股/期貨在該價格下的合法跳動單位。
    恪遵 Rule 19：
    1. ETF 專屬特規：未滿 50 元 ➔ 0.01 元；50 元以上 ➔ 0.05 元。
    2. 一般股票官方級距：未滿 10 元 ➔ 0.01 | 10~50 ➔ 0.05 | 50~100 ➔ 0.10 | 100~500 ➔ 0.50 | 500~1000 ➔ 1.00 | 1000 元以上 ➔ 5.00 元！
    """
    if asset_type in ("future", "期貨"):
        return 1.0
    elif asset_type in ("stock", "index_tw", "股票", "零股", "指數"):
        p = float(price)
        sym = raw_symbol.replace('.TW', '').replace('.TWO', '').strip()
        if sym.startswith('00'):
            if p < 50:
                return 0.01
            else:
                return 0.05
        else:
            if p < 10:
                return 0.01
            elif p < 50:
                return 0.05
            elif p < 100:
                return 0.1
            elif p < 500:
                return 0.5
            elif p < 1000:
                return 1.0
            else:
                return 5.0
    return 0.01


def fmt_price(price, asset_type: str, raw_symbol: str) -> str:
    try:
        p = float(price)
        t = get_tick(p, asset_type, raw_symbol)
        if t >= 1:
            return f"{p:.0f}"
        if t in (0.5, 0.1):
            return f"{p:.1f}"
        return f"{p:.2f}"
    except Exception:
        return "--"


def round_to_tick(price: float, asset_type: str, raw_symbol: str) -> float:
    try:
        p = float(price)
    except (TypeError, ValueError):
        return price

    tick = get_tick(p, asset_type, raw_symbol)
    if tick <= 0:
        return p
    rounded = round(round(p / tick) * tick, 4)

    tick2 = get_tick(rounded, asset_type, raw_symbol)
    if tick2 != tick:
        rounded = round(round(rounded / tick2) * tick2, 4)

    return rounded
