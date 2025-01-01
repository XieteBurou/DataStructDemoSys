"""
@File     : new_array_buttons.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/3/15 21:40
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/15 21:40        1.0             None
"""
from PyQt5.QtCore import pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QLabel, QSpinBox, QLineEdit, QPushButton, QGridLayout
from numpy.random import randint


class NewArrayButton(QDialog):
    linked_list_signal = pyqtSignal(list)

    def __init__(self, arr=None, max_length=10, max_value=100, min_value=1):
        super(NewArrayButton, self).__init__()
        if arr is None:
            arr = []
        self.min_value = min_value
        self.max_length = max_length
        self.max_value = max_value
        self.arr = arr
        self.label = QLabel()
        self.spin = QSpinBox()
        self.line_edit = QLineEdit()
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('创建链表')
        self.resize(260, 190)

        self.label.setText(str(self.arr))
        button_1 = QPushButton('随机创建链表')
        button_2 = QPushButton('随机指定长度')
        button_3 = QPushButton('自定义创建')
        button_4 = QPushButton('确定')
        button_5 = QPushButton('清空')
        button_6 = QPushButton('取消')

        button_1.clicked.connect(self.__click_bt1)
        button_2.clicked.connect(self.__click_bt2)
        button_3.clicked.connect(self.__click_bt3)
        button_4.clicked.connect(self.__click_bt4)
        button_5.clicked.connect(self.__click_bt5)
        button_6.clicked.connect(self.__click_bt6)

        self.spin.setValue(randint(3, self.max_length))
        self.spin.setMinimum(1)
        self.spin.setMaximum(self.max_length)

        validator = QRegExpValidator()
        validator.setRegExp(QRegExp('^\d[ 0-9]*$'))
        self.line_edit.setValidator(validator)
        self.line_edit.setPlaceholderText('%d个数以内, 并用空格隔开' % self.max_length)

        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 0, 1, 4)
        layout.addWidget(button_1, 1, 1, 1, 2)
        layout.addWidget(self.spin, 2, 0, 1, 1)
        layout.addWidget(button_2, 2, 1, 1, 2)
        layout.addWidget(self.line_edit, 3, 0, 1, 2)
        layout.addWidget(button_3, 3, 2, 1, 1)
        layout.addWidget(button_4, 4, 1, 1, 1)
        layout.addWidget(button_5, 1, 0, 1, 1)
        layout.addWidget(button_6, 4, 2, 1, 1)

    def __click_bt1(self):
        """
        随机创建链表

        :return: None
        """
        self.arr.clear()
        self.arr = list(randint(self.min_value, self.max_value, randint(4, self.max_length)))
        self.label.setText(str(self.arr))

    def __click_bt2(self):
        """
        随机指定长度

        :return:
        """
        k = int(self.spin.text())
        self.arr.clear()
        self.arr = list(randint(self.min_value, self.max_value, k))
        self.label.setText(str(self.arr))

    def __click_bt3(self):
        """
        自定义创建

        :return:
        """
        if len(self.line_edit.text()) == 0:
            self.label.setText('请输入数组，用空格隔开')
        else:
            self.arr = list(map(int, self.line_edit.text().split()))
            if len(self.arr) > self.max_length:
                self.arr.clear()
                self.label.setText('输入过多')
            elif max(self.arr) > self.max_value:
                self.arr.clear()
                self.label.setText('超出最大值限制')
            else:
                self.label.setText(str(self.arr))

    def __click_bt4(self):
        """
        确定按钮，向父程序发送数组信号，并关闭页面

        :return: None
        """
        # noinspection PyUnresolvedReferences
        self.linked_list_signal.emit(self.arr)
        self.close()

    def __click_bt5(self):
        """
        清空

        :return: None
        """
        self.arr.clear()
        self.label.setText(str(self.arr))

    def __click_bt6(self):
        """
        取消

        :return: None
        """
        self.close()
