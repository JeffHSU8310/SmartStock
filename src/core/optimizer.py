# -*- coding: utf-8 -*-
"""
core/optimizer.py — 策略參數網格搜尋與最佳化器 (移植自 StockBuild)
"""
import copy
import itertools

from core import backtest as _backtest


def parse_param_spec(spec):
    text = str(spec or '').strip()
    if not text:
        raise ValueError("參數範圍不可空白，例如: fast=5,7,10; slow=20,25,30")
    grid = {}
    for part in text.replace('\n', ';').split(';'):
        part = part.strip()
        if not part:
            continue
        if '=' not in part:
            raise ValueError(f"參數格式錯誤 (缺少 =): {part}")
        name, vals = part.split('=', 1)
        name = name.strip()
        vals = vals.strip()
        if ':' in vals:
            nums = [float(x) for x in vals.split(':')]
            start, stop = nums[0], nums[1]
            step = nums[2] if len(nums) == 3 else 1.0
            out, cur = [], start
            while (cur < stop) if step > 0 else (cur > stop):
                out.append(_num(cur))
                cur += step
            grid[name] = out
        else:
            items = [v.strip() for v in vals.split(',') if v.strip()]
            grid[name] = [_num(v) for v in items]
    return grid


def _num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return v
    return int(f) if abs(f - int(f)) < 1e-12 else f


def run_grid_search(strategy, df, spec_text, objective='淨損益', min_trades=1, max_combos=500):
    grid = parse_param_spec(spec_text)
    names = list(grid.keys())
    combos = [dict(zip(names, c)) for c in itertools.product(*[grid[n] for n in names])][:max_combos]

    results = []
    for combo in combos:
        s = copy.deepcopy(strategy)
        params = dict(s.get('custom_params') or {})
        params.update(combo)
        s['custom_params'] = params
        r = _backtest.run_backtest(s, df)
        m = r['metrics']
        results.append({
            'params': combo,
            'metrics': m,
            'score': m.get('total_pnl', 0.0)
        })

    results.sort(key=lambda x: x['score'], reverse=True)
    return {
        'best': results[0] if results else None,
        'results': results,
        'total_evaluated': len(results)
    }
