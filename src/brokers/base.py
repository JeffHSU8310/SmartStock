# -*- coding: utf-8 -*-
"""
brokers/base.py — 券商 adapter 共用介面 (移植自 StockBuild)
"""

class BrokerClient:
    """所有券商 adapter 的共用基底類別。"""

    name = "base"
    display_name = "未命名券商"

    def __init__(self):
        self.api = None
        self.logged_in = False

    def new_session(self):
        raise NotImplementedError

    def login(self, **credentials):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError

    def list_positions(self):
        """回傳 [(symbol, 買賣別, 股數/口數, 成本均價, 市價/參考價, 未實現損益), ...];未登入回空 list。"""
        return []

    def build_order(self, order_intent):
        raise NotImplementedError

    def place_order(self, contract, order_intent):
        raise NotImplementedError

    def list_accounts(self):
        return []

    def account_object(self, account_id):
        return None
