# -*- coding: utf-8 -*-
"""
SmartStock 啟動入口
"""
import sys
import os

# 將 src 納入路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == '__main__':
    from gui_host_qt import main
    main()
