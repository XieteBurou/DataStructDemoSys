"""
数据结构：栈

@File     : my_stack.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/3/11 19:39
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/11 19:39        1.0             None
"""

import random

from PyQt5.QtCore import QPropertyAnimation, QPoint
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QTextBrowser, QGridLayout, QPushButton, QVBoxLayout, QInputDialog, QMessageBox


class Stack(QWidget):
    width = 100
    height = 50
    space = 10
    left = 25
    top = 25
    fontSize = 15

    def __init__(self, parent=None):
        super(Stack, self).__init__(parent)

        # 栈数据
        self.stack = list()
        self.pop = list()
        # 绘图数据
        self.action_speed = 500
        self.ii = 0
        # 绘图区域
        self.draw_stack_area = QWidget()
        self.draw_pop_area = QWidget()
        self.text = QTextBrowser()

        self.__init_data()
        self.__init_ui()

    def __init_data(self):
        for i in self.pop:
            i.deleteLater()
        self.pop.clear()
        for j in self.stack:
            j.deleteLater()
        self.stack.clear()
        self.text.setText('栈结构\n')
        self.text.append('栈实现的是一种后进先出的策略，栈结构只有入栈和出栈两种操作，只能访问栈顶元素或取栈顶元素\n')
        self.text.append('class Stack:')
        self.text.append('    stack = int[11]      # 线性数组')
        self.text.append('    top = 0             # 栈顶下标')
        self.text.append('    def Push(self, x):')
        self.text.append('        self.top += 1')
        self.text.append('        self.stack[top] = x')
        self.text.append('    def POP(self):')
        self.text.append('        if self.top > 0:')
        self.text.append('            self.top = self.top - 1')
        self.text.append('            return self.stack[top+1]\n')

    def __init_ui(self):
        self.draw_stack_area.setMinimumSize(150, 600)
        self.draw_stack_area.setMaximumWidth(200)
        self.draw_pop_area.setMinimumSize(600, 150)
        self.draw_pop_area.setMaximumHeight(200)
        self.draw_stack_area.setStyleSheet(
            """
                QWidget {
                    border-left: 1px solid #D3D3D3;
                    border-right: 1px solid #D3D3D3;
                    border-bottom: 1px solid #D3D3D3;
                    background-color: rgb(238,238,238);
                }
            """
        )
        self.draw_pop_area.setStyleSheet(
            """
                QWidget {
                    border-top: 1px solid #D3D3D3;
                    border-bottom: 1px solid #D3D3D3;
                    background-color: rgb(238,238,238);
                }
            """
        )

        layout = QGridLayout(self)
        layout.addWidget(self.draw_stack_area, 0, 0, 2, 1)
        layout.addWidget(self.draw_pop_area, 0, 1, 1, 2)
        layout.addLayout(self.__set_control_layout(), 1, 1)
        layout.addWidget(self.text, 1, 2)

    def __set_control_layout(self):
        """
        创建控制布局

        :return:
        """

        button_1 = QPushButton('重置')
        button_2 = QPushButton('入栈')
        button_3 = QPushButton('出栈')
        button_4 = QPushButton('调整速度')

        button_1.clicked.connect(self.click_bt1)
        button_2.clicked.connect(self.click_bt2)
        button_3.clicked.connect(self.click_bt3)
        button_4.clicked.connect(self.click_bt4)

        layout = QVBoxLayout()
        layout.addWidget(button_1)
        layout.addWidget(button_2)
        layout.addWidget(button_3)
        layout.addWidget(button_4)
        layout.setContentsMargins(8, 50, 8, 50)

        return layout

    def click_bt1(self):
        self.__init_data()

    def click_bt2(self):
        if len(self.stack) > 11:
            QMessageBox.warning(self, '警告...', '栈空间不足！', QMessageBox.Yes, QMessageBox.Yes)

        num, ok = QInputDialog.getInt(self, '入栈', '输入整数', random.randint(1, 50))
        if ok:
            self.text.append('元素%d入栈，top += 1' % num)

            color = {0: 'rgb(255, 138, 39)', 1: 'rgb(82, 188, 105)', 2: 'rgb(46, 187, 209)'}
            bottom = self.draw_stack_area.geometry().height()

            btn = QPushButton(str(num), self.draw_stack_area)
            btn.resize(self.width, self.height)
            btn.setFont(QFont('', self.fontSize))
            btn.setStyleSheet('QPushButton{border: none; background: %s;}' % color[self.ii])
            self.stack.append(btn)
            self.ii = (self.ii + 1) % 3
            btn.move(self.left, self.space)
            btn.show()

            animation = QPropertyAnimation(btn, b'pos', self.draw_stack_area)
            animation.setStartValue(QPoint(self.left, self.space))
            animation.setEndValue(QPoint(self.left, bottom - (len(self.stack)) * (self.space + self.height)))
            animation.setDuration(self.action_speed)
            animation.start()

    def click_bt3(self):
        def delete(a0: QPushButton):
            a0.deleteLater()
            btn.show()
            animation1.start()

        if not len(self.stack):
            QMessageBox.critical(self, '错误...', '栈为空', QMessageBox.Yes, QMessageBox.Yes)
        else:
            self.text.append('栈顶元素出栈，top -= 1')

            a = self.stack.pop()
            num = a.text()
            style = a.styleSheet()
            font = a.font()

            animation = QPropertyAnimation(a, b'pos', self.draw_stack_area)
            animation.finished.connect(lambda: delete(a))
            animation.setStartValue(a.pos())
            animation.setEndValue(QPoint(self.left, self.space))
            animation.setDuration(self.action_speed)
            animation.start()

            right = self.draw_pop_area.geometry().width()
            btn = QPushButton(num, self.draw_pop_area)
            btn.setStyleSheet(style)
            btn.resize(self.height, self.width)
            btn.setFont(font)
            btn.move(right - self.space - self.height, self.top)
            self.pop.append(btn)

            animation1 = QPropertyAnimation(btn, b'pos', self.draw_pop_area)
            animation1.setStartValue(btn.pos())
            animation1.setEndValue(QPoint(self.space + (len(self.pop) - 1) * (self.space + self.height), self.top))
            animation1.setDuration(self.action_speed)

    def click_bt4(self):
        num, ok = QInputDialog.getDouble(self, '设置演示速度', '单位：秒')
        if ok and num:
            self.action_speed = num * 1000

    def resizeEvent(self, a0) -> None:
        ii = 0
        bottom = self.draw_stack_area.geometry().bottom() - self.space
        for i in self.stack:
            ii += 1
            i.move(self.left, bottom - ii * (self.space + self.height))
