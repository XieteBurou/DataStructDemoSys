"""
数据结构：链表

@File     : linkedList.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/3/8 16:10
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/8 16:10        1.0             None
"""

import random
import threading
import time
from mainFrame import new_array_buttons

from PyQt5.QtCore import QRegExp, pyqtSignal, Qt, QRect, QPoint, QLine
from PyQt5.QtGui import QRegExpValidator, QPainter, QPaintEvent, QPen, QFont, QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout, QDialog, QLabel, QSpinBox, QLineEdit, \
    QTextBrowser, QInputDialog, QMessageBox


class InsertButton(QDialog):
    insert_signal = pyqtSignal(int, int)

    def __init__(self, length):
        super(InsertButton, self).__init__()
        self.length = length - 1
        self.spin_i = QSpinBox()
        self.spin_value = QSpinBox()
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('插入结点')
        self.resize(260, 190)

        button_1 = QPushButton('在头部插入value')
        button_2 = QPushButton('在尾部插入value')
        button_3 = QPushButton('在第i个节点上插入value')
        button_4 = QPushButton('取消')

        button_1.clicked.connect(self.__click_bt1)
        button_2.clicked.connect(self.__click_bt2)
        button_3.clicked.connect(self.__click_bt3)
        button_4.clicked.connect(self.__click_bt4)

        self.spin_i.setValue(random.randint(1, self.length))
        self.spin_i.setMinimum(1)
        self.spin_i.setMaximum(self.length)

        self.spin_value.setValue(random.randint(1, 100))
        label_i = QLabel(' i = ')
        label_value = QLabel(' value = ')

        layout = QGridLayout(self)
        layout.addWidget(label_i, 0, 0)
        layout.addWidget(self.spin_i, 0, 1)
        layout.addWidget(label_value, 0, 2)
        layout.addWidget(self.spin_value, 0, 3)
        layout.addWidget(button_1, 1, 0, 1, 4)
        layout.addWidget(button_2, 2, 0, 1, 4)
        layout.addWidget(button_3, 3, 0, 1, 4)
        layout.addWidget(button_4, 4, 3, 1, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(3, 1)

    def __click_bt1(self):
        """
        在头部插入value

        :return: None
        """
        # noinspection PyUnresolvedReferences
        self.insert_signal.emit(0, self.spin_value.value())
        self.close()

    def __click_bt2(self):
        """
        在尾部插入value

        :return:
        """
        # noinspection PyUnresolvedReferences
        self.insert_signal.emit(self.length + 1, self.spin_value.value())
        self.close()

    def __click_bt3(self):
        """
        在第i个节点上插入value

        :return:
        """
        # noinspection PyUnresolvedReferences
        self.insert_signal.emit(self.spin_i.value(), self.spin_value.value())
        self.close()

    def __click_bt4(self):
        """
        取消

        :return: None
        """
        self.close()


class LinkedList(QWidget):
    def __init__(self, parent=None):
        super(LinkedList, self).__init__(parent)
        # 链表数据
        self.arr = list()
        # 绘图数据
        self.draw_list = list()
        self.action_flag = True
        self.action_node = dict()
        self.action_speed = 1
        # 绘图区域
        self.drawing_area = QWidget()
        self.text = QTextBrowser()

        self.__init_data()
        self.__init_ui()

    def __init_data(self):
        k = random.randint(3, 10)
        for i in range(k):
            self.arr.append(random.randint(1, 100))

        self.text.setText('单向链表')
        self.text.append('')
        self.text.append('单向链表结构:')
        self.text.append('class LinkedNode:')
        self.text.append('    value: int')
        self.text.append('    next: LinkedNode')
        self.text.append('')
        self.text.append('链表是一种线性结构，与数组不同的是，单向链表只记录头结点位置，无法直接获取头结点后的结点')
        self.text.append('链表的优势是不需要有连续的存储空间，需要多少空间就分配多少空间，没有长度限制，方便修改结点')

    def __init_ui(self):

        self.drawing_area.setMinimumSize(800, 300)
        self.drawing_area.setStyleSheet(
            """
                QWidget {
                    border: 1px solid #D3D3D3;
                }
            """
        )

        layout = QGridLayout()
        layout.addWidget(self.drawing_area, 0, 0, 1, 4)
        layout.addLayout(self.__set_left_bottom_layout(), 1, 1)
        layout.addWidget(self.text, 1, 3)
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 12)
        layout.setRowStretch(0, 5)
        layout.setRowStretch(1, 4)
        self.setLayout(layout)

    def __set_left_bottom_layout(self):
        """
        创建左下角布局

        :return:
        """
        button_1 = QPushButton('创建')
        button_2 = QPushButton('搜索')
        button_3 = QPushButton('插入')
        button_4 = QPushButton('移除')
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
        layout.setContentsMargins(3, 3, 3, 3)

        return layout

    def click_bt1(self):
        dialog = new_array_buttons.NewArrayButton(self.arr)
        # noinspection PyUnresolvedReferences
        dialog.linked_list_signal.connect(self.set_arr)
        dialog.exec()
        self.action_flag = True

    def click_bt2(self):
        num, ok = QInputDialog.getInt(self, '搜索', '输入值', random.randint(1, 100))
        if ok:
            self.search_value(num)

    def click_bt3(self):
        if len(self.arr) >= 10:
            QMessageBox.warning(self, '警告', '长度超出限制', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            dialog = InsertButton(len(self.arr))
            # noinspection PyUnresolvedReferences
            dialog.insert_signal.connect(self.insert_node)
            dialog.exec()

    def click_bt4(self):
        num, ok = QInputDialog.getInt(
            self, '移除', '移除第i个结点',
            random.randint(0, len(self.arr) - 1),
            0,
            len(self.arr) - 1
        )
        if ok:
            self.delete_index(num)

    def click_bt5(self):
        num, ok = QInputDialog.getDouble(self, '调整速度', '单位：秒')
        if ok and num:
            self.action_speed = num

    def set_arr(self, arr):
        self.arr = arr

    def insert_node(self, index, value):
        if index == len(self.arr):
            self.text.setText('在尾部插入值为%d的结点' % value)
        else:
            self.text.setText('在第%d位插入值为%d的结点' % (index, value))
        self.__compute_draw_area(self.drawing_area.geometry())
        thread = threading.Thread(target=self.insert_action, args=(index, value), daemon=True)
        thread.start()

    def insert_action(self, index, value):
        self.text.append('取头指针指向的结点, index=0')
        i = 0
        while i != index:
            self.text.append('位置是%d' % i)
            self.draw_list[i]['rect-pen'].setColor(QColor(255, 138, 39))
            self.draw_list[i]['value-pen'].setColor(Qt.white)
            self.draw_list[i]['fill-rect'] = QColor(255, 138, 39)
            self.update()
            time.sleep(self.action_speed)
            self.draw_list[i].pop('fill-rect')
            self.draw_list[i]['rect-pen'].setColor(QColor(255, 138, 39))
            self.draw_list[i]['value-pen'].setColor(Qt.black)
            self.draw_list[i]['line-pen'].setColor(QColor(255, 138, 39))
            self.update()
            self.text.append('  取该节点的next指针, index += 1')
            time.sleep(self.action_speed)
            i += 1
        if i < len(self.arr):
            self.draw_list[i]['rect-pen'].setColor(QColor(46, 187, 209))
            self.draw_list[i]['value-pen'].setColor(Qt.black)
            self.update()
            time.sleep(self.action_speed)

            self.text.append('取到第%d位的指针' % index)
            self.action_node['rect-pen'] = QPen(QColor(82, 188, 105), 2, Qt.SolidLine)
            self.action_node['rect-left'] = QRect(self.draw_list[i]['rect-left'])
            self.action_node['rect-left'].setY(self.action_node['rect-left'].y() + 100)
            self.action_node['rect-left'].setHeight(self.draw_list[i]['rect-left'].height())
            self.action_node['rect-right'] = QRect(self.draw_list[i]['rect-right'])
            self.action_node['rect-right'].setY(self.action_node['rect-right'].y() + 100)
            self.action_node['rect-right'].setHeight(self.draw_list[i]['rect-right'].height())
            self.action_node['point'] = QPoint(
                self.action_node['rect-right'].x() + self.action_node['rect-right'].width() // 2,
                self.action_node['rect-right'].y() + self.action_node['rect-right'].height() // 2
            )
            self.action_node['point-pen'] = self.draw_list[i]['point-pen']
            self.action_node['value-pen'] = QPen(Qt.white, 2, Qt.SolidLine)
            self.action_node['value-font'] = QFont('Microsoft YaHei', 15, 1)
            self.action_node['value'] = str(value)
            self.action_node['fill-rect'] = QColor(82, 188, 105)
            self.update()
            self.text.append(' 创建值为"%d"的结点' % value)
            time.sleep(self.action_speed)

            point_2 = QPoint(
                self.action_node['point'].x(),
                self.draw_list[i]['rect-right'].y() + self.draw_list[i]['rect-right'].height()
            )
            self.action_node['line-1'] = QLine(self.action_node['point'], point_2)
            self.action_node['line-2'] = QLine(point_2.x() - 5, point_2.y() + 5, point_2.x(), point_2.y())
            self.action_node['line-3'] = QLine(point_2.x() + 5, point_2.y() + 5, point_2.x(), point_2.y())
            self.action_node['line-pen'] = QPen(QColor(82, 188, 105), 2, Qt.SolidLine)
            self.update()
            self.text.append('  将新建结点的next指针指向原链表第"%d"个结点' % index)
            time.sleep(self.action_speed)
        else:
            self.text.append(' 找到尾部指针')
            self.action_node['rect-pen'] = QPen(QColor(82, 188, 105), 2, Qt.SolidLine)
            self.action_node['rect-left'] = QRect(self.draw_list[i]['null-rect'])
            self.action_node['rect-left'].setY(self.action_node['rect-left'].y() + 100)
            self.action_node['rect-left'].setHeight(self.draw_list[i]['null-rect'].height())
            self.action_node['rect-right'] = QRect(self.action_node['rect-left'])
            self.action_node['rect-right'].setX(self.action_node['rect-right'].x() + 50)
            self.action_node['rect-right'].setWidth(30)
            self.action_node['point'] = QPoint(
                self.action_node['rect-right'].x() + self.action_node['rect-right'].width() // 2,
                self.action_node['rect-right'].y() + self.action_node['rect-right'].height() // 2
            )
            self.action_node['point-pen'] = self.draw_list[i - 1]['point-pen']
            self.action_node['value-pen'] = QPen(Qt.white, 2, Qt.SolidLine)
            self.action_node['value-font'] = QFont('Microsoft YaHei', 15, 1)
            self.action_node['value'] = str(value)
            self.action_node['fill-rect'] = QColor(82, 188, 105)
            self.update()
            self.text.append(' 创建值为"%d"的结点' % value)
            time.sleep(self.action_speed)

            point_2 = QPoint(
                self.draw_list[i]['null-rect'].x() + self.draw_list[i]['null-rect'].width(),
                self.draw_list[i]['null-rect'].y() + self.draw_list[i]['null-rect'].height()
            )
            self.action_node['line-1'] = QLine(self.action_node['point'], point_2)
            self.action_node['line-2'] = QLine(point_2.x() - 3, point_2.y() + 4, point_2.x(), point_2.y())
            self.action_node['line-3'] = QLine(point_2.x() + 4, point_2.y() + 1, point_2.x(), point_2.y())
            self.action_node['line-pen'] = QPen(QColor(82, 188, 105), 2, Qt.SolidLine)
            self.update()
            self.text.append('  将新建结点的next指针指向Null')
            time.sleep(self.action_speed)

        if i > 0:
            self.draw_list[i - 1]['line-1'].setP2(QPoint(
                self.action_node['rect-left'].x(),
                self.action_node['rect-left'].y())
            )
            self.draw_list[i - 1]['line-2'].setLine(
                self.action_node['rect-left'].x() - 5,
                self.action_node['rect-left'].y() - 2,
                self.action_node['rect-left'].x(),
                self.action_node['rect-left'].y()
            )
            self.draw_list[i - 1]['line-3'].setLine(
                self.action_node['rect-left'].x() + 2,
                self.action_node['rect-left'].y() - 5,
                self.action_node['rect-left'].x(),
                self.action_node['rect-left'].y()
            )
            self.update()
            self.text.append('  将原链表第"%d"个结点的next指针指向新建结点' % (index - 1))
            time.sleep(self.action_speed)
        else:
            self.text.append('  将head指针指向新建结点')

        if i < len(self.arr):
            point_2 = QPoint(self.draw_list[i]['line-1'].p2())
            point_2.setY(point_2.y() + 20)
            self.action_node['line-1'].setP2(point_2)
            self.action_node['line-2'].setP2(point_2)
            self.action_node['line-3'].setP2(point_2)
            self.action_node['line-2'].setP1(QPoint(point_2.x() - 4, point_2.y() + 1))
            self.action_node['line-3'].setP1(QPoint(point_2.x() + 1, point_2.y() + 4))
            for j in range(i, len(self.arr)):
                self.draw_list[j]['rect-left'].setX(self.draw_list[j]['rect-left'].x() + 100)
                self.draw_list[j]['rect-left'].setWidth(50)
                self.draw_list[j]['rect-right'].setX(self.draw_list[j]['rect-right'].x() + 100)
                self.draw_list[j]['rect-right'].setWidth(30)
                self.draw_list[j]['point'].setX(self.draw_list[j]['point'].x() + 100)
                point_2 = QPoint(self.draw_list[j]['point'].x() + 33, self.draw_list[j]['point'].y())
                self.draw_list[j]['line-1'].setP1(self.draw_list[j]['point'])
                self.draw_list[j]['line-1'].setP2(point_2)
                self.draw_list[j]['line-2'].setP2(point_2)
                self.draw_list[j]['line-3'].setP2(point_2)
                self.draw_list[j]['line-2'].setP1(QPoint(point_2.x() - 5, point_2.y() - 5))
                self.draw_list[j]['line-3'].setP1(QPoint(point_2.x() - 5, point_2.y() + 5))
            self.draw_list[-1]['null-rect'].setX(self.draw_list[-1]['null-rect'].x() + 100)
            self.draw_list[-1]['null-rect'].setWidth(50)
            self.update()
            time.sleep(self.action_speed)
        else:
            point_2 = QPoint(self.draw_list[i]['null-rect'].x() + 100, self.draw_list[i]['null-rect'].y() + 40)
            self.action_node['line-1'].setP2(point_2)
            self.action_node['line-2'].setP2(point_2)
            self.action_node['line-3'].setP2(point_2)
            self.action_node['line-2'].setP1(QPoint(point_2.x() - 4, point_2.y() + 1))
            self.action_node['line-3'].setP1(QPoint(point_2.x() + 1, point_2.y() + 4))
            self.draw_list[-1]['null-rect'].setX(self.draw_list[-1]['null-rect'].x() + 100)
            self.draw_list[-1]['null-rect'].setWidth(50)
            self.update()
            time.sleep(self.action_speed)

        self.action_node['rect-left'].setY(self.action_node['rect-left'].y() - 100)
        self.action_node['rect-right'].setY(self.action_node['rect-left'].y())
        self.action_node['rect-left'].setHeight(40)
        self.action_node['rect-right'].setHeight(40)
        self.action_node['point'].setY(self.action_node['point'].y() - 100)
        self.action_node['line-1'].setP1(self.action_node['point'])
        point_2 = QPoint(self.action_node['point'].x() + 33, self.action_node['point'].y())
        self.action_node['line-1'].setP2(point_2)
        self.action_node['line-2'].setP2(point_2)
        self.action_node['line-3'].setP2(point_2)
        self.action_node['line-2'].setP1(
            QPoint(self.action_node['line-2'].p2().x() - 5, self.action_node['line-2'].p2().y() - 5)
        )
        self.action_node['line-3'].setP1(
            QPoint(self.action_node['line-3'].p2().x() - 5, self.action_node['line-3'].p2().y() + 5)
        )
        if i > 0:
            point_2 = QPoint(self.draw_list[i - 1]['point'])
            point_2.setX(point_2.x() + 33)
            self.draw_list[i - 1]['line-1'].setP2(point_2)
            self.draw_list[i - 1]['line-2'].setP2(point_2)
            self.draw_list[i - 1]['line-3'].setP2(point_2)
            self.draw_list[i - 1]['line-2'].setP1(QPoint(point_2.x() - 5, point_2.y() - 5))
            self.draw_list[i - 1]['line-3'].setP1(QPoint(point_2.x() - 5, point_2.y() + 5))
        self.arr.insert(index, value)
        self.draw_list.insert(index, self.action_node.copy())
        self.action_node.clear()
        self.update()
        self.text.append('插入完成')
        time.sleep(self.action_speed)

    def __compute_draw_area(self, main_rect: QRect):
        """
        计算绘图区域, 刷新绘图列表

        :param main_rect: QRect
        :return: None
        """
        width_left = 50
        width_right = 30
        height = 40
        spacing = 20
        font_size = 15
        padding_left = main_rect.x() + 40
        padding_top = main_rect.y() + main_rect.height() // 2 - height

        self.draw_list.clear()

        for i in range(len(self.arr)):
            point = QPoint(
                padding_left + width_left + width_right // 2 + i * (width_left + width_right + spacing),
                padding_top + height // 2
            )
            right_point = QPoint(point.x() + width_right // 2 + spacing - 2, point.y())
            self.draw_list.append(
                {
                    'rect-left': QRect(
                        padding_left + i * (width_left + width_right + spacing),
                        padding_top, width_left, height
                    ),
                    'rect-right': QRect(
                        padding_left + width_left + i * (width_left + width_right + spacing),
                        padding_top, width_right, height
                    ),
                    'rect-pen': QPen(Qt.black, 2, Qt.SolidLine),
                    'point-pen': QPen(Qt.black, 8, Qt.SolidLine),
                    'point': point,
                    'value-pen': QPen(Qt.black, 2, Qt.SolidLine),
                    'value-font': QFont('Microsoft YaHei', font_size, 1),
                    'value': str(self.arr[i]),
                    'line-pen': QPen(Qt.black, 2, Qt.SolidLine),
                    'line-1': QLine(point, right_point),
                    'line-2': QLine(right_point.x() - 5, right_point.y() - 5, right_point.x(), right_point.y()),
                    'line-3': QLine(right_point.x() - 5, right_point.y() + 5, right_point.x(), right_point.y())
                }

            )
        i = len(self.arr)
        self.draw_list.append(
            {
                'null-rect': QRect(
                    padding_left + i * (width_left + width_right + spacing),
                    padding_top, width_left, height
                ),
                'null-font': QFont('Microsoft YaHei', font_size, 1),
                'null-pen': QPen(QPen(Qt.black, 2, Qt.SolidLine)),
            }
        )

    def search_value(self, value):
        self.text.setText('搜索值:' + str(value) + ' 的位置\n')
        self.__compute_draw_area(self.drawing_area.geometry())
        thread = threading.Thread(target=self.search_action, args=(value,), daemon=True)
        thread.start()

    def search_action(self, value: int):
        self.text.append('取头指针指向的结点, index=0')
        for i in range(len(self.arr)):
            self.text.append('值是%d' % (self.arr[i]))
            self.draw_list[i]['rect-pen'].setColor(QColor(255, 138, 39))
            self.draw_list[i]['value-pen'].setColor(Qt.white)
            self.draw_list[i]['fill-rect'] = QColor(255, 138, 39)
            self.update()
            time.sleep(self.action_speed)
            if self.arr[i] == value:
                self.text.append(' 在高亮结点找到 %d, index=%d' % (value, i))
                break
            else:
                self.draw_list[i].pop('fill-rect')
                self.draw_list[i]['rect-pen'].setColor(QColor(255, 138, 39))
                self.draw_list[i]['value-pen'].setColor(Qt.black)
                self.draw_list[i]['line-pen'].setColor(QColor(255, 138, 39))
                self.update()
                self.text.append('  取该结点的next指针, index += 1')
                if i == len(self.arr) - 1:
                    self.text.append('指针为空，未找到值为 %d 的结点' % value)
            time.sleep(self.action_speed)

    def delete_index(self, index):
        self.text.setText('删除第"%d"个结点' % index)
        self.__compute_draw_area(self.drawing_area.geometry())
        thread = threading.Thread(target=self.delete_action, args=(index,), daemon=True)
        thread.start()

    def delete_action(self, index):
        i = 0

        while i < index:
            self.draw_list[i]['rect-pen'].setColor(QColor(255, 138, 39))
            self.draw_list[i]['value-pen'].setColor(Qt.white)
            self.draw_list[i]['fill-rect'] = QColor(255, 138, 39)
            self.update()
            self.text.append('取第"%d"个结点' % i)
            time.sleep(self.action_speed)

            self.draw_list[i].pop('fill-rect')
            self.draw_list[i]['rect-pen'].setColor(QColor(255, 138, 39))
            self.draw_list[i]['value-pen'].setColor(Qt.black)
            self.draw_list[i]['line-pen'].setColor(QColor(255, 138, 39))
            self.update()
            self.text.append('  取该结点的next指针, index += 1')
            time.sleep(self.action_speed)
            i += 1

        self.draw_list[i]['rect-pen'].setColor(QColor(217, 81, 60))
        self.draw_list[i]['value-pen'].setColor(Qt.white)
        self.draw_list[i]['fill-rect'] = QColor(217, 81, 60)
        self.update()
        self.text.append('  找到第"%d"个结点, 记录该结点，将在最后删除' % index)
        time.sleep(self.action_speed)

        self.draw_list[i].pop('fill-rect')
        self.draw_list[i]['rect-pen'].setColor(QColor(217, 81, 60))
        self.draw_list[i]['value-pen'].setColor(QColor(217, 81, 60))
        self.draw_list[i]['line-pen'].setColor(QColor(217, 81, 60))
        self.update()
        self.text.append('  取第记录结点的next指针指向的结点')
        time.sleep(self.action_speed)

        if i + 1 < len(self.arr):
            self.draw_list[i+1]['rect-pen'].setColor(QColor(82, 188, 105))
            self.draw_list[i+1]['value-pen'].setColor(Qt.white)
            self.draw_list[i+1]['fill-rect'] = QColor(82, 188, 105)
            self.update()
            self.text.append('  取第“%d+1“个结点' % index)
            time.sleep(self.action_speed)

        self.draw_list[i]['rect-left'].setY(self.draw_list[i]['rect-left'].y() + 100)
        self.draw_list[i]['rect-left'].setHeight(40)
        self.draw_list[i]['rect-right'].setY(self.draw_list[i]['rect-left'].y())
        self.draw_list[i]['rect-right'].setHeight(40)
        self.draw_list[i]['point'].setY(self.draw_list[i]['point'].y() + 100)
        self.draw_list[i]['line-1'].setP1(self.draw_list[i]['point'])
        if i + 1 < len(self.arr):
            point_2 = QPoint(
                self.draw_list[i+1]['rect-left'].x(),
                self.draw_list[i+1]['rect-left'].y() + self.draw_list[i]['rect-left'].height()
            )
        else:
            point_2 = QPoint(
                self.draw_list[i+1]['null-rect'].x(),
                self.draw_list[i+1]['null-rect'].y() + self.draw_list[i+1]['null-rect'].height()
            )
        if i > 0:
            line_1 = QLine(self.draw_list[i - 1]['line-1'])
            line_2 = QLine(self.draw_list[i - 1]['line-2'])
            line_3 = QLine(self.draw_list[i - 1]['line-3'])
            self.draw_list[i - 1]['line-1'].setP2(QPoint(self.draw_list[i]['line-1'].p2()))
            self.draw_list[i - 1]['line-2'].setP2(self.draw_list[i - 1]['line-1'].p2())
            self.draw_list[i - 1]['line-3'].setP2(self.draw_list[i - 1]['line-1'].p2())
            self.draw_list[i - 1]['line-2'].setP1(QPoint(
                self.draw_list[i - 1]['line-2'].p2().x() - 5, self.draw_list[i - 1]['line-2'].p2().y() - 5
            ))
            self.draw_list[i - 1]['line-3'].setP1(QPoint(
                self.draw_list[i - 1]['line-2'].p2().x() - 5, self.draw_list[i - 1]['line-2'].p2().y() + 5
            ))
        self.draw_list[i]['line-1'].setP2(point_2)
        self.draw_list[i]['line-2'].setP2(point_2)
        self.draw_list[i]['line-3'].setP2(point_2)
        self.draw_list[i]['line-2'].setP1(QPoint(point_2.x() - 4, point_2.y() + 2))
        self.draw_list[i]['line-3'].setP1(QPoint(point_2.x() + 2, point_2.y() + 3))
        self.action_node = self.draw_list[i]
        self.arr.pop(i)
        self.draw_list.pop(i)
        self.update()
        if i > 1:
            self.text.append('将标记结点前方结点的next指针 指向标记结点的next指针指向的结点')
        else:
            self.text.append('将头指针指向标记结点的next指针指向的结点')
        time.sleep(self.action_speed)

        self.action_node.clear()
        self.update()
        self.text.append('删除记录的结点')
        time.sleep(self.action_speed)

        for j in range(i, len(self.arr)):
            self.draw_list[j]['rect-left'].setX(self.draw_list[j]['rect-left'].x() - 100)
            self.draw_list[j]['rect-left'].setWidth(50)
            self.draw_list[j]['rect-right'].setX(self.draw_list[j]['rect-right'].x() - 100)
            self.draw_list[j]['rect-right'].setWidth(30)
            self.draw_list[j]['point'].setX(self.draw_list[j]['point'].x() - 100)
            point_2 = self.draw_list[j]['line-1'].p2()
            point_2.setX(point_2.x() - 100)
            self.draw_list[j]['line-1'].setP1(self.draw_list[j]['point'])
            self.draw_list[j]['line-1'].setP2(point_2)
            self.draw_list[j]['line-2'].setP2(point_2)
            self.draw_list[j]['line-3'].setP2(point_2)
            self.draw_list[j]['line-2'].setP1(QPoint(point_2.x() - 5, point_2.y() - 5))
            self.draw_list[j]['line-3'].setP1(QPoint(point_2.x() - 5, point_2.y() + 5))
        if i > 0:
            self.draw_list[i - 1]['line-1'] = line_1
            self.draw_list[i - 1]['line-2'] = line_2
            self.draw_list[i - 1]['line-3'] = line_3
        self.draw_list[-1]['null-rect'].setX(self.draw_list[-1]['null-rect'].x() - 100)
        self.draw_list[-1]['null-rect'].setWidth(50)
        self.update()
        self.text.append('完成移除操作')
        time.sleep(self.action_speed)

    def paintEvent(self, event: QPaintEvent):
        # 获取画图区域, x, y相对于窗口偏移量.

        draw_area = self.drawing_area.geometry()
        if self.action_flag:
            self.__compute_draw_area(draw_area)
            self.action_flag = False

        # 设置画笔
        painter = QPainter()
        painter.begin(self)

        # 绘制背景色2
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.fillRect(draw_area, QColor(250, 255, 255))

        # 活动结点
        if self.action_node:
            if 'fill-rect' in self.action_node:
                painter.fillRect(self.action_node['rect-left'], self.action_node['fill-rect'])
            painter.setPen(self.action_node['rect-pen'])
            painter.drawRect(self.action_node['rect-left'])
            painter.drawRect(self.action_node['rect-right'])
            painter.setPen(self.action_node['point-pen'])
            painter.drawPoint(self.action_node['point'])
            painter.setPen(self.action_node['value-pen'])
            painter.setFont(self.action_node['value-font'])
            painter.drawText(self.action_node['rect-left'], Qt.AlignCenter, self.action_node['value'])
            if 'line-1' in self.action_node:
                painter.setPen(self.action_node['line-pen'])
                painter.drawLine(self.action_node['line-1'])
                painter.drawLine(self.action_node['line-2'])
                painter.drawLine(self.action_node['line-3'])

        # 绘制图像
        j = 0
        for i in self.draw_list:
            if j == len(self.arr):
                break

            elif j == 0 and 'rect-left' in i:
                painter.setPen(Qt.red)
                painter.setFont(QFont('Microsoft YaHei', 12))
                head_rect = QRect(i['rect-left'])
                head_rect.setY(head_rect.y() + 50)
                head_rect.setHeight(20)
                painter.drawText(head_rect, Qt.AlignCenter, 'head')
            j += 1

            if 'fill-rect' in i:
                painter.fillRect(i['rect-left'], i['fill-rect'])

            painter.setPen(i['rect-pen'])
            painter.drawRect(i['rect-left'])
            painter.drawRect(i['rect-right'])
            painter.setPen(i['point-pen'])
            painter.drawPoint(i['point'])
            painter.setPen(i['value-pen'])
            painter.setFont(i['value-font'])
            painter.drawText(i['rect-left'], Qt.AlignCenter, i['value'])
            painter.setPen(i['line-pen'])
            painter.drawLine(i['line-1'])
            painter.drawLine(i['line-2'])
            painter.drawLine(i['line-3'])

        i = self.draw_list[j]
        painter.setPen(i['null-pen'])
        painter.setFont(i['null-font'])
        painter.drawText(i['null-rect'], Qt.AlignCenter, 'Null')

        painter.end()
