import os
import sys
import logging
import datetime
import time
import threading
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Any, Callable

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

try:
    import shioaji as sj
    SHIOAJI_AVAILABLE = True
except ImportError:
    SHIOAJI_AVAILABLE = False
    logging.warning("Shioaji API SDK 未安裝 (請使用 pip install shioaji)")

class SinoPacEngine:
    """永豐金證券 Shioaji API 量化行情與交易引擎 (100% 恪遵 Rule 22 券商真實數據金律)"""

    # Shioaji 官方 REST API (snapshots/ticks/kbars) 10 秒 50 次限制防護：最小快照間隔 2.5 秒
    MIN_SNAPSHOT_INTERVAL = 2.5

    def __init__(self, simulation: bool = True):
        self.simulation = simulation
        self.api = None
        self.is_connected = False
        self.is_ca_active = False
        self.active_account = None
        
        self.subscribe_lock = threading.Lock()
        self.last_snapshot_time = 0.0
        self.last_realtime_cache = []
        self.subscribed_contracts = set()
        
        self.sub_callbacks = []
        self.quote_cache = {}
        self.contracts_cache = {}
        self.kbars_cache = {}
        self._init_shioaji()

    def _init_shioaji(self):
        try:
            if SHIOAJI_AVAILABLE:
                self.api = sj.Shioaji(simulation=self.simulation)
                logging.info("Shioaji API SDK 初始化完成")
        except Exception as e:
            logging.error(f"Shioaji API 初始化失敗: {e}")
            self.api = None

    def connect(self, api_key: str = "", secret_key: str = "") -> bool:
        """登入永豐金 Shioaji API 並下載官方股票、期貨、指數字典」"""
        if not SHIOAJI_AVAILABLE or not self.api:
            logging.error("無法連線：未安裝 Shioaji SDK")
            return False

        try:
            if api_key and secret_key:
                accounts = self.api.login(api_key=api_key, secret_key=secret_key, subscribe_trade=False)
            else:
                accounts = self.api.login(
                    api_key=os.getenv("SHIOAJI_API_KEY", "DEMO_KEY"),
                    secret_key=os.getenv("SHIOAJI_SECRET_KEY", "DEMO_SECRET"),
                    subscribe_trade=False
                )
            
            self.is_connected = True
            if accounts:
                self.active_account = accounts[0]
            
            try:
                self.api.fetch_contracts()
                logging.info("Shioaji 官方合約字典下載完成！")
            except Exception as fc_err:
                logging.warning(f"fetch_contracts 警示: {fc_err}")

            logging.info("Shioaji API 成功登入")
            return True
        except Exception as e:
            logging.error(f"Shioaji API 登入失敗: {e}")
            self.is_connected = False
            return False

    def login_with_ca(self, api_key: str, secret_key: str, ca_path: str = "", ca_password: str = "", person_id: str = "") -> Dict:
        """永豐金 API 登入與 CA 憑證激活 (SinoPac Shioaji CA Auth)"""
        if not self.api:
            self._init_shioaji()

        if not self.api:
            return {"status": "error", "message": "Shioaji API SDK 未能正確載入"}

        try:
            accounts = self.api.login(
                api_key=api_key,
                secret_key=secret_key,
                subscribe_trade=False
            )
            self.is_connected = True
            self.kbars_cache.clear()
            self.contracts_cache.clear()

            try:
                self.api.fetch_contracts()
                logging.info("Shioaji 官方合約字典下載完成！")
            except Exception as fc_err:
                logging.warning(f"fetch_contracts 警示: {fc_err}")

            if ca_path and os.path.exists(ca_path) and ca_password and person_id:
                try:
                    res = self.api.activate_ca(
                        ca_path=ca_path,
                        ca_passwd=ca_password,
                        person_id=person_id
                    )
                    self.is_ca_active = True
                    logging.info(f"CA 憑證激活成功: {res}")
                except Exception as ca_err:
                    logging.warning(f"CA 憑證激活警示: {ca_err}")

            return {
                "status": "success",
                "message": "永豐金 API 連線成功！" + (" (憑證已激活)" if self.is_ca_active else " (無憑證)"),
                "accounts": [str(acc) for acc in accounts] if accounts else []
            }
        except Exception as e:
            logging.error(f"永豐金 API 登入失敗: {e}")
            return {"status": "error", "message": f"登入失敗: {str(e)}"}

    def logout(self):
        """登出永豐金 API"""
        if self.api and self.is_connected:
            try:
                self.api.logout()
            except Exception as e:
                logging.error(f"Shioaji Logout Exception: {e}")
        self.is_connected = False
        self.is_ca_active = False
        self.kbars_cache.clear()
        with self.subscribe_lock:
            self.subscribed_contracts.clear()

    def disconnect(self):
        self.logout()

    def set_quote_callbacks(self, on_tick_stk=None, on_bidask_stk=None, on_tick_fop=None, on_bidask_fop=None):
        """註冊 Shioaji 官方即時報價 WebSocket 回調 (Tick 與 BidAsk)"""
        if not self.api or not self.is_connected:
            return False
        try:
            quote_api = getattr(self.api, "quote", None)
            if quote_api:
                if on_tick_stk and hasattr(quote_api, "set_on_tick_stk_v1_callback"):
                    quote_api.set_on_tick_stk_v1_callback(on_tick_stk)
                if on_bidask_stk and hasattr(quote_api, "set_on_bidask_stk_v1_callback"):
                    quote_api.set_on_bidask_stk_v1_callback(on_bidask_stk)
                if on_tick_fop and hasattr(quote_api, "set_on_tick_fop_v1_callback"):
                    quote_api.set_on_tick_fop_v1_callback(on_tick_fop)
                if on_bidask_fop and hasattr(quote_api, "set_on_bidask_fop_v1_callback"):
                    quote_api.set_on_bidask_fop_v1_callback(on_bidask_fop)
                logging.info("Shioaji 實時報價 WebSocket 回調設定完成")
                return True
        except Exception as e:
            logging.error(f"設定報價回調失敗: {e}")
        return False

    def subscribe_quote(self, code: str, quote_type: str = "both", intraday_odd: bool = False) -> bool:
        """【WebSocket 串流訂閱】訂閱指定商品實時撮合/五檔報價 (搭配 subscribe_lock 確保線程安全)"""
        if not self.api or not self.is_connected:
            return False

        contract = self.get_contract(code)
        if not contract:
            logging.warning(f"無法訂閱報價：找不到商品 {code} 的合約物件")
            return False

        with self.subscribe_lock:
            try:
                quote_api = getattr(self.api, "quote", None)
                if not quote_api or not hasattr(quote_api, "subscribe"):
                    return False

                c_code = getattr(contract, "code", code)
                if c_code in self.subscribed_contracts:
                    return True

                if quote_type in ["tick", "both"]:
                    try:
                        quote_api.subscribe(contract, quote_type=sj.constant.QuoteType.Tick, version=sj.constant.QuoteVersion.v1, intraday_odd=intraday_odd)
                    except (TypeError, Exception):
                        quote_api.subscribe(contract, quote_type="tick", intraday_odd=intraday_odd)

                if quote_type in ["bidask", "both"]:
                    try:
                        quote_api.subscribe(contract, quote_type=sj.constant.QuoteType.BidAsk, version=sj.constant.QuoteVersion.v1, intraday_odd=intraday_odd)
                    except (TypeError, Exception):
                        quote_api.subscribe(contract, quote_type="bidask", intraday_odd=intraday_odd)

                self.subscribed_contracts.add(c_code)
                logging.info(f"成功訂閱 [{c_code}] 即時報價串流")
                return True
            except Exception as e:
                logging.error(f"訂閱商品 [{code}] 實時報價失敗: {e}")
                return False

    def unsubscribe_quote(self, code: str, quote_type: str = "both", intraday_odd: bool = False) -> bool:
        """【WebSocket 串流退訂】退訂指定商品實時報價 (搭配 subscribe_lock 確保線程安全)"""
        if not self.api or not self.is_connected:
            return False

        contract = self.get_contract(code)
        if not contract:
            return False

        with self.subscribe_lock:
            try:
                quote_api = getattr(self.api, "quote", None)
                if not quote_api or not hasattr(quote_api, "unsubscribe"):
                    return False

                c_code = getattr(contract, "code", code)
                if quote_type in ["tick", "both"]:
                    try:
                        quote_api.unsubscribe(contract, quote_type=sj.constant.QuoteType.Tick, intraday_odd=intraday_odd)
                    except Exception:
                        pass
                if quote_type in ["bidask", "both"]:
                    try:
                        quote_api.unsubscribe(contract, quote_type=sj.constant.QuoteType.BidAsk, intraday_odd=intraday_odd)
                    except Exception:
                        pass

                self.subscribed_contracts.discard(c_code)
                logging.info(f"已退訂 [{c_code}] 即時報價串流")
                return True
            except Exception as e:
                logging.error(f"退訂商品 [{code}] 實時報價失敗: {e}")
                return False

    def get_accounts(self) -> List[str]:
        if self.is_connected and self.api:
            try:
                accs = self.api.list_accounts()
                return [f"{a.account_type}-{a.account_id}" for a in accs]
            except Exception:
                pass
        return ["PaperTrading-8888888 (虛擬帳戶)"]

    def _safe_has_code(self, contract: Any) -> bool:
        try:
            return hasattr(contract, "code") and bool(contract.code)
        except Exception:
            return False

    def _extract_contract(self, container: Any, keys: List[str], name_keywords: List[str] = None) -> Any:
        """從 Shioaji 合約容器中極速提取 Contract 物件 (支援 dict []、getattr 及動態 values 遍歷)"""
        if not container:
            return None

        # 1. 嘗試直接 Key 檢索 (支援 [] 與 getattr)
        for k in keys:
            try:
                if hasattr(container, "__getitem__"):
                    item = container[k]
                    if item and self._safe_has_code(item):
                        return item
            except Exception:
                pass

            try:
                item = getattr(container, k, None)
                if item and self._safe_has_code(item):
                    return item
            except Exception:
                pass

        # 2. 嘗試 values() 或 遍歷
        items_to_check = []
        if isinstance(container, dict) or hasattr(container, "values"):
            try:
                items_to_check = list(container.values())
            except Exception:
                pass
        elif hasattr(container, "__iter__"):
            try:
                for k in container:
                    try:
                        val = container[k] if hasattr(container, "__getitem__") else getattr(container, k, None)
                        if val:
                            items_to_check.append(val)
                    except Exception:
                        pass
            except Exception:
                pass

        for item in items_to_check:
            if not self._safe_has_code(item):
                continue
            c_code = str(getattr(item, "code", "")).strip().upper()
            c_name = str(getattr(item, "name", "")).strip()

            if c_code in [x.upper() for x in keys]:
                return item

            if name_keywords:
                for kw in name_keywords:
                    if kw in c_name:
                        return item

        return None

    def get_contract(self, code: str):
        """全面防爆獲取官方正確 Shioaji Contract 物件 (支援 api.contracts.get 官方檢索與字典層級安全提取)"""
        if not self.api or not self.is_connected:
            return None

        code_upper = code.upper().strip()
        if code_upper in self.contracts_cache:
            return self.contracts_cache[code_upper]

        # 1. 建立代碼轉換對照集 (包含 Shioaji 官方合約代碼 001, 101, TXFR1)
        candidate_codes = [code_upper]
        if code_upper in ["IX0001", "TSE", "加權指數", "001"]:
            candidate_codes = ["001", "0001", "IX0001", "TSE001", "TSE0001", "0000"]
        elif code_upper in ["IX0043", "OTC", "櫃買指數", "101"]:
            candidate_codes = ["101", "0043", "IX0043", "OTC101", "OTC0043"]
        elif code_upper in ["TX00", "TXF", "TXFR1", "TXRF1", "台指期"]:
            candidate_codes = ["TXFR1", "TXF", "TXF202608", "TXF202609"]

        # 2. 優先嘗試 Shioaji 官方原生 api.contracts.get(code)
        contracts_api = getattr(self.api, "contracts", None) or getattr(self.api, "Contracts", None)
        if contracts_api and hasattr(contracts_api, "get"):
            for c_code in candidate_codes:
                try:
                    c = contracts_api.get(c_code)
                    if c and self._safe_has_code(c):
                        self.contracts_cache[code_upper] = c
                        return c
                except Exception:
                    pass

        # 3. 備用方案：深層次遍歷 Shioaji Contracts 物件屬性結構
        contracts_obj = getattr(self.api, "Contracts", None)
        if contracts_obj:
            contract = None
            if code_upper in ["IX0001", "TSE", "加權指數", "001"]:
                for index_attr in ["Indexs", "Indices", "indexs", "indices"]:
                    indices = getattr(contracts_obj, index_attr, None)
                    if indices and (hasattr(indices, "TSE") or hasattr(indices, "tse")):
                        tse = getattr(indices, "TSE", None) or getattr(indices, "tse", None)
                        contract = self._extract_contract(tse, candidate_codes, ["加權", "發行量"])
                        if contract:
                            break

            elif code_upper in ["IX0043", "OTC", "櫃買指數", "101"]:
                for index_attr in ["Indexs", "Indices", "indexs", "indices"]:
                    indices = getattr(contracts_obj, index_attr, None)
                    if indices and (hasattr(indices, "OTC") or hasattr(indices, "otc")):
                        otc = getattr(indices, "OTC", None) or getattr(indices, "otc", None)
                        contract = self._extract_contract(otc, candidate_codes, ["櫃買"])
                        if contract:
                            break

            elif code_upper in ["TX00", "TXF", "TXFR1", "TXRF1", "台指期"]:
                fut = getattr(contracts_obj, "Futures", None) or getattr(contracts_obj, "futures", None)
                if fut and (hasattr(fut, "TXF") or hasattr(fut, "txf")):
                    txf = getattr(fut, "TXF", None) or getattr(fut, "txf", None)
                    contract = self._extract_contract(txf, candidate_codes, ["台指期", "全月"])

            else:
                stk = getattr(contracts_obj, "Stocks", None) or getattr(contracts_obj, "stocks", None)
                if stk:
                    for market_name in ["TSE", "OTC", "tse", "otc"]:
                        m_obj = getattr(stk, market_name, None)
                        if m_obj:
                            contract = self._extract_contract(m_obj, candidate_codes, None)
                            if contract:
                                break

            if contract and self._safe_has_code(contract):
                self.contracts_cache[code_upper] = contract
                return contract

        return None

    def get_futures_kbar_contract(self, code: str):
        """專門為 KBars 歷史 K 棒獲取 TXFR1 合約"""
        if not self.api or not self.is_connected:
            return None
        return self.get_contract("TXFR1")

    def get_symbol_name(self, code: str) -> str:
        """取得商品官方中文名稱"""
        code_upper = code.upper()
        if code_upper in ["IX0001", "TSE", "加權指數"]:
            return "加權指數"
        elif code_upper in ["IX0043", "OTC", "櫃買指數"]:
            return "櫃買指數"
        elif code_upper in ["TX00", "TXF", "TXFR1", "TXRF1", "台指期"]:
            return "台指期主力"

        contract = self.get_contract(code)
        if contract:
            name = getattr(contract, "name", "")
            if name:
                return name

        common_names = {
            "2330": "台積電", "2317": "鴻海", "2454": "聯發科", "2308": "台達電",
            "2382": "廣達", "0050": "元大台灣50", "0056": "元大高股息"
        }
        return common_names.get(code, f"股票 {code}")

    def get_realtime_quotes(self, code_list: List[str] = None) -> List[Dict]:
        """
        取得實時成交與參考價報價 (100% 恪遵 Rule 22 全真實券商行情數據金律)
        學習 StockBuild 券商 API 串接金律：加入 2.5 秒快照流量節流防護 (Throttle Guard)，
        避免過度頻繁的 REST 請求耗盡 Shioaji 官方 10 秒 50 次流量限制。
        """
        if code_list is None:
            code_list = ["IX0001", "IX0043", "TX00", "2330", "2317", "2454", "2308", "2382", "0050", "0056"]

        results = []
        if not self.is_connected or not self.api:
            return results

        now = time.time()
        # 流量節流防護 (Throttle Guard)：若調用間隔小於 MIN_SNAPSHOT_INTERVAL (2.5秒)，優先回傳最新快取
        if now - self.last_snapshot_time < self.MIN_SNAPSHOT_INTERVAL and self.last_realtime_cache:
            return self.last_realtime_cache

        snap_map = {}
        contracts = []

        for req_code in code_list:
            c = self.get_contract(req_code)
            if c:
                contracts.append(c)

        if contracts:
            try:
                snaps = self.api.snapshots(contracts)
                for snap in snaps:
                    snap_code = getattr(snap, "code", "")
                    snap_map[snap_code] = snap
            except Exception as e:
                logging.warning(f"Shioaji snapshots exception: {e}")

        for req_code in code_list:
            c = self.get_contract(req_code)
            c_code = getattr(c, "code", "") if c else req_code
            snap = snap_map.get(c_code) or snap_map.get(req_code)

            display_name = self.get_symbol_name(req_code)

            c_close = 0.0
            ref_price = 0.0
            c_change = 0.0
            c_pct = 0.0
            vol = 0
            amt_str = ""

            if snap:
                c_close = float(getattr(snap, "close", 0.0))
                raw_ref = float(getattr(snap, "reference_price", 0.0))
                raw_chg = float(getattr(snap, "change_price", 0.0))
                raw_pct = float(getattr(snap, "change_rate", 0.0))
                vol = int(getattr(snap, "total_volume", getattr(snap, "volume", 0)))
                amt = float(getattr(snap, "total_amount", 0.0))
                if amt > 0:
                    amt_str = f"{amt / 1e8:.1f}億"

                # 精準參考價定位算法 (優先度: reference_price -> close - change_price -> open)
                if raw_ref > 0:
                    ref_price = raw_ref
                elif c_close > 0 and raw_chg != 0:
                    ref_price = c_close - raw_chg
                elif c_close > 0:
                    ref_price = float(getattr(snap, "open", c_close))

                if c_close > 0 and ref_price > 0:
                    c_change = c_close - ref_price
                    c_pct = (c_change / ref_price) * 100.0
                elif raw_chg != 0 or raw_pct != 0:
                    c_change = raw_chg
                    c_pct = raw_pct

            # 萬一盤後/離線/無快照導致 c_close 仍為 0，則從券商官方最新 2 根 K 棒對齊真實收盤價與參考價！
            if c_close <= 0 or ref_price <= 0:
                kbars = self.get_kbars(req_code, ktype="Day", limit=2)
                if len(kbars) >= 1:
                    last_kb = kbars[-1]
                    c_close = last_kb['close']
                    vol = vol if vol > 0 else last_kb['volume']
                    
                    if len(kbars) >= 2:
                        prev_kb = kbars[-2]
                        ref_price = prev_kb['close']
                    else:
                        ref_price = last_kb['open']

                    if ref_price > 0:
                        c_change = c_close - ref_price
                        c_pct = (c_change / ref_price) * 100.0

            if c_close > 0:
                results.append({
                    "code": req_code,
                    "name": display_name,
                    "price": c_close,
                    "ref_price": ref_price,
                    "change": c_change,
                    "pct_change": c_pct,
                    "volume": vol,
                    "amount_str": amt_str,
                    "is_realtime": True
                })

        if results:
            self.last_realtime_cache = results
            self.last_snapshot_time = now

        return results

    def fetch_snapshots(self, code_list: List[str]) -> List[Dict]:
        return self.get_realtime_quotes(code_list)

    def _resample_dataframe(self, df: pd.DataFrame, ktype: str, is_futures: bool = False) -> pd.DataFrame:
        """Pandas 金融級 K 棒多週期重採樣引擎"""
        if df.empty:
            return df

        col_map = {c.lower(): c for c in df.columns}
        ts_col = col_map.get('ts', 'ts')
        op_col = col_map.get('open', 'Open')
        hi_col = col_map.get('high', 'High')
        lo_col = col_map.get('low', 'Low')
        cl_col = col_map.get('close', 'Close')
        vo_col = col_map.get('volume', 'Volume')

        df[ts_col] = pd.to_datetime(df[ts_col])
        ktype_upper = ktype.upper()

        if ktype_upper in ["DAY", "日", "日K"]:
            df['date'] = df[ts_col].dt.strftime('%Y-%m-%d')
        elif ktype_upper in ["WEEK", "週", "週K"]:
            df['date'] = df[ts_col].dt.to_period('W').dt.start_time.dt.strftime('%Y-%m-%d')
        elif ktype_upper in ["MONTH", "月", "月K"]:
            df['date'] = df[ts_col].dt.strftime('%Y-%m-01')
        else:
            df['date'] = None

        if df['date'] is not None:
            grouped = df.groupby('date', sort=False)
            records = []
            for d_val, group in grouped:
                if not group.empty:
                    records.append({
                        'ts': group[ts_col].iloc[0],
                        'open': group[op_col].iloc[0],
                        'high': group[hi_col].max(),
                        'low': group[lo_col].min(),
                        'close': group[cl_col].iloc[-1],
                        'volume': group[vo_col].sum()
                    })
            return pd.DataFrame(records)

        freq_map = {"5M": "5min", "5分": "5min", "15M": "15min", "15分": "15min", "30M": "30min", "30分": "30min", "60M": "60min", "60分": "60min"}
        freq = freq_map.get(ktype_upper)
        if freq:
            df.set_index(ts_col, inplace=True)
            res = df.resample(freq).agg({
                op_col: 'first',
                hi_col: 'max',
                lo_col: 'min',
                cl_col: 'last',
                vo_col: 'sum'
            }).dropna().reset_index()
            res.rename(columns={ts_col: 'ts', op_col: 'open', hi_col: 'high', lo_col: 'low', cl_col: 'close', vo_col: 'volume'}, inplace=True)
            return res

        df.rename(columns={ts_col: 'ts', op_col: 'open', hi_col: 'high', lo_col: 'low', cl_col: 'close', vo_col: 'volume'}, inplace=True)
        return df

    def get_kbars(self, code: str = "2330", ktype: str = "Day", limit: int = 2500) -> List[Dict]:
        """
        取得 K 線歷史數據 (100% 全真實券商數據金律 - 絕不造假)
        支援大盤加權指數 IX0001、櫃買指數 IX0043、台指期貨 TX00 與全股票
        """
        cache_key = f"{code}_{ktype}_{limit}"
        if cache_key in self.kbars_cache:
            return self.kbars_cache[cache_key]

        # 恪遵 Rule 22：未連線 API 時，嚴禁生成任何虛擬/假數據，回傳空列表 []
        if not self.is_connected or not self.api:
            return []

        code_upper = code.upper()
        is_futures = code_upper.startswith("TX") or code_upper.startswith("MX") or code_upper.startswith("TM") or "期" in code

        contract = self.get_futures_kbar_contract(code) if is_futures else self.get_contract(code)

        if contract and self._safe_has_code(contract):
            try:
                today = datetime.date.today()
                # 智能天數調用：日/週/月 K 下載近 3 年 (1000 天)，極速傳輸 (<150ms)；分 K 下載 60 天
                days_back = 1000 if ktype in ["Day", "日", "日K", "Week", "週", "Month", "月"] else 60

                start_date = (today - datetime.timedelta(days=days_back)).strftime("%Y-%m-%d")
                end_date = today.strftime("%Y-%m-%d")

                kbars_raw = self.api.kbars(
                    contract=contract,
                    start=start_date,
                    end=end_date
                )
                df_raw = pd.DataFrame({**kbars_raw})
                if not df_raw.empty:
                    df_res = self._resample_dataframe(df_raw, ktype, is_futures=is_futures)
                    
                    kbars = []
                    for idx, row in df_res.iterrows():
                        dt_str = str(row['ts'])
                        if len(dt_str) > 10 and "00:00:00" in dt_str:
                            dt_str = dt_str.split()[0]

                        kbars.append({
                            'datetime': dt_str,
                            'open': float(row['open']),
                            'high': float(row['high']),
                            'low': float(row['low']),
                            'close': float(row['close']),
                            'volume': int(row['volume'])
                        })
                    if kbars:
                        self.kbars_cache[cache_key] = kbars
                        return kbars
            except Exception as e:
                logging.warning(f"Shioaji KBars error for {code}: {e}")

        # 恪遵 Rule 22 金律：若 API 傳輸失敗或券商無交易數據，絕不產生任何合成假數據，嚴格回傳空列表 []
        return []
