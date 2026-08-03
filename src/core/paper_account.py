# -*- coding: utf-8 -*-
"""
core/paper_account.py — 內建虛擬模擬帳戶 (紙上交易記帳與部位對帳引擎，移植自 StockBuild)
"""
import uuid

STOCK_FEE_RATE = 0.001425     # 券商手續費 (單邊)
STOCK_TAX_RATE = 0.003        # 證交稅 (賣出)
FUTURES_FEE_PER_LOT = 50.0    # 期貨手續費估計 (單邊每口)
FUTURES_MULTIPLIER = {'TXF': 200.0, 'MXF': 50.0, 'TMF': 10.0}

DEFAULT_ACCOUNT_ID = 'default'


def new_account(initial_cash=1000000.0, name='預設模擬帳戶', account_id=None):
    return {
        'id': account_id or uuid.uuid4().hex[:10],
        'name': str(name or '').strip() or '未命名帳戶',
        'initial_cash': float(initial_cash),
        'cash': float(initial_cash),
        'positions': {},   # key=symbol -> {market, direction(多/空), qty, avg_price, mark_price}
        'history': [],     # 每筆:{ts, symbol, market, action, kind, qty, price, fee, pnl, note}
        'realized_pnl': 0.0,
    }


def _fut_multiplier(symbol):
    sym = str(symbol).upper()
    for prefix, mult in FUTURES_MULTIPLIER.items():
        if sym.startswith(prefix):
            return mult, ''
    return 1.0, '(未知期貨乘數，以 1 計)'


def apply_fill(acct, ts, market, symbol, action, kind, qty, price, trade_type=None):
    qty = int(qty)
    price = float(price)
    sym = str(symbol).upper()
    note = ''
    fee = 0.0
    pnl = 0.0
    pos = acct['positions'].get(sym)
    share_per_unit = 1 if trade_type == '零股' else 1000

    if market in ('台股', '股票', '零股'):
        gross = price * share_per_unit * qty
        if action == '買進':
            fee = gross * STOCK_FEE_RATE
            acct['cash'] -= (gross + fee)
        else:
            fee = gross * STOCK_FEE_RATE + gross * STOCK_TAX_RATE
            acct['cash'] += (gross - fee)
    else:  # 台期貨 / 期貨
        mult, note = _fut_multiplier(sym)
        fee = FUTURES_FEE_PER_LOT * qty
        acct['cash'] -= fee

    if kind == 'OPEN':
        direction = '多' if action == '買進' else '空'
        if pos and pos.get('direction') == direction:
            total = pos['qty'] + qty
            pos['avg_price'] = (pos['avg_price'] * pos['qty'] + price * qty) / total
            pos['qty'] = total
        else:
            acct['positions'][sym] = {'market': market, 'direction': direction,
                                       'qty': qty, 'avg_price': price, 'mark_price': price,
                                       'share_per_unit': share_per_unit}
    else:  # CLOSE
        if pos:
            close_qty = min(qty, pos['qty'])
            d_mult = 1.0 if pos['direction'] == '多' else -1.0
            diff = (price - pos['avg_price']) * d_mult
            if market in ('台股', '股票', '零股'):
                spu = pos.get('share_per_unit', share_per_unit)
                pnl = diff * spu * close_qty - fee
            else:
                mult, note = _fut_multiplier(sym)
                pnl = diff * mult * close_qty - fee
                acct['cash'] += diff * mult * close_qty
            acct['realized_pnl'] += pnl
            pos['qty'] -= close_qty
            if pos['qty'] <= 0:
                acct['positions'].pop(sym, None)
        else:
            note = (note + ' 無對應持倉的平倉 (忽略部位)').strip()

    rec = {'ts': str(ts), 'symbol': sym, 'market': market, 'action': action,
           'kind': kind, 'qty': qty, 'price': price, 'fee': round(fee, 2),
           'pnl': round(pnl, 2), 'note': note}
    acct['history'].append(rec)
    return rec


def mark_price(acct, symbol, price):
    pos = acct['positions'].get(str(symbol).upper())
    if pos:
        pos['mark_price'] = float(price)


def unrealized_pnl(acct):
    total = 0.0
    for sym, pos in acct['positions'].items():
        qty = pos['qty']
        avg = pos['avg_price']
        mark = pos.get('mark_price', avg)
        d_mult = 1.0 if pos['direction'] == '多' else -1.0
        diff = (mark - avg) * d_mult
        if pos['market'] in ('台股', '股票', '零股'):
            spu = pos.get('share_per_unit', 1000)
            total += diff * spu * qty
        else:
            mult, _ = _fut_multiplier(sym)
            total += diff * mult * qty
    return round(total, 2)


def equity(acct):
    return round(acct['cash'] + unrealized_pnl(acct), 2)
