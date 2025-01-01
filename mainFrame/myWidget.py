"""
自定义控件
可关闭的选项卡控件

@File     : myWidget.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/3/9 12:57
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/9 12:57        1.0             None
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTabWidget


class MyQTab(QTabWidget):
    # 自定义关闭信号
    close_tab_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyQTab, self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        self.widget(index).deleteLater()
        self.removeTab(index)
        # 发送信号
        # noinspection PyUnresolvedReferences
        self.close_tab_signal.emit(index)
