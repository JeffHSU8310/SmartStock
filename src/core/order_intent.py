# -*- coding: utf-8 -*-
"""
core/order_intent.py — 券商中立的「委託意圖」(移植自 StockBuild)
"""
from core import tick_rules

ACTIONS = ('買進', '賣出')
TRADE_TYPES = ('股票', '零股', '期貨')
PRICE_TYPES = ('限價', '市價', '範圍市價')

TIF_ROD = 'ROD'
LOT_COMMON = '整股'
LOT_ODD = '零股'
COND_CASH = '現股'

DEFAULT_BROKER = 'sinopac'


def broker_of(strategy):
    return str((strategy or {}).get('broker', '') or '').strip() or DEFAULT_BROKER


def account_of(strategy):
    v = str((strategy or {}).get('broker_account', '') or '').strip()
    return v or None


def describe_target(strategy, broker_label=None, account_label=None):
    b = broker_label or broker_of(strategy)
    a = account_label or account_of(strategy) or '預設帳號'
    return f"{b} / {a}"


def apply_slippage(base_price, action, ticks, asset_type, symbol):
    base = float(base_price)
    tick = tick_rules.get_tick(base, asset_type, symbol)
    n = int(ticks or 0)
    px = base + n * tick if action == '買進' else base - n * tick
    return round(round(px / tick) * tick, 4), tick


def build_live_order(strategy, intent, asset_type, exec_price=None):
    sym = str(strategy.get('symbol', '')).upper()
    qty = int(intent['qty'])
    action = intent['action']
    base_px = float(exec_price) if exec_price is not None else float(intent['price'])
    ticks = int(strategy.get('slippage_ticks', 2) or 0)
    px, tick = apply_slippage(base_px, action, ticks, asset_type, sym)

    tt = strategy.get('trade_type', '股票')
    ptype = strategy.get('price_type', '限價')

    if tt == '零股':
        ptype = '限價'
    is_lmt = (ptype == '限價')

    return {
        'symbol': sym,
        'action': action,
        'qty': qty,
        'trade_type': tt,
        'price_type': ptype,
        'price': px if is_lmt else 0.0,
        'limit_price': px,
        'tick': tick,
        'time_in_force': TIF_ROD,
        'order_lot': LOT_ODD if tt == '零股' else LOT_COMMON,
        'order_cond': COND_CASH,
        'price_label': f"限價{px:g}" if is_lmt else ptype,
        'broker': broker_of(strategy),
        'account': account_of(strategy),
    }


def describe(order_intent):
    oi = order_intent or {}
    return (f"{oi.get('action', '?')} {oi.get('symbol', '?')} "
            f"{oi.get('qty', 0)} ({oi.get('trade_type', '?')}) "
            f"{oi.get('price_label', '?')}")
