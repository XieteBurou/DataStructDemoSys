
"""
@File     : my_queue.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/3/13 9:56
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/13 9:56        1.0             None
"""

import random

from PyQt5.QtCore import QPropertyAnimation, QPoint
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QTextBrowser, QGridLayout, QPushButton, QVBoxLayout, QInputDialog, QMessageBox


class Queue(QWidget):
    width = 50
    height = 100
    space = 10
    top = 25
    fontSize = 15

    def __init__(self, parent=None):
        super(Queue, self).__init__(parent)

        # 队列数据
        self.length = 14
        self.queue = []
        self.pop = []
        self.head = 0
        self.tail = 0
        # 绘图数据
        self.action_speed = 500
        self.ii = 0
        # 绘图区域
        self.draw_queue_area = QWidget()
        self.draw_pop_area = QWidget()
        self.text = QTextBrowser()

        self.__init_data()
        self.__init_ui()

    def __init_data(self):
        for i in self.pop:
            i.deleteLater()
        self.pop.clear()
        for j in self.queue:
            j.deleteLater()
        self.queue.clear()

        self.text.setText('队列\n')
        self.text.append('队列实现的是一种先进先出的策略，队列只有入队和出队两种操作，只能访问队头元素或取队头元素\n')
        self.text.append('class Queue:            # 循环队列')
        self.text.append('    queue = int[n]      # 线性数组')
        self.text.append('    head = 0            # 队头下标')
        self.text.append('    tail = 0            # 队尾下标')
        self.text.append('    def EnQueue(self, x):')
        self.text.append('        self.queue[self.tail] = x')
        self.text.append('        self.tail = (self.tail + 1) % n \n')
        self.text.append('    def DeQueue(self):')
        self.text.append('        x = self.queue[head]')
        self.text.append('        self.head = (self.head + 1) % n')
        self.text.append('        return x\n')

    def __init_ui(self):

        self.draw_queue_area.setMinimumSize(800, 150)
        self.draw_queue_area.setMaximumHeight(200)
        self.draw_pop_area.setMinimumSize(800, 150)
        self.draw_pop_area.setMaximumHeight(200)
        self.draw_queue_area.setStyleSheet(
            """
                QWidget {
                    border-top: 1px solid #D3D3D3;
                    border-bottom: 1px solid #D3D3D3;
                    background-color: rgb(238,238,238);
                }
            """
        )
        self.draw_pop_area.setStyleSheet(
            """
                QWidget {
                    border-top: 1px solid #D3D3D3;
                    border-left: 1px solid #D3D3D3;
                    border-bottom: 1px solid #D3D3D3;
                    background-color: rgb(238,238,238);
                }
            """
        )

        layout = QGridLayout(self)
        layout.addWidget(self.draw_queue_area, 0, 0, 1, 2)
        layout.addWidget(self.draw_pop_area, 1, 0, 1, 2)
        layout.addLayout(self.__set_control_layout(), 2, 0)
        layout.addWidget(self.text, 2, 1)

    def __set_control_layout(self):
        """
        创建控制布局

        :return:
        """

        button_1 = QPushButton('重置')
        button_2 = QPushButton('入队')
        button_3 = QPushButton('出队')
        button_4 = QPushButton('重置出队序列')
        button_5 = QPushButton('调整速度')

        button_1.clicked.connect(self.click_bt1)
        button_2.clicked.connect(self.click_bt2)
        button_3.clicked.connect(self.click_bt3)
        button_4.clicked.connect(self.click_bt4)
        button_5.clicked.connect(self.click_bt5)

        layout = QVBoxLayout()
        layout.addWidget(button_1)
        layout.addWidget(button_2)
        layout.addWidget(button_3)
        layout.addWidget(button_4)
        layout.addWidget(button_5)
        layout.setContentsMargins(8, 50, 8, 50)

        return layout

    def click_bt1(self):
        self.__init_data()

    def click_bt2(self):
        if len(self.queue) > self.length:
            QMessageBox.warning(self, '警告...', '队列空间不足！', QMessageBox.Yes, QMessageBox.Yes)

        else:
            num, ok = QInputDialog.getInt(self, '入队', '输入整数', random.randint(1, 50))
            if ok:
                self.text.append('元素%d入队，尾指针后移' % num)

                color = {0: 'rgb(255, 138, 39)', 1: 'rgb(82, 188, 105)', 2: 'rgb(46, 187, 209)'}
                bottom = self.draw_queue_area.geometry().right()

                btn = QPushButton(str(num), self.draw_queue_area)
                btn.resize(self.width, self.height)
                btn.setFont(QFont('', self.fontSize))
                btn.setStyleSheet('QPushButton{border: none; background: %s;}' % color[self.ii])
                self.queue.append(btn)
                self.ii = (self.ii + 1) % 3
                btn.move(bottom-self.width-self.space, self.top)
                btn.show()

                animation = QPropertyAnimation(btn, b'pos', self.draw_queue_area)
                animation.setStartValue(btn.pos())
                animation.setEndValue(QPoint(self.space + (len(self.queue) - 1) * (self.space + self.width), self.top))
                animation.setDuration(self.action_speed)
                animation.start()

    def click_bt3(self):
        def delete(a0: QPushButton):
            a0.deleteLater()
            btn.show()
            animation1.start()
            i = 0
            for ii in self.queue:
                anima = QPropertyAnimation(ii, b'pos', self.draw_queue_area)
                anima.setStartValue(ii.pos())
                anima.setEndValue(QPoint(self.space + i * (self.space + self.width), self.top))
                anima.setDuration(self.action_speed)
                anima.start()
                i += 1

        if not len(self.queue):
            QMessageBox.critical(self, '错误...', '队列为空！', QMessageBox.Yes, QMessageBox.Yes)
        else:
            self.text.append('队头元素出队，头指针后移')

            a = self.queue.pop(0)
            num = a.text()
            style = a.styleSheet()
            font = a.font()

            animation = QPropertyAnimation(a, b'pos', self.draw_queue_area)
            animation.finished.connect(lambda: delete(a))
            animation.setStartValue(a.pos())
            animation.setEndValue(QPoint(a.x() - 300, self.top))
            animation.setDuration(self.action_speed)
            animation.start()

            right = self.draw_pop_area.geometry().width()
            btn = QPushButton(num, self.draw_pop_area)
            btn.setStyleSheet(style)
            btn.resize(self.width, self.height)
            btn.setFont(font)
            btn.move(right - self.space - self.width, self.top)
            self.pop.append(btn)

            animation1 = QPropertyAnimation(btn, b'pos', self.draw_pop_area)
            animation1.setStartValue(btn.pos())
            animation1.setEndValue(QPoint(self.space + (len(self.pop) - 1) * (self.space + self.width), self.top))
            animation1.setDuration(self.action_speed)

    def click_bt4(self):
        for i in self.pop:
            i.deleteLater()
        self.pop.clear()

    def click_bt5(self):
        num, ok = QInputDialog.getDouble(self, '设置演示速度', '单位：秒')
        if ok and num:
            self.action_speed = num * 1000

    def resizeEvent(self, a0) -> None:
        self.length = self.draw_queue_area.geometry().right() // (self.space + self.width)
