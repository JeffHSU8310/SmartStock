# -*- coding: utf-8 -*-
"""
core/market_screener.py — 全市場多因子選股引擎 (移植自 StockBuild)
"""
import pandas as pd

OP_GTE = '>='
OP_LTE = '<='
OPS = (OP_GTE, OP_LTE)

FUNDAMENTAL_FIELDS = {
    'pe':          ('pe', '本益比', '倍', 15.0),
    'pb':          ('pb', '股價淨值比', '倍', 1.5),
    'yield':       ('yield', '殖利率', '%', 5.0),
    'eps':         ('eps', '每股盈餘 EPS', '元', 1.0),
    'gross_margin': ('gross_margin', '毛利率', '%', 20.0),
    'revenue_yoy': ('revenue_yoy', '月營收年增率', '%', 10.0),
    'revenue_mom': ('revenue_mom', '月營收月增率', '%', 0.0),
    'roe':         ('roe', 'ROE (推算)', '%', 10.0),
    'close':       ('close', '股價', '元', 100.0),
}


def _text(v, default=''):
    if v is None:
        return default
    try:
        if pd.isna(v):
            return default
    except (TypeError, ValueError):
        pass
    s = str(v).strip()
    return s if s and s.lower() != 'nan' else default


def fundamental_label(cond):
    meta = FUNDAMENTAL_FIELDS.get(cond.get('field'))
    if not meta:
        return f"未知基本面條件 {cond.get('field')}"
    _col, label, unit, _dv = meta
    return f"{label} {cond.get('op', OP_GTE)} {cond.get('value')} {unit}"


def eval_fundamental(row, conds):
    for c in (conds or []):
        meta = FUNDAMENTAL_FIELDS.get(c.get('field'))
        if not meta:
            return False, f"未知條件 {c.get('field')}"
        col = meta[0]
        val = row.get(col)
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return False, f"{meta[1]} 無資料"
        try:
            thr = float(c.get('value'))
            v = float(val)
        except (TypeError, ValueError):
            return False, f"{meta[1]} 門檻或數值格式錯誤"
        if c.get('op', OP_GTE) == OP_GTE:
            if not (v >= thr):
                return False, f"{meta[1]} {v:g} < {thr:g}"
        else:
            if not (v <= thr):
                return False, f"{meta[1]} {v:g} > {thr:g}"
    return True, ''
