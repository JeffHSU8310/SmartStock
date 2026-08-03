# -*- coding: utf-8 -*-
"""
core/order_rules.py — 台股/期貨委託送出與刪改前的本地風控驗證 (移植自 StockBuild)
"""

MODE_LABELS = {"Common": "整股", "IntradayOdd": "盤中零股", "Fixing": "盤後定價", "Odd": "盤後零股"}

MAX_QTY_LOT = 499     # 整股/盤後定價，單位：張
MAX_QTY_ODD = 999     # 盤中零股/盤後零股，單位：股


def validate_stock_order(mode: str, order_type_str: str, order_cond: str, order_type_tif: str, qty_str: str):
    """
    驗證台股委託是否符合交易所規則與本系統的數量上限。回傳 (ok: bool, reason: str)。
    """
    is_lot_restricted = mode in ("IntradayOdd", "Odd")
    label = MODE_LABELS.get(mode, mode)

    try:
        q = int(qty_str)
    except ValueError:
        unit = "股" if is_lot_restricted else "張"
        return False, f"數量請輸入有效整數 (單位:{unit})。"

    if is_lot_restricted:
        if not (1 <= q <= MAX_QTY_ODD):
            return False, f"{label}數量須為 1~{MAX_QTY_ODD} 股。"
    else:
        if not (1 <= q <= MAX_QTY_LOT):
            return False, f"{label}單筆委託數量須為 1~{MAX_QTY_LOT} 張。"

    if is_lot_restricted:
        if order_type_str == "市價":
            return False, f"{label}僅接受「限價」委託 (交易所規則)，請切換為限價。"
        if order_cond != "Cash":
            return False, f"{label}僅能現股交易，不可融資融券 (交易所規則)。"
        if order_type_tif != "ROD":
            return False, f"{label}僅能使用 ROD (交易所規則)。"

    if mode == "Fixing":
        if order_type_str == "市價":
            return False, "盤後定價沒有市價委託 (成交價固定為當日收盤價)。"
        if order_type_tif != "ROD":
            return False, "盤後定價僅能使用 ROD。"

    return True, ""


def is_daytrade_eligible(mode: str, order_cond: str, action: str, current_day_trade: bool) -> bool:
    return mode == "Common" and order_cond == "Cash" and action == "賣出" and bool(current_day_trade)


def _safe_int(v, default=0):
    try:
        return int(float(str(v).strip()))
    except (TypeError, ValueError):
        return default


def price_change_allowed(order_lot: str) -> bool:
    return order_lot == "Common"


def order_is_modifiable(status_display, current_qty, filled_qty):
    if "取消" in str(status_display):
        return False, "此委託已取消，無法再操作。"
    outstanding = _safe_int(current_qty) - _safe_int(filled_qty)
    if outstanding <= 0:
        return False, "此委託已全部成交，沒有未成交數量可刪改。"
    return True, ""


def validate_cancel(status_display, current_qty, filled_qty):
    return order_is_modifiable(status_display, current_qty, filled_qty)


def validate_qty_change(order_lot, status_display, current_qty, filled_qty, new_qty):
    ok, reason = order_is_modifiable(status_display, current_qty, filled_qty)
    if not ok:
        return ok, reason
    cur = _safe_int(current_qty)
    filled = _safe_int(filled_qty)
    unit = "股" if order_lot in ("IntradayOdd", "Odd") else "張"
    try:
        n = int(str(new_qty).strip())
    except (TypeError, ValueError):
        return False, f"新數量請輸入有效整數 (單位:{unit})。"
    if n >= cur:
        return False, f"改量只能減少：新數量須小於目前委託量 {cur}{unit}。"
    if n < 1:
        return False, f"新數量至少 1{unit}；若要全部取消請用「刪單」。"
    if n < filled:
        return False, f"新數量不可小於已成交量 {filled}{unit}。"
    return True, ""


def validate_price_change(order_lot, current_price, new_price):
    if not price_change_allowed(order_lot):
        label = MODE_LABELS.get(order_lot, order_lot)
        return False, f"{label}不可改價 (零股不可改價；盤後定價鎖定收盤價)。"
    try:
        np_ = float(new_price)
    except (TypeError, ValueError):
        return False, "新價格請輸入有效數字。"
    if np_ <= 0:
        return False, "新價格必須大於 0。"
    try:
        cp = float(current_price)
    except (TypeError, ValueError):
        cp = None
    if cp is not None and abs(np_ - cp) < 1e-9:
        return False, "新價格與原委託價相同，不需改價。"
    return True, ""
