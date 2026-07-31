import os
import sys
import webview

def main():
    # 獲取軟體專案根目錄
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'gui', 'index.html')

    if not os.path.exists(html_path):
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        html_path = os.path.join(base_dir, 'gui', 'index.html')

    # 開啟 100% 純正獨立 Windows 桌面應用程式視窗 (無 CMD 黑框、無瀏覽器頁籤)
    window = webview.create_window(
        title='台灣智慧機器人選股與回測系統 TaiwanSmartQuant v5.0 Native GUI',
        url=f'file:///{html_path}',
        width=1480,
        height=920,
        resizable=True,
        min_size=(1024, 720),
        background_color='#07090E'
    )

    webview.start(debug=False)

if __name__ == '__main__':
    main()
