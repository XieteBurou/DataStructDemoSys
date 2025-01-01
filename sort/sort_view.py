"""
@File     : sort_view.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/3/15 9:23
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/15 9:23        1.0             None
"""
import threading
import time
from abc import abstractmethod

from mainFrame import new_array_buttons
from numpy.random import randint
from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF, QPropertyAnimation, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QFont, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QInputDialog, QTextBrowser


class SortView(QWidget):
    # 绘图中的一些常量
    _space = 8
    _width = 40
    _top = 60
    _bottom = 80

    font_size = 14

    # 灰色
    default_rect_color = QColor(130, 130, 130)
    default_rect_font = QFont('Microsoft YaHei', font_size, 1)

    # 橙色
    act_rect_color1 = QColor(255, 165, 0)
    # 蓝色
    act_rect_color2 = QColor(0, 191, 255)

    # 紫色
    median_color = QColor(255, 0, 255)
    # 绿色
    finished_rect_color = QColor(50, 205, 50)

    def __init__(self, parent=None):
        super(SortView, self).__init__(parent)

        # 数据区域
        self.arr = list(randint(1, 51, 12))
        # 绘图数据
        self.point_1 = []
        self.point_2 = []
        self.draw_list: list[dict] = []
        self.action_speed = 0.6
        self._fps = 60
        self.acting = False
        # 屏幕数据
        self.setMinimumSize(800, 400)
        self.resize(800, 400)

    def reset_draw_list(self):
        """
        修改绘图区
        """
        arr_len = len(self.arr)
        min_rect_height = 20
        max_num = max(self.arr)
        max_rect_height = self.height() - self._top - self._bottom - min_rect_height
        border_left = self.width() / 2 - (arr_len * (self._width + self._space) - self._space) / 2
        self.draw_list.clear()

        for i in range(arr_len):
            rect_height = max_rect_height * self.arr[i] / max_num + min_rect_height
            border_top = self._top + max_rect_height + min_rect_height - rect_height

            self.draw_list.append({
                'rect_brush_color': self.default_rect_color,
                'rect_font': self.default_rect_font,
                'rect': QRectF(border_left + i * (self._width + self._space), border_top, self._width, rect_height),
                'font_color': QColor(Qt.white),
                'num': str(self.arr[i])
            })

    def paintEvent(self, a0) -> None:
        draw_area = QRectF(0, 0, self.geometry().width(), self.geometry().height())

        paint = QPainter()
        paint.begin(self)

        # 设背景为黑色， 边框为灰色
        pen = QPen(Qt.gray, 2, Qt.SolidLine)
        paint.setPen(pen)
        paint.fillRect(draw_area, QColor(10, 10, 10))
        paint.drawRect(draw_area)

        # 绘制数组
        for i in self.draw_list:
            paint.fillRect(i['rect'], i['rect_brush_color'])
            paint.setFont(i['rect_font'])
            paint.setPen(i['font_color'])
            paint.drawText(i['rect'], Qt.AlignBottom | Qt.AlignCenter, i['num'])

        # 结束绘图
        paint.end()

    def resizeEvent(self, a0) -> None:
        self.reset_draw_list()
        self.update()

    def set_arr(self, arr: list) -> None:
        self.arr = arr.copy()
        self.reset_draw_list()
        self.update()

    def set_speed(self, speed: float) -> None:
        self.action_speed = speed

    def swap_pos(self, i0: int, j0: int) -> None:
        """
        交换i0和j0位置上的数

        :param i0: 位置1
        :param j0: 位置2
        :return: None
        """
        self.acting = True
        thread = threading.Thread(target=self.swap_pos_event, args=(i0, j0), daemon=True)
        thread.start()

    def swap_pos_event(self, i0, j0) -> None:
        if i0 > j0:
            i0, j0 = j0, i0
        dx = self.draw_list[j0]['rect'].x() - self.draw_list[i0]['rect'].x()
        NOT = int(self.action_speed * self._fps)
        mx = dx / NOT

        for _ in range(NOT):
            self.draw_list[i0]['rect'].setX(self.draw_list[i0]['rect'].x() + mx)
            self.draw_list[i0]['rect'].setWidth(self._width)
            self.draw_list[j0]['rect'].setX(self.draw_list[j0]['rect'].x() - mx)
            self.draw_list[j0]['rect'].setWidth(self._width)
            self.update()
            time.sleep(self.action_speed / NOT / 2)

        self.draw_list[i0], self.draw_list[j0] = self.draw_list[j0], self.draw_list[i0]
        self.arr[i0], self.arr[j0] = self.arr[j0], self.arr[i0]
        self.acting = False


class ListSortWidget(QWidget):
    def __init__(self, parent=None):
        super(ListSortWidget, self).__init__(parent)
        # 数组
        self.arr = []  # 保留原数组
        # 绘图对象
        self.draw_widget = SortView(self)
        # 文本区
        self.text_list = []
        self.text_widget = QWidget()
        self.text_view = QTextBrowser()

        self.__init_data()
        self.__init_ui()

    def __init_data(self):
        self.arr = self.draw_widget.arr.copy()

    def __init_ui(self):
        self.text_widget.setLayout(QVBoxLayout())
        self.text_widget.layout().setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.text_widget.setStyleSheet('QWidget{border: 1px solid #D3D3D3;}')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.text_widget)
        bottom_layout.addWidget(self.text_view)
        bottom_layout.addLayout(self.__button_layout())

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.draw_widget)
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

    def __button_layout(self):
        self.button1 = QPushButton('开始')
        self.button2 = QPushButton('重置')
        self.button3 = QPushButton('创建')
        button4 = QPushButton('设置速度')

        self.button1.clicked.connect(self.btn_clicked1)
        self.button2.clicked.connect(self.btn_clicked2)
        self.button3.clicked.connect(self.btn_clicked3)
        button4.clicked.connect(self.btn_clicked4)

        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(button4)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(5, 0, 5, 0)

        return layout

    def btn_clicked1(self):
        self.start_sort()
        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)

    def btn_clicked2(self):
        self.draw_widget.set_arr(self.arr)
        self.text_view.clear()

    def btn_clicked3(self):
        dialog = new_array_buttons.NewArrayButton(self.arr, 18, 51)
        dialog.linked_list_signal.connect(self.set_arr)
        dialog.exec()

    def btn_clicked4(self):
        num, ok = QInputDialog.getDouble(self, '设置演示速度', '单位：秒')
        if ok and num:
            self.draw_widget.action_speed = num

    def set_arr(self, arr):
        self.arr = arr
        self.draw_widget.set_arr(arr.copy())

    def add_text(self, text_list: list) -> None:
        self.text_list = text_list
        for i in text_list:
            self.text_widget.layout().addWidget(i)

    @abstractmethod
    def start_sort(self):
        """
        需要排序的数组：
            self.sort_arr
            self.draw_widget.arr
        需要修改:
            self.draw_widget.draw_list 中对应位置的颜色
            self.draw_widget.

        :return:
        """
        pass


class DoubleSortView(SortView):
    # 绘图中的一些常量
    _space = 8
    _width = 40
    _top = 40
    _bottom = 320

    font_size = 14

    def __init__(self, parent=None):
        super(DoubleSortView, self).__init__(parent)
        self.draw_list1: list[dict] = []
        self.x_list = []
        self.setMinimumSize(800, 600)

    def merge_pop(self, i0, j0):
        """

        :param i0: 原数组的位置
        :param j0: 加入到新数组的位置
        """
        self.acting = True
        thread = threading.Thread(target=self.merge_pop_event, args=(i0, j0), daemon=True)
        thread.start()

    def reset_draw_list(self):
        super(DoubleSortView, self).reset_draw_list()
        self.x_list.clear()
        for i in self.draw_list:
            self.x_list.append(i['rect'].x())

    def merge_pop_event(self, i0, j0):
        dx = self.x_list[j0] - self.draw_list[i0]['rect'].x()
        height = self.draw_list[i0]['rect'].height()
        NOT = int(self.action_speed * self._fps)
        mx = dx / NOT
        my = (self._bottom - 20) / NOT

        self.draw_list[i0]['rect_brush_color'] = self.median_color

        for _ in range(NOT):
            self.draw_list[i0]['rect'].setX(self.draw_list[i0]['rect'].x() + mx)
            self.draw_list[i0]['rect'].setY(self.draw_list[i0]['rect'].y() + my)
            self.draw_list[i0]['rect'].setWidth(self._width)
            self.draw_list[i0]['rect'].setHeight(height)
            self.update()
            time.sleep(self.action_speed / NOT / 2)

        self.draw_list1.append(self.draw_list[i0])
        self.acting = False

    def merge_add(self, left):
        """
        将 self.draw_list1的值赋给 self.draw_list[left: right]
        """
        self.acting = True
        thread = threading.Thread(target=self.merge_add_event, args=(left,), daemon=True)
        thread.start()

    def merge_add_event(self, left):

        NOT = int(self.action_speed * self._fps)
        my = (self._bottom - 20) / NOT

        for i in self.draw_list1:
            height = i['rect'].height()
            i['rect_brush_color'] = self.finished_rect_color
            for _ in range(NOT):
                i['rect'].setY(i['rect'].y() - my)
                i['rect'].setHeight(height)
                self.update()
                time.sleep(self.action_speed / NOT / 2)

        for i in range(len(self.draw_list1)):
            self.draw_list[left + i] = self.draw_list1[i]
            self.arr[left + i] = int(self.draw_list1[i]['num'])
        self.draw_list1.clear()

        self.acting = False


class DoubleSortWidget(QWidget):
    def __init__(self, parent=None):
        super(DoubleSortWidget, self).__init__(parent)
        # 数组
        self.arr = []  # 保留原数组
        # 绘图对象
        self.draw_widget = DoubleSortView(self)
        # 文本区
        self.text_list = []
        self.text_widget = QWidget()
        self.text_view = QTextBrowser()

        self.__init_data()
        self.__init_ui()

    def __init_data(self):
        self.arr = self.draw_widget.arr.copy()

    def __init_ui(self):
        self.text_widget.setLayout(QVBoxLayout())
        self.text_widget.layout().setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.text_widget.setStyleSheet('QWidget{border: 1px solid #D3D3D3;}')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.text_widget)
        bottom_layout.addWidget(self.text_view)
        bottom_layout.addLayout(self.__button_layout())

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.draw_widget)
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

    def __button_layout(self):
        self.button1 = QPushButton('开始')
        self.button2 = QPushButton('重置')
        self.button3 = QPushButton('创建')
        button4 = QPushButton('设置速度')

        self.button1.clicked.connect(self.btn_clicked1)
        self.button2.clicked.connect(self.btn_clicked2)
        self.button3.clicked.connect(self.btn_clicked3)
        button4.clicked.connect(self.btn_clicked4)

        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(button4)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(5, 0, 5, 0)

        return layout

    def btn_clicked1(self):
        self.start_sort()
        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)

    def btn_clicked2(self):
        self.draw_widget.set_arr(self.arr)
        self.text_view.clear()

    def btn_clicked3(self):
        dialog = new_array_buttons.NewArrayButton(self.arr, 18, 51)
        dialog.linked_list_signal.connect(self.set_arr)
        dialog.exec()

    def btn_clicked4(self):
        num, ok = QInputDialog.getDouble(self, '设置演示速度', '单位：秒')
        if ok and num:
            self.draw_widget.action_speed = num

    def set_arr(self, arr):
        self.arr = arr
        self.draw_widget.set_arr(arr.copy())

    def add_text(self, text_list: list) -> None:
        self.text_list = text_list
        for i in text_list:
            self.text_widget.layout().addWidget(i)

    @abstractmethod
    def start_sort(self):
        pass


class BlockSortView(QWidget):
    """
    用按钮+动画实现。
    在paintEvent中绘制 0~9的槽。
    """
    _width = 50
    _height = 26
    _h_space = 8
    _v_space = 4

    _bottom = 20
    _top = 40

    _fontSize = 14

    # 动画信号
    add_signal = pyqtSignal(int, int)
    pop_signal = pyqtSignal(int, float, list)

    def __init__(self, arr=None, parent=None):
        super(BlockSortView, self).__init__(parent)

        # 数组
        self.arr = arr

        # button
        self.button_list = []
        self._slot_list = [[] for _ in range(10)]
        # paint数据
        self.action_speed = 500
        self._slot = []
        self._no_act = True

        # 绑定信号
        # noinspection PyUnresolvedReferences
        self.add_signal.connect(self.slot_add_animation)
        # noinspection PyUnresolvedReferences
        self.pop_signal.connect(self.__slot_pop_animation)
        # 初始化
        self.__init_ui()

    def __init_data(self):
        x0 = (self.width() - len(self.arr) * (self._width + self._h_space) - self._h_space) // 2
        for i in self.button_list:
            i.close()
            i.deleteLater()
        self.button_list.clear()
        for i in range(len(self.arr)):
            button = QPushButton(str(self.arr[i]), self)
            button.setEnabled(False)
            button.setFont(QFont('', self._fontSize, 2))
            button.resize(self._width, self._height)
            button.move(x0 + i * (self._width + self._h_space), self._top)
            button.setStyleSheet("""
                QPushButton {  
                     border-style: outset;
                     border-width: 2px;
                     border-color: rgb(10,45,110); 
                     color: black;
                }  
            """)
            button.show()
            self.button_list.append(button)

    def __init_ui(self):
        self.resize(800, 600)
        self.setMinimumSize(800, 600)

    def set_arr(self, arr: list):
        self.arr = arr.copy()
        self.__init_data()

    def resizeEvent(self, a0):
        if self._no_act:
            self.__init_data()

            self._slot.clear()
            sum_width = (self._width + self._h_space) * 10 - self._h_space
            x0 = (self.width() - sum_width) / 2
            for i in range(10):
                self._slot.append(
                    QPointF(
                        x0 + i * (self._width + self._h_space),
                        self.height() - self._bottom - self._height
                    )
                )

    def paintEvent(self, a0) -> None:
        """
        需要绘制 0~9 共10个槽， 并给窗口加上边框
        """
        # 获取窗口
        main_rect = QRectF(3, 3, self.width() - 6, self.height() - 6)

        # 创建画笔
        paint = QPainter()
        paint.begin(self)

        # 填充背景
        paint.fillRect(main_rect, QColor(236, 236, 236))
        paint.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
        paint.drawRect(main_rect)
        # 绘制槽
        paint.setFont(QFont('', self._fontSize, 2))
        paint.setPen(QColor(0, 0, 0))
        for i in range(10):
            paint.drawLine(
                QLineF(self._slot[i].x(), self._slot[i].y(), self._slot[i].x() + self._width, self._slot[i].y())
            )
            paint.drawText(
                QRectF(self._slot[i].x(), self._slot[i].y(), self._width, self._height),
                Qt.AlignCenter,
                '%d' % i
            )

        # 消除画笔
        paint.end()

    def slot_add_animation(self, i0, j0):
        """
        将 arr[i0] 加入到 slot_list[j0]的动画
        """
        animation = QPropertyAnimation(self.button_list[i0], b'pos', self)
        animation.setStartValue(self.button_list[i0].pos())
        animation.setEndValue(
            QPointF(
                self._slot[j0].x(),
                self._slot[j0].y() - (len(self._slot_list[j0]) + 1) * (self._height + self._v_space)
            )
        )
        animation.setDuration(self.action_speed)
        animation.start()

        self._slot_list[j0].append(self.button_list[i0])

    def __slot_pop_animation(self, i, x0, j0):
        last_pos = self.button_list[i].pos()
        animation = QPropertyAnimation(self.button_list[i], b'pos', self)
        animation.setStartValue(last_pos)
        animation.setEndValue(QPointF(x0 + i * (self._width + self._h_space), self._top))
        animation.setDuration(self.action_speed)
        animation.start()
        for i0 in j0:
            animation1 = QPropertyAnimation(i0, b'pos', self)
            animation1.setStartValue(i0.pos())
            animation1.setEndValue(last_pos)
            animation1.setDuration(self.action_speed - 90)
            animation1.start()
            last_pos = i0.pos()

    def __slot_pop_event(self):
        i = 0
        x0 = (self.width() - len(self.arr) * (self._width + self._h_space) - self._h_space) // 2
        for j in self._slot_list:
            while j:
                self.button_list[i] = j.pop(0)
                self.arr[i] = int(self.button_list[i].text())
                # noinspection PyUnresolvedReferences
                self.pop_signal.emit(i, x0, j)
                time.sleep(self.action_speed / 1000 + 0.05)
                i += 1
        # 排序结束 开放按钮
        self._no_act = True

    def slot_pop_animation(self):
        thread = threading.Thread(target=self.__slot_pop_event, daemon=True)
        thread.start()


class BlockSortWidget(QWidget):
    def __init__(self, parent=None, max_num=10):
        super(BlockSortWidget, self).__init__(parent)
        # 数组
        self.max_num = max_num
        self.arr = []  # 保留原数组
        # 绘图对象
        self.draw_widget = BlockSortView(self)
        # 文本区
        self.text_list = []
        self.text_widget = QWidget()
        self.text_view = QTextBrowser()

        self.__init_data()
        self.__init_ui()

    def __init_data(self):
        self.arr = list(randint(0, self.max_num, randint(8, 13)))
        self.draw_widget.set_arr(self.arr)

    def __init_ui(self):
        self.text_widget.setLayout(QVBoxLayout())
        self.text_widget.layout().setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.text_widget.setStyleSheet('QWidget{border: 1px solid #D3D3D3;}')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.text_widget)
        bottom_layout.addWidget(self.text_view)
        bottom_layout.addLayout(self.__button_layout())

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.draw_widget)
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

    def __button_layout(self):
        self.button1 = QPushButton('开始')
        self.button2 = QPushButton('重置')
        self.button3 = QPushButton('创建')
        button4 = QPushButton('设置速度')

        self.button1.clicked.connect(self.btn_clicked1)
        self.button2.clicked.connect(self.btn_clicked2)
        self.button3.clicked.connect(self.btn_clicked3)
        button4.clicked.connect(self.btn_clicked4)

        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(button4)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(5, 0, 5, 0)

        return layout

    def btn_clicked1(self):
        self.start_sort()
        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)

    def btn_clicked2(self):
        self.draw_widget.set_arr(self.arr)
        self.text_view.clear()

    def btn_clicked3(self):
        dialog = new_array_buttons.NewArrayButton(self.arr, 14, self.max_num, 0)
        dialog.linked_list_signal.connect(self.set_arr)
        dialog.exec()

    def btn_clicked4(self):
        num, ok = QInputDialog.getDouble(self, '设置演示速度', '单位：秒')
        if ok and num:
            self.draw_widget.action_speed = num * 1000

    def set_arr(self, arr):
        self.arr = arr
        self.draw_widget.set_arr(arr)

    def add_text(self, text_list: list) -> None:
        self.text_list = text_list
        for i in text_list:
            self.text_widget.layout().addWidget(i)

    @abstractmethod
    def start_sort(self):
        pass
