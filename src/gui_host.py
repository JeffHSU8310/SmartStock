import os
import sys
import webview

def main():
    # 取得當前軟體目錄路徑
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'gui', 'index.html')

    if not os.path.exists(html_path):
        # 打包發布後的相對路徑適配
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        html_path = os.path.join(base_dir, 'gui', 'index.html')

    # 建立純原生 100% 獨立 Windows 桌面應用軟體視窗 (無 CMD 控制台，無瀏覽器頁籤)
    window = webview.create_window(
        title='台灣智慧機器人選股與回測系統 TaiwanSmartQuant v4.0 Native GUI',
        url=f'file:///{html_path}',
        width=1440,
        height=900,
        resizable=True,
        min_size=(1024, 720),
        background_color='#07090E'
    )

    # 啟動原生視窗引擎
    webview.start(debug=False)

if __name__ == '__main__':
    main()
