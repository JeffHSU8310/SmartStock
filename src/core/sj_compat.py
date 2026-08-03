# -*- coding: utf-8 -*-
"""
core/sj_compat.py — shioaji 1.5.6 / 1.7 相容層 (移植自 StockBuild)
"""
import inspect

INDEX_CANDIDATES = {
    'TSE': ('IX0001', 'TSE001', '001'),                                  # 加權指數
    'OTC': ('IX0043', 'IX0101', 'IX0002', 'OTC101', 'OTC001', '101'),    # 櫃買指數
}

INDEX_SYMBOLS = frozenset({
    'TWII', 'TWOII', 'TSE', 'OTC',
    'TSE001', 'OTC101', 'OTC001',        # 1.5.6
    'IX0001', 'IX0043',                  # 1.7 (加權 / 櫃買)
    'IX0101', 'IX0002',                  # 1.7
})


def index_candidates(market):
    """某個市場的指數代碼候選 (由新到舊)。market: 'TSE' / 'OTC'。"""
    return INDEX_CANDIDATES.get(str(market or '').upper().strip(), ())


def _try_get(obj, key):
    if obj is None:
        return None
    getter = getattr(obj, 'get', None)
    if callable(getter):
        try:
            v = getter(key)
            if v is not None:
                return v
        except Exception:
            pass
    try:
        v = obj[key]
        if v is not None:
            return v
    except Exception:
        pass
    try:
        v = getattr(obj, key, None)
        if v is not None:
            return v
    except Exception:
        pass
    return None


def resolve_index(indexs, market):
    """從 `api.Contracts.Indexs` 取出指數合約。找不到回 None。"""
    codes = index_candidates(market)
    if not codes or indexs is None:
        return None
    for code in codes:
        c = _try_get(indexs, code)
        if c is not None and not _looks_like_group(c):
            return c
    group = _try_get(indexs, str(market).upper())
    if group is not None:
        for code in codes:
            c = _try_get(group, code)
            if c is not None and not _looks_like_group(c):
                return c
    return None


def _looks_like_group(obj):
    code = getattr(obj, 'code', None)
    return not isinstance(code, str)


def contract_symbol(contract, default=''):
    if contract is None:
        return default
    v = getattr(contract, 'symbol', None)
    if isinstance(v, str) and v:
        return v
    v = getattr(contract, 'code', None)
    if isinstance(v, str) and v:
        return v
    return default


def match_contract_code(contract, wanted):
    w = str(wanted or '').strip().upper()
    if not w:
        return False
    for attr in ('symbol', 'code'):
        v = getattr(contract, attr, None)
        if isinstance(v, str) and v.strip().upper() == w:
            return True
    return False


def supported_kwargs(func, desired):
    try:
        params = inspect.signature(func).parameters
    except (TypeError, ValueError):
        return dict(desired), []
    if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()):
        return dict(desired), []
    ok, dropped = {}, []
    for k, v in (desired or {}).items():
        if k in params:
            ok[k] = v
        else:
            dropped.append(k)
    return ok, dropped


ACCOUNT_KIND_ZH = {'Stock': '證券', 'Future': '期貨', 'Intl': '複委託'}


def account_kind(acc):
    at = getattr(acc, 'account_type', None)
    name = getattr(at, 'name', None) or (str(at) if at is not None else '')
    name = str(name or '').strip()
    if name and name.lower() not in ('none', ''):
        return name.split('.')[-1]
    cls = type(acc).__name__.replace('Account', '').strip()
    return cls


def account_label(acc, acc_id=''):
    kind = account_kind(acc)
    kind_zh = ACCOUNT_KIND_ZH.get(kind, kind or '未知類別')
    aid = str(acc_id or getattr(acc, 'account_id', '') or '').strip()
    user = str(getattr(acc, 'username', '') or '').strip()
    parts = [f'{kind_zh} {aid}'.strip()]
    if user:
        parts.append(user)
    if getattr(acc, 'signed', None) is False:
        parts.append('⚠未簽署')
    return '｜'.join(parts)
