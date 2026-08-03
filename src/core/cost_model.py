# -*- coding: utf-8 -*-
"""
core/cost_model.py — 台股/台期貨交易成本模型 (移植自 StockBuild)
"""

STOCK_FEE_RATE = 0.001425      # 券商手續費率 (單邊)
STOCK_FEE_DISCOUNT = 1.0       # 折扣
STOCK_FEE_MIN = 20.0           # 單筆最低手續費 (整股)
ODD_FEE_MIN = 1.0              # 零股單筆最低手續費
STOCK_TAX_RATE = 0.003         # 證交稅 (賣出)
ETF_TAX_RATE = 0.001           # ETF 證交稅 (賣出)
FUT_FEE_PER_LOT = 50.0         # 期貨手續費 (單邊每口)
FUT_TAX_RATE = 0.00002         # 期交稅 (十萬分之二)


def is_etf(symbol):
    s = str(symbol or '').strip().upper()
    return s.startswith('00') and len(s) >= 4


def _p(params, key, default):
    if not params:
        return default
    v = params.get(key)
    return default if v is None else v


def side_cost(trade_type, symbol, price, qty, contract_size, is_sell, params=None):
    price = abs(float(price)); qty = int(qty); contract_size = float(contract_size)
    amount = price * qty * contract_size
    if trade_type in ('期貨', 'future'):
        fee = _p(params, 'fut_fee_per_lot', FUT_FEE_PER_LOT) * qty
        tax = amount * _p(params, 'fut_tax_rate', FUT_TAX_RATE)
        return float(fee), float(tax)

    rate = _p(params, 'stock_fee_rate', STOCK_FEE_RATE) * _p(params, 'fee_discount', STOCK_FEE_DISCOUNT)
    fee = amount * rate
    fee_min = _p(params, 'odd_fee_min', ODD_FEE_MIN) if trade_type == '零股' \
        else _p(params, 'stock_fee_min', STOCK_FEE_MIN)
    if amount > 0:
        fee = max(fee, float(fee_min))
    tax = 0.0
    if is_sell:
        tax_rate = _p(params, 'etf_tax_rate', ETF_TAX_RATE) if is_etf(symbol) \
            else _p(params, 'stock_tax_rate', STOCK_TAX_RATE)
        tax = amount * tax_rate
    return float(fee), float(tax)


def round_trip_cost(trade_type, symbol, entry_price, exit_price, qty, contract_size,
                    direction='做多', params=None):
    entry_is_sell = (direction in ('做空', 'SHORT'))
    e_fee, e_tax = side_cost(trade_type, symbol, entry_price, qty, contract_size,
                             entry_is_sell, params)
    x_fee, x_tax = side_cost(trade_type, symbol, exit_price, qty, contract_size,
                             not entry_is_sell, params)
    return {
        'entry_fee': e_fee, 'exit_fee': x_fee,
        'fee': e_fee + x_fee,
        'tax': e_tax + x_tax,
        'total': e_fee + x_fee + e_tax + x_tax,
    }


def describe(trade_type, params=None):
    if trade_type in ('期貨', 'future'):
        return (f"期貨:手續費 {_p(params,'fut_fee_per_lot',FUT_FEE_PER_LOT):g} 元/口(單邊)"
                f" + 期交稅 {_p(params,'fut_tax_rate',FUT_TAX_RATE)*100:.3f}%(買賣皆收)")
    disc = _p(params, 'fee_discount', STOCK_FEE_DISCOUNT)
    rate = _p(params, 'stock_fee_rate', STOCK_FEE_RATE)
    return (f"{trade_type}:手續費 {rate*100:.4f}%×{disc:g}折(單邊,最低"
            f"{_p(params,'odd_fee_min',ODD_FEE_MIN) if trade_type=='零股' else _p(params,'stock_fee_min',STOCK_FEE_MIN):g}元)"
            f" + 證交稅 {_p(params,'stock_tax_rate',STOCK_TAX_RATE)*100:.2f}%(賣出;ETF {ETF_TAX_RATE*100:.2f}%)")
