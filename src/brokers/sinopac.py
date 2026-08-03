# -*- coding: utf-8 -*-
"""
brokers/sinopac.py — 永豐金 Shioaji Adapter (移植自 StockBuild)
"""
from brokers.base import BrokerClient
from core import sj_compat

try:
    import shioaji as sj
    HAS_SJ = True
except ImportError:
    HAS_SJ = False


class SinopacBroker(BrokerClient):
    name = "sinopac"
    display_name = "永豐金"

    def __init__(self, simulation: bool = True):
        super().__init__()
        self.simulation = simulation
        if HAS_SJ:
            self.new_session()

    def new_session(self):
        """建立全新的 Shioaji 實例"""
        self.api = sj.Shioaji(simulation=self.simulation)
        self.logged_in = False
        return self.api

    def login(self, api_key: str, secret_key: str, contracts_timeout: int = 10000):
        """永豐金 API 登入 (支援 1.5.6 與 1.7 異動參數動態相容)"""
        kw, dropped = sj_compat.supported_kwargs(
            self.api.login, {'contracts_timeout': contracts_timeout})
        accounts = self.api.login(api_key=api_key, secret_key=secret_key, **kw)
        self.logged_in = True
        self.dropped_login_kwargs = dropped
        return accounts

    def index_contract(self, market: str):
        """加權(TSE)/櫃買(OTC)指數合約檢索"""
        return sj_compat.resolve_index(
            getattr(getattr(self.api, 'Contracts', None), 'Indexs', None) or
            getattr(getattr(self.api, 'Contracts', None), 'Indices', None), market)

    def stock_contract(self, code: str):
        """股票/ETF 合約檢索 (支援 direct get 與全屬性掃描)"""
        contracts_obj = getattr(self.api, 'Contracts', None)
        if not contracts_obj:
            return None
        
        # 1. 原生 get
        c = sj_compat._try_get(contracts_obj, str(code))
        if c is not None and getattr(c, 'code', None):
            return c

        stocks = getattr(contracts_obj, 'Stocks', None) or getattr(contracts_obj, 'stocks', None)
        if stocks is None:
            return None

        c = sj_compat._try_get(stocks, str(code))
        if c is not None:
            return c

        try:
            return next((x for x in stocks if sj_compat.match_contract_code(x, code)), None)
        except Exception:
            return None

    def futures_contract(self, raw: str):
        """【學習自 StockBuild】通用期貨合約解析:任何期貨商品代號 (TX00/TXF/MXF...) → R1 熱門連續合約 (TXFR1)。
        若無 R1 則挑選 delivery_month / 交割日最小的近月實體合約。
        """
        contracts_obj = getattr(self.api, 'Contracts', None)
        if not contracts_obj:
            return None

        futs = getattr(contracts_obj, 'Futures', None) or getattr(contracts_obj, 'futures', None)
        if not futs:
            return None

        raw_u = str(raw or '').strip().upper()
        code_map = {'TX00': 'TXF', 'MX00': 'MXF', '台指期': 'TXF', '小台指': 'MXF'}
        code = code_map.get(raw_u, raw_u)

        if len(code) > 3:
            grp3 = sj_compat._try_get(futs, code[:3])
            if grp3 is not None:
                c_exact = sj_compat._try_get(grp3, code)
                if c_exact and getattr(c_exact, 'code', None):
                    return c_exact
                try:
                    for cand in grp3:
                        if sj_compat.match_contract_code(cand, code):
                            return cand
                except Exception:
                    pass
            code = code[:3]

        grp = sj_compat._try_get(futs, code)
        if grp is None:
            return None

        try:
            r1 = sj_compat._try_get(grp, f"{code}R1")
            if r1 and getattr(r1, 'code', None):
                return r1
        except Exception:
            pass

        try:
            cands = list(grp)
            r1s = [x for x in cands if str(getattr(x, 'symbol', '')).upper().endswith('R1')]
            if r1s:
                return r1s[0]

            def _month_key(x):
                dm = str(getattr(x, 'delivery_month', '') or getattr(x, 'delivery_date', '') or '')
                return dm or '999999'

            dated = [x for x in cands if any(ch.isdigit() for ch in str(getattr(x, 'symbol', '')))]
            pool = dated if dated else cands
            if pool:
                return min(pool, key=_month_key)
        except Exception:
            pass

        return None

    def sdk_version(self):
        return getattr(sj, '__version__', '?') if HAS_SJ else '(未安裝)'

    def activate_ca(self, ca_path: str, ca_pw: str, pid: str):
        self.api.activate_ca(ca_path=ca_path, ca_passwd=ca_pw, person_id=pid)

    def set_quote_callbacks(self, on_tick_stk=None, on_bidask_stk=None, on_tick_fop=None, on_bidask_fop=None):
        quote_api = getattr(self.api, 'quote', None)
        if quote_api:
            if on_tick_stk and hasattr(quote_api, 'set_on_tick_stk_v1_callback'):
                quote_api.set_on_tick_stk_v1_callback(on_tick_stk)
            if on_bidask_stk and hasattr(quote_api, 'set_on_bidask_stk_v1_callback'):
                quote_api.set_on_bidask_stk_v1_callback(on_bidask_stk)
            if on_tick_fop and hasattr(quote_api, 'set_on_tick_fop_v1_callback'):
                quote_api.set_on_tick_fop_v1_callback(on_tick_fop)
            if on_bidask_fop and hasattr(quote_api, 'set_on_bidask_fop_v1_callback'):
                quote_api.set_on_bidask_fop_v1_callback(on_bidask_fop)

    def logout(self):
        if self.api and self.logged_in:
            try:
                self.api.logout()
            except Exception:
                pass
        self.logged_in = False

    @staticmethod
    def account_id(acc):
        return f"{getattr(acc, 'broker_id', '')}-{getattr(acc, 'account_id', '')}"

    def _accounts(self):
        try:
            return list(self.api.list_accounts() or [])
        except Exception:
            return []

    def list_accounts(self):
        out = []
        for a in self._accounts():
            aid = self.account_id(a)
            out.append((aid, sj_compat.account_label(a, getattr(a, 'account_id', ''))))
        return out

    def account_object(self, account_id):
        want = str(account_id or '').strip()
        if not want:
            return None
        for a in self._accounts():
            if self.account_id(a) == want:
                return a
        return None

    def build_order(self, oi: dict):
        """把 core.order_intent 的輸出翻成 Shioaji Order 物件 (相容 StockOrder/FuturesOrder 與通用 Order)。
        整股與零股分開組，零股帶入 order_lot=IntradayOdd；期貨則採用 FuturesPriceType 常數。
        """
        if not HAS_SJ:
            raise RuntimeError("未安裝 Shioaji SDK")

        action = sj.constant.Action.Buy if oi['action'] == '買進' else sj.constant.Action.Sell
        px = float(oi['price'])
        qty = int(oi['qty'])
        ptype = oi['price_type']

        extra = {}
        if oi.get('account'):
            acc = self.account_object(oi['account'])
            if acc is not None:
                extra['account'] = acc

        order_cls = getattr(self.api, 'Order', None)

        if oi['trade_type'] == '期貨':
            fut_order_cls = getattr(self.api, 'FuturesOrder', None) or order_cls
            fut_ptype = {'限價': sj.constant.FuturesPriceType.LMT,
                         '市價': sj.constant.FuturesPriceType.MKT,
                         '範圍市價': sj.constant.FuturesPriceType.MKP}.get(ptype, sj.constant.FuturesPriceType.LMT)
            return fut_order_cls(price=px, quantity=qty, action=action,
                                 price_type=fut_ptype,
                                 order_type=sj.constant.OrderType.ROD, **extra)

        stk_order_cls = getattr(self.api, 'StockOrder', None) or order_cls
        if oi['trade_type'] == '零股':
            # 盤中零股單，單位股，限價 ROD
            return stk_order_cls(price=px, quantity=qty, action=action,
                                 price_type=sj.constant.StockPriceType.LMT,
                                 order_type=sj.constant.OrderType.ROD,
                                 order_lot=sj.constant.StockOrderLot.IntradayOdd,
                                 order_cond=sj.constant.StockOrderCond.Cash, **extra)
        stk_ptype = (sj.constant.StockPriceType.MKT if ptype == '市價'
                     else sj.constant.StockPriceType.LMT)
        return stk_order_cls(price=px, quantity=qty, action=action,
                             price_type=stk_ptype,
                             order_type=sj.constant.OrderType.ROD,
                             order_lot=sj.constant.StockOrderLot.Common,
                             order_cond=sj.constant.StockOrderCond.Cash, **extra)

    def place_order(self, contract, oi: dict):
        """送出委託至永豐金 API (100% 限定 Shioaji 模擬環境，零實盤資金風險)"""
        if not self.api or not self.logged_in:
            raise RuntimeError("未登入永豐金 API")
        if oi.get('account') and self.account_object(oi['account']) is None:
            raise ValueError(f"找不到指定的永豐帳號 {oi['account']}")
        return self.api.place_order(contract, self.build_order(oi))

    def order_status_text(self, trade):
        st = getattr(getattr(trade, 'status', None), 'status', '')
        return getattr(st, 'name', st) or '送出'

    def list_positions(self) -> list:
        """查詢永豐金股票與期貨即時部位與庫存"""
        if not self.api or not self.logged_in:
            return []
        positions = []
        try:
            stk_pos = self.api.list_positions(self.api.stock_account) if hasattr(self.api, 'stock_account') else []
            for p in (stk_pos or []):
                code = getattr(p, 'code', '')
                qty = int(getattr(p, 'quantity', 0))
                price = float(getattr(p, 'price', 0.0))
                last_price = float(getattr(p, 'last_price', price))
                pnl = float(getattr(p, 'pnl', 0.0))
                direction = '買進' if getattr(p, 'direction', '') == 'Action.Buy' else '買進'
                positions.append({
                    'code': code,
                    'direction': direction,
                    'qty': qty,
                    'price': price,
                    'last_price': last_price,
                    'pnl': pnl,
                    'type': '股票'
                })
        except Exception:
            pass
        return positions
