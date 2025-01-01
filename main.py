"""
@File     : main.py
@Project  : 数据结构与算法可视化演示系统
@Time     : 2022/3/5 14:09
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/5 14:09        1.0             None
"""

import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from mainFrame.mainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./images/icon.ico'))
    main = MainWindow()
    sys.exit(app.exec_())
