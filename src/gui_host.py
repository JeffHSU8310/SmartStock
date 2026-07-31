import os
import sys
import json
import webview
from sinopac_engine import SinoPacEngine

class ApiBridge:
    def __init__(self, window=None):
        self.window = window
        self.engine = SinoPacEngine()

    def set_window(self, window):
        self.window = window

    def login_sinopac(self, config_str):
        """
        供 JavaScript 呼叫之永豐金 API 登入接口
        """
        try:
            if isinstance(config_str, str):
                data = json.loads(config_str)
            else:
                data = config_str
                
            person_id = data.get("person_id", "")
            api_key = data.get("api_key", "")
            secret_key = data.get("secret_key", "")
            ca_path = data.get("ca_path", "")
            ca_passwd = data.get("ca_passwd", "")

            result = self.engine.login_with_ca(
                person_id=person_id,
                api_key=api_key,
                secret_key=secret_key,
                ca_path=ca_path,
                ca_passwd=ca_passwd
            )
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"橋接呼叫失敗: {str(e)}"
            }, ensure_ascii=False)

    def select_pfx_file(self):
        """
        開啟 Windows 原生檔案選擇視窗，挑選 .pfx 憑證檔案
        """
        if self.window:
            result = self.window.create_file_dialog(
                dialog_type=webview.OPEN_DIALOG,
                file_types=('PFX Certificate (*.pfx)', 'All files (*.*)')
            )
            if result and len(result) > 0:
                return result[0]
        return ""

def main():
    # 獲取軟體專案根目錄
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'gui', 'index.html')

    if not os.path.exists(html_path):
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        html_path = os.path.join(base_dir, 'gui', 'index.html')

    api_bridge = ApiBridge()

    # 開啟 100% 純正獨立 Windows 桌面應用程式視窗 (無 CMD 黑框、無瀏覽器頁籤)
    window = webview.create_window(
        title='台灣智慧機器人選股與回測系統 TaiwanSmartQuant v6.0.5 Native GUI',
        url=f'file:///{html_path}',
        width=1480,
        height=920,
        resizable=True,
        min_size=(1024, 720),
        background_color='#07090E',
        js_api=api_bridge
    )

    api_bridge.set_window(window)
    webview.start(debug=False)

if __name__ == '__main__':
    main()
