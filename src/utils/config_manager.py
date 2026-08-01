import os
import json
import logging

class ConfigManager:
    """本地配置管理員 (負責安全讀寫 API Key 與憑證設定，保護隱私資訊)"""
    CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config.json")

    @classmethod
    def load_config(cls) -> dict:
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"讀取 config.json 失敗: {e}")
        return {
            "remember": False,
            "person_id": "",
            "api_key": "",
            "secret_key": "",
            "ca_path": "",
            "ca_password": ""
        }

    @classmethod
    def save_config(cls, config_data: dict):
        try:
            with open(cls.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            logging.info("config.json 成功寫入")
        except Exception as e:
            logging.error(f"寫入 config.json 失敗: {e}")

    @classmethod
    def clear_config(cls):
        if os.path.exists(cls.CONFIG_FILE):
            try:
                os.remove(cls.CONFIG_FILE)
            except Exception as e:
                logging.error(f"清除 config.json 失敗: {e}")
