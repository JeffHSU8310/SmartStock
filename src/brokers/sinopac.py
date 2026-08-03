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
