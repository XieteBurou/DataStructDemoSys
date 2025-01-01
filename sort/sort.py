"""
@File     : sort.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/3/15 17:18
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/15 17:18        1.0             None
"""
import threading
import time

from numpy.random import randint
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import QLabel

from sort import sort_view


class BubbleSortView(sort_view.ListSortWidget):
    def __init__(self, parent=None):
        super(BubbleSortView, self).__init__(parent)

        # 排序规则说明区
        label_list = [
            QLabel('循环 -> i 从 1 到 arr.length - 1:'),
            QLabel('    循环 -> j 从 0 到 arr.length - i:'),
            QLabel('        如果 -> arr[j] > arr[j+1]:'),
            QLabel('            交换位置: (arr[j], arr[j+1])'),
        ]
        font = QFont()
        font.setPointSize(13)
        for i in label_list:
            i.setFont(font)
            i.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.add_text(label_list)

    def sorted(self):
        # 重置颜色
        self.draw_widget.reset_draw_list()
        self.text_view.append('外层循环: i 从 1 到 %d' % (len(self.arr) - 1))

        for i in range(1, len(self.draw_widget.arr)):

            self.text_list[0].setStyleSheet('background-color: rgb(0, 191, 255);')
            time.sleep(0.05)
            self.text_list[0].setStyleSheet('background-color: rgb(255, 255, 255);')

            self.text_view.append('    内层循环: j 从 0 到 %d' % (len(self.draw_widget.arr) - i))
            self.text_view.moveCursor(QTextCursor.End)

            for j in range(len(self.draw_widget.arr) - i):
                self.text_list[1].setStyleSheet('background-color: rgb(0, 191, 255);')
                time.sleep(0.05)
                self.text_list[1].setStyleSheet('background-color: rgb(255, 255, 255);')

                # 对比两数
                self.draw_widget.draw_list[j]['rect_brush_color'] = self.draw_widget.act_rect_color1
                self.draw_widget.draw_list[j + 1]['rect_brush_color'] = self.draw_widget.act_rect_color2
                self.draw_widget.update()
                self.text_list[2].setStyleSheet('background-color: rgb(0, 191, 255);')
                self.text_view.append(
                    '        判断: arr[%d]=%d > arr[%d]=%d ' %
                    (j, self.draw_widget.arr[j], j + 1, self.draw_widget.arr[j + 1])
                )
                self.text_view.moveCursor(QTextCursor.End)

                time.sleep(self.draw_widget.action_speed)
                self.text_list[2].setStyleSheet('background-color: rgb(255, 255, 255);')

                # 交换两数
                if self.draw_widget.arr[j] > self.draw_widget.arr[j + 1]:
                    self.text_list[3].setStyleSheet('background-color: rgb(0, 191, 255);')
                    self.text_view.append('          交换两数位置')
                    self.draw_widget.swap_pos(j, j + 1)
                    while self.draw_widget.acting:
                        time.sleep(self.draw_widget.action_speed)
                    self.text_list[3].setStyleSheet('background-color: rgb(255, 255, 255);')

                # 恢复活动区域颜色
                self.draw_widget.draw_list[j]['rect_brush_color'] = self.draw_widget.default_rect_color
                self.draw_widget.update()

            # 排序完成的颜色
            self.draw_widget.draw_list[len(self.draw_widget.arr) - i]['rect_brush_color'] = \
                self.draw_widget.finished_rect_color
            self.draw_widget.update()

        # 排序完成，给首个元素染色
        self.draw_widget.draw_list[0]['rect_brush_color'] = self.draw_widget.finished_rect_color
        self.draw_widget.update()
        # 设置释放按钮
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.button3.setEnabled(True)

    def start_sort(self):
        thread = threading.Thread(target=self.sorted, daemon=True)
        thread.start()


class InsertSortView(sort_view.ListSortWidget):
    def __init__(self, parent=None):
        super(InsertSortView, self).__init__(parent)

        # 排序规则说明区
        label_list = [
            QLabel('循环 -> i 从 1 到 arr.length - 1:'),
            QLabel('    循环 -> j 从 i 到 1:'),
            QLabel('        如果 -> arr[j] < arr[j-1]:'),
            QLabel('            交换位置: (arr[j], arr[j-1])'),
            QLabel('        否则：退出内层循环'),
        ]
        font = QFont()
        font.setPointSize(13)
        for i in label_list:
            i.setFont(font)
            i.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.add_text(label_list)

    def sorted(self):
        # 重置颜色
        self.draw_widget.reset_draw_list()
        self.text_view.append('外层循环: i 从 1 到 %d' % (len(self.arr) - 1))

        for i in range(1, len(self.draw_widget.arr)):

            self.text_list[0].setStyleSheet('background-color: rgb(0, 191, 255);')
            time.sleep(0.05)
            self.text_list[0].setStyleSheet('background-color: rgb(255, 255, 255);')

            self.text_view.append('    内层循环: j 从 %d 到 1' % i)
            self.text_view.moveCursor(QTextCursor.End)

            for j in range(i, 0, -1):
                self.text_list[1].setStyleSheet('background-color: rgb(0, 191, 255);')
                time.sleep(0.05)
                self.text_list[1].setStyleSheet('background-color: rgb(255, 255, 255);')

                # 对比两数
                self.draw_widget.draw_list[j]['rect_brush_color'] = self.draw_widget.act_rect_color1
                self.draw_widget.draw_list[j - 1]['rect_brush_color'] = self.draw_widget.act_rect_color2
                self.draw_widget.update()
                self.text_list[2].setStyleSheet('background-color: rgb(0, 191, 255);')
                self.text_view.append(
                    '        判断: arr[%d]=%d < arr[%d]=%d ' %
                    (j, self.draw_widget.arr[j], j - 1, self.draw_widget.arr[j - 1])
                )
                self.text_view.moveCursor(QTextCursor.End)

                time.sleep(self.draw_widget.action_speed)
                self.text_list[2].setStyleSheet('background-color: rgb(255, 255, 255);')

                # 交换两数
                if self.draw_widget.arr[j] < self.draw_widget.arr[j - 1]:
                    self.text_list[3].setStyleSheet('background-color: rgb(0, 191, 255);')
                    self.text_view.append('          交换两数位置')
                    self.draw_widget.swap_pos(j, j - 1)
                    while self.draw_widget.acting:
                        time.sleep(self.draw_widget.action_speed)
                    self.text_list[3].setStyleSheet('background-color: rgb(255, 255, 255);')
                else:
                    # 文本
                    self.text_list[4].setStyleSheet('background-color: rgb(0, 191, 255);')
                    self.text_view.append('          退出内层循环')
                    time.sleep(0.05)
                    self.text_list[4].setStyleSheet('background-color: rgb(255, 255, 255);')
                    # 活动颜色
                    self.draw_widget.draw_list[j]['rect_brush_color'] = self.draw_widget.finished_rect_color
                    self.draw_widget.draw_list[j-1]['rect_brush_color'] = self.draw_widget.finished_rect_color
                    break

                # 恢复活动区域颜色
                self.draw_widget.draw_list[j]['rect_brush_color'] = self.draw_widget.finished_rect_color
                self.draw_widget.update()

            # 排序完成的颜色
            self.draw_widget.draw_list[0]['rect_brush_color'] = self.draw_widget.finished_rect_color
            self.draw_widget.update()

        # 设置释放按钮
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.button3.setEnabled(True)

    def start_sort(self):
        thread = threading.Thread(target=self.sorted, daemon=True)
        thread.start()


class SelectSortView(sort_view.ListSortWidget):
    def __init__(self, parent=None):
        super(SelectSortView, self).__init__(parent)

        # 排序规则说明区
        label_list = [
            QLabel('循环 -> i 从 0 到 arr.length - 2:'),
            QLabel('    设置最小值下标 min_index = i'),
            QLabel('    循环 -> j 从 i+1 到 arr.length:'),
            QLabel('        如果 -> arr[j] < arr[min_index]:'),
            QLabel('            修改 min_index = j'),
            QLabel('    交换位置: (arr[i], arr[min_index])'),
        ]
        font = QFont()
        font.setPointSize(13)
        for i in label_list:
            i.setFont(font)
            i.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.add_text(label_list)

    def sorted(self):
        # 重置颜色
        self.draw_widget.reset_draw_list()
        self.text_view.append('外层循环: i 从 0 到 %d' % (len(self.arr) - 2))

        for i in range(len(self.draw_widget.arr)):

            self.text_list[0].setStyleSheet('background-color: rgb(0, 191, 255);')
            time.sleep(0.05)
            self.text_list[0].setStyleSheet('background-color: rgb(255, 255, 255);')

            min_index = i
            self.text_view.append('    设置最小值下标 min_index = %d' % i)
            self.text_list[1].setStyleSheet('background-color: rgb(0, 191, 255);')
            self.draw_widget.draw_list[min_index]['rect_brush_color'] = self.draw_widget.act_rect_color2
            time.sleep(0.05)
            self.text_list[1].setStyleSheet('background-color: rgb(255, 255, 255);')

            self.text_view.append('    内层循环: j 从 i+1 到 %d' % (len(self.arr) - 1))

            for j in range(i + 1, len(self.arr)):
                self.text_list[2].setStyleSheet('background-color: rgb(0, 191, 255);')
                time.sleep(0.05)
                self.text_list[2].setStyleSheet('background-color: rgb(255, 255, 255);')

                # 对比两数
                self.draw_widget.draw_list[j]['rect_brush_color'] = self.draw_widget.act_rect_color1
                self.draw_widget.update()
                self.text_list[3].setStyleSheet('background-color: rgb(0, 191, 255);')
                self.text_view.append(
                    '        判断: arr[%d]=%d < arr[%d]=%d ' %
                    (j, self.draw_widget.arr[j], min_index, self.draw_widget.arr[min_index])
                )
                self.text_view.moveCursor(QTextCursor.End)

                time.sleep(self.draw_widget.action_speed)
                self.text_list[3].setStyleSheet('background-color: rgb(255, 255, 255);')

                # 交换最小值下标
                if self.draw_widget.arr[j] < self.draw_widget.arr[min_index]:
                    self.text_list[4].setStyleSheet('background-color: rgb(0, 191, 255);')
                    self.text_view.append('          修改 min_index = %d' % j)
                    self.draw_widget.draw_list[min_index]['rect_brush_color'] = self.draw_widget.default_rect_color
                    self.draw_widget.draw_list[j]['rect_brush_color'] = self.draw_widget.act_rect_color2
                    min_index = j
                    time.sleep(self.draw_widget.action_speed)
                    self.text_list[4].setStyleSheet('background-color: rgb(255, 255, 255);')
                else:
                    # 恢复活动区域颜色
                    self.draw_widget.draw_list[j]['rect_brush_color'] = self.draw_widget.default_rect_color
                    self.draw_widget.update()
            # 找到最小值 交换位置
            self.text_list[5].setStyleSheet('background-color: rgb(0, 191, 255);')
            self.text_view.append('    交换arr[%d] 和 arr[%d]' % (i, min_index))
            self.text_view.moveCursor(QTextCursor.End)
            if min_index == i:
                time.sleep(self.draw_widget.action_speed)
            else:
                self.draw_widget.swap_pos(min_index, i)
                while self.draw_widget.acting:
                    time.sleep(self.draw_widget.action_speed)
            self.text_list[5].setStyleSheet('background-color: rgb(255, 255, 255);')

            # 排序完成的颜色
            self.draw_widget.draw_list[i]['rect_brush_color'] = self.draw_widget.finished_rect_color
            self.draw_widget.update()
        # 排序完成 给最后的数据染色
        self.draw_widget.draw_list[-1]['rect_brush_color'] = self.draw_widget.finished_rect_color
        self.draw_widget.update()
        # 设置释放按钮
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.button3.setEnabled(True)

    def start_sort(self):
        thread = threading.Thread(target=self.sorted, daemon=True)
        thread.start()


class QuickSortView(sort_view.ListSortWidget):
    def __init__(self, parent=None):
        super(QuickSortView, self).__init__(parent)

        # 排序规则说明区
        label_list = [
            QLabel('定义函数 快速排序(参数: left, 参数: right):'),
            QLabel('    如果 left　>= right:   退出函数'),
            QLabel('    设: median = left, i = left + 1, j = right'),
            QLabel('    循环1: 当 i <= j 时:'),
            QLabel('        如果 arr[j] < arr[median]: 否则: j--'),
            QLabel('           交换 arr[j], arr[median]'),
            QLabel('           median = j, j--, 切换到: 循环2'),
            QLabel('    循环2: 当 i <= j 时:'),
            QLabel('        如果 arr[i] > arr[median]: 否则: i++'),
            QLabel('           交换 arr[i], arr[median]'),
            QLabel('           median = i, i++, 切换到: 循环1'),
            QLabel('    调用函数 快速排序(left, median - 1)'),
            QLabel('    调用函数 快速排序(median + 1, right)')
        ]
        font = QFont()
        font.setPointSize(13)
        for i in label_list:
            i.setFont(font)
            i.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.add_text(label_list)

    def sorted(self, left, right, deep=0):
        # text_widget
        self.text_list[1].setStyleSheet('background-color: rgb(0, 191, 255);')
        time.sleep(0.05)
        if left >= right:
            self.text_view.append('  [left, right] = [%d, %d], left >= right, 退出递归' % (left, right))
            self.text_view.moveCursor(QTextCursor.End)
            if left == right:
                self.draw_widget.draw_list[left]['rect_brush_color'] = self.draw_widget.finished_rect_color
                self.draw_widget.update()
                time.sleep(self.draw_widget.action_speed)
                self.text_list[1].setStyleSheet('background-color: rgb(255, 255, 255);')
                time.sleep(0.05)
            return

        self.text_list[1].setStyleSheet('background-color: rgb(255, 255, 255);')
        self.text_list[2].setStyleSheet('background-color: rgb(0, 191, 255);')

        median = left
        i = left + 1
        j = right
        # 说明信息
        self.text_view.append('    media = left, i = left + 1, j = right, 其中 left = %d, right = %d' % (left, right))
        # 染色
        self.draw_widget.draw_list[median]['rect_brush_color'] = self.draw_widget.median_color
        self.update()
        time.sleep(0.05)
        self.text_list[2].setStyleSheet('background-color: rgb(255, 255, 255);')

        while i <= j:
            self.text_list[3].setStyleSheet('background-color: rgb(0, 191, 255);')
            time.sleep(0.05)
            self.text_list[3].setStyleSheet('background-color: rgb(255, 255, 255);')
            self.text_list[4].setStyleSheet('background-color: rgb(0, 191, 255);')

            self.draw_widget.draw_list[j]['rect_brush_color'] = self.draw_widget.act_rect_color2
            self.draw_widget.update()
            time.sleep(self.draw_widget.action_speed)
            self.text_list[4].setStyleSheet('background-color: rgb(255, 255, 255);')

            if self.draw_widget.arr[j] < self.draw_widget.arr[median]:

                # 说明信息
                self.text_view.append('         arr[j] < arr[median], 交换两数位置, media = j, j--， 切换遍历方向')
                self.text_view.moveCursor(QTextCursor.End)

                self.text_list[5].setStyleSheet('background-color: rgb(0, 191, 255);')

                # 交换
                self.draw_widget.swap_pos(j, median)
                # 等待交换动作完成
                while self.draw_widget.acting:
                    time.sleep(self.draw_widget.action_speed)
                self.text_list[5].setStyleSheet('background-color: rgb(255, 255, 255);')

                # 修改下标
                self.text_list[6].setStyleSheet('background-color: rgb(0, 191, 255);')
                # 染色
                self.draw_widget.draw_list[median]['rect_brush_color'] = self.draw_widget.default_rect_color
                self.draw_widget.update()
                time.sleep(0.05)
                self.text_list[6].setStyleSheet('background-color: rgb(255, 255, 255);')
                median = j
                j -= 1

                while i <= j:
                    self.text_list[7].setStyleSheet('background-color: rgb(0, 191, 255);')
                    time.sleep(0.05)
                    self.text_list[7].setStyleSheet('background-color: rgb(255, 255, 255);')
                    self.text_list[8].setStyleSheet('background-color: rgb(0, 191, 255);')

                    self.draw_widget.draw_list[i]['rect_brush_color'] = self.draw_widget.act_rect_color1
                    self.draw_widget.update()
                    time.sleep(self.draw_widget.action_speed)
                    self.text_list[8].setStyleSheet('background-color: rgb(255, 255, 255);')

                    if self.draw_widget.arr[i] > self.draw_widget.arr[median]:

                        self.text_view.append('         arr[i] > arr[median], 交换两数位置, media = i, i++, 切换遍历方向')
                        self.text_view.moveCursor(QTextCursor.End)

                        self.text_list[9].setStyleSheet('background-color: rgb(0, 191, 255);')

                        self.draw_widget.swap_pos(i, median)
                        # 等待交换动作完成
                        while self.draw_widget.acting:
                            time.sleep(self.draw_widget.action_speed)

                        self.text_list[9].setStyleSheet('background-color: rgb(255, 255, 255);')

                        # 修改下标
                        self.text_list[10].setStyleSheet('background-color: rgb(0, 191, 255);')
                        # 染色
                        self.draw_widget.draw_list[median]['rect_brush_color'] = self.draw_widget.default_rect_color
                        self.draw_widget.update()
                        time.sleep(0.05)
                        self.text_list[10].setStyleSheet('background-color: rgb(255, 255, 255);')
                        median = i
                        i += 1
                        break
                    else:
                        self.draw_widget.draw_list[i]['rect_brush_color'] = self.draw_widget.default_rect_color
                        self.draw_widget.update()
                        i += 1
                        self.text_view.append('         arr[i] <= arr[median], i++')
                        self.text_view.moveCursor(QTextCursor.End)
            else:
                self.draw_widget.draw_list[j]['rect_brush_color'] = self.draw_widget.default_rect_color
                self.draw_widget.update()
                j -= 1
                self.text_view.append('         arr[j] >= arr[median], j--')
                self.text_view.moveCursor(QTextCursor.End)

        # 排序完后， 递归
        self.text_view.append('位置%d已完成排序' % median)
        self.text_view.moveCursor(QTextCursor.End)
        self.draw_widget.draw_list[median]['rect_brush_color'] = self.draw_widget.finished_rect_color
        self.show()
        time.sleep(self.draw_widget.action_speed)

        self.text_list[11].setStyleSheet('background-color: rgb(0, 191, 255);')
        time.sleep(0.05)
        self.text_list[11].setStyleSheet('background-color: rgb(255, 255, 255);')
        self.text_view.append('  递归排序[%d, %d]' % (left, median - 1))
        self.sorted(left, median - 1, deep+1)

        self.text_list[12].setStyleSheet('background-color: rgb(0, 191, 255);')
        time.sleep(0.05)
        self.text_list[12].setStyleSheet('background-color: rgb(255, 255, 255);')
        self.text_view.append('  递归排序[%d, %d]' % (median + 1, right))
        self.sorted(median + 1, right, deep+1)

        # 取消按钮限制
        if deep == 0:
            self.button1.setEnabled(True)
            self.button2.setEnabled(True)
            self.button3.setEnabled(True)

    def start_sort(self):
        thread = threading.Thread(target=self.sorted, args=(0, len(self.arr) - 1), daemon=True)
        thread.start()


class RandomQuickSortView(sort_view.ListSortWidget):

    def __init__(self, parent=None):
        super(RandomQuickSortView, self).__init__(parent)

        # 排序规则说明区
        label_list = [
            QLabel('定义函数 快速排序(参数: left, 参数: right):'),
            QLabel('    如果 left　>= right:   退出函数'),
            QLabel('    随机从[left, right]中选取一个数, 与left交换'),
            QLabel('    设: median = left, i = left + 1, j = right'),
            QLabel('    循环1: 当 i <= j 时:'),
            QLabel('        如果 arr[j] < arr[median]: 否则: j--'),
            QLabel('           交换 arr[j], arr[median]'),
            QLabel('           median = j, j--, 切换到: 循环2'),
            QLabel('    循环2: 当 i <= j 时:'),
            QLabel('        如果 arr[i] > arr[median]: 否则: i++'),
            QLabel('           交换 arr[i], arr[median]'),
            QLabel('           median = i, i++, 切换到: 循环1'),
            QLabel('    调用函数 快速排序(left, median - 1)'),
            QLabel('    调用函数 快速排序(median + 1, right)')
        ]
        font = QFont()
        font.setPointSize(13)
        for i in label_list:
            i.setFont(font)
            i.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.add_text(label_list)

    def sorted(self, left, right, deep=0):
        # text_widget
        self.text_list[1].setStyleSheet('background-color: rgb(0, 191, 255);')
        time.sleep(0.05)
        if left >= right:
            self.text_view.append('  [left, right] = [%d, %d], left >= right, 退出递归' % (left, right))
            self.text_view.moveCursor(QTextCursor.End)
            if left == right:
                self.draw_widget.draw_list[left]['rect_brush_color'] = self.draw_widget.finished_rect_color
                self.draw_widget.update()
                time.sleep(self.draw_widget.action_speed)
                self.text_list[1].setStyleSheet('background-color: rgb(255, 255, 255);')
                time.sleep(0.05)
            return

        self.text_list[1].setStyleSheet('background-color: rgb(255, 255, 255);')

        median = randint(left, right + 1)
        # 染色
        self.draw_widget.draw_list[median]['rect_brush_color'] = self.draw_widget.median_color
        self.text_list[2].setStyleSheet('background-color: rgb(0, 191, 255);')
        self.text_view.append('  从[%d, %d]中随机选取: %d' % (left, right, median))
        self.update()
        time.sleep(0.05)
        self.draw_widget.swap_pos(median, left)
        while self.draw_widget.acting:
            time.sleep(self.draw_widget.action_speed)
        self.text_list[2].setStyleSheet('background-color: rgb(255, 255, 255);')

        self.text_list[3].setStyleSheet('background-color: rgb(0, 191, 255);')
        median = left
        i = left + 1
        j = right
        # 说明信息
        self.text_view.append('    media = left, i = left + 1, j = right, 其中 left = %d, right = %d' % (left, right))
        time.sleep(0.05)
        self.text_list[3].setStyleSheet('background-color: rgb(255, 255, 255);')

        while i <= j:
            self.text_list[4].setStyleSheet('background-color: rgb(0, 191, 255);')
            time.sleep(0.05)
            self.text_list[4].setStyleSheet('background-color: rgb(255, 255, 255);')
            self.text_list[5].setStyleSheet('background-color: rgb(0, 191, 255);')

            self.draw_widget.draw_list[j]['rect_brush_color'] = self.draw_widget.act_rect_color2
            self.draw_widget.update()
            time.sleep(self.draw_widget.action_speed)
            self.text_list[5].setStyleSheet('background-color: rgb(255, 255, 255);')

            if self.draw_widget.arr[j] < self.draw_widget.arr[median]:

                # 说明信息
                self.text_view.append('         arr[j] < arr[median], 交换两数位置, media = j, j--， 切换遍历方向')
                self.text_view.moveCursor(QTextCursor.End)

                self.text_list[6].setStyleSheet('background-color: rgb(0, 191, 255);')

                # 交换
                self.draw_widget.swap_pos(j, median)
                # 等待交换动作完成
                while self.draw_widget.acting:
                    time.sleep(self.draw_widget.action_speed)
                self.text_list[6].setStyleSheet('background-color: rgb(255, 255, 255);')

                # 修改下标
                self.text_list[7].setStyleSheet('background-color: rgb(0, 191, 255);')
                # 染色
                self.draw_widget.draw_list[median]['rect_brush_color'] = self.draw_widget.default_rect_color
                self.draw_widget.update()
                time.sleep(0.05)
                self.text_list[7].setStyleSheet('background-color: rgb(255, 255, 255);')
                median = j
                j -= 1

                while i <= j:
                    self.text_list[8].setStyleSheet('background-color: rgb(0, 191, 255);')
                    time.sleep(0.05)
                    self.text_list[8].setStyleSheet('background-color: rgb(255, 255, 255);')
                    self.text_list[9].setStyleSheet('background-color: rgb(0, 191, 255);')

                    self.draw_widget.draw_list[i]['rect_brush_color'] = self.draw_widget.act_rect_color1
                    self.draw_widget.update()
                    time.sleep(self.draw_widget.action_speed)
                    self.text_list[9].setStyleSheet('background-color: rgb(255, 255, 255);')

                    if self.draw_widget.arr[i] > self.draw_widget.arr[median]:

                        self.text_view.append('         arr[i] > arr[median], 交换两数位置, media = i, i++, 切换遍历方向')
                        self.text_view.moveCursor(QTextCursor.End)

                        self.text_list[10].setStyleSheet('background-color: rgb(0, 191, 255);')

                        self.draw_widget.swap_pos(i, median)
                        # 等待交换动作完成
                        while self.draw_widget.acting:
                            time.sleep(self.draw_widget.action_speed)

                        self.text_list[10].setStyleSheet('background-color: rgb(255, 255, 255);')

                        # 修改下标
                        self.text_list[11].setStyleSheet('background-color: rgb(0, 191, 255);')
                        # 染色
                        self.draw_widget.draw_list[median]['rect_brush_color'] = self.draw_widget.default_rect_color
                        self.draw_widget.update()
                        time.sleep(0.05)
                        self.text_list[11].setStyleSheet('background-color: rgb(255, 255, 255);')
                        median = i
                        i += 1
                        break
                    else:
                        self.draw_widget.draw_list[i]['rect_brush_color'] = self.draw_widget.default_rect_color
                        self.draw_widget.update()
                        i += 1
                        self.text_view.append('         arr[i] <= arr[median], i++')
                        self.text_view.moveCursor(QTextCursor.End)
            else:
                self.draw_widget.draw_list[j]['rect_brush_color'] = self.draw_widget.default_rect_color
                self.draw_widget.update()
                j -= 1
                self.text_view.append('         arr[j] >= arr[median], j--')
                self.text_view.moveCursor(QTextCursor.End)

        # 排序完后， 递归
        self.text_view.append('位置%d已完成排序' % median)
        self.text_view.moveCursor(QTextCursor.End)
        self.draw_widget.draw_list[median]['rect_brush_color'] = self.draw_widget.finished_rect_color
        self.show()
        time.sleep(self.draw_widget.action_speed)

        self.text_list[12].setStyleSheet('background-color: rgb(0, 191, 255);')
        time.sleep(0.05)
        self.text_list[12].setStyleSheet('background-color: rgb(255, 255, 255);')
        self.text_view.append('  递归排序[%d, %d]' % (left, median - 1))
        self.sorted(left, median - 1, deep+1)

        self.text_list[12].setStyleSheet('background-color: rgb(0, 191, 255);')
        time.sleep(0.05)
        self.text_list[12].setStyleSheet('background-color: rgb(255, 255, 255);')
        self.text_view.append('  递归排序[%d, %d]' % (median + 1, right))
        self.sorted(median + 1, right, deep+1)

        # 取消按钮限制
        if deep == 0:
            self.button1.setEnabled(True)
            self.button2.setEnabled(True)
            self.button3.setEnabled(True)

    def start_sort(self):
        thread = threading.Thread(target=self.sorted, args=(0, len(self.arr) - 1), daemon=True)
        thread.start()


class MergeSortView(sort_view.DoubleSortWidget):
    def __init__(self, parent=None):
        super(MergeSortView, self).__init__(parent)

        # 排序规则说明区
        label_list = [
            QLabel('将数组拆分为大小为一的分区'),
            QLabel('递归地合并相邻的分区'),
            QLabel('    遍历：如果左侧首个值 <= 右侧首个值：'),
            QLabel('             拷贝左侧首个值'),
            QLabel('         否则: 拷贝右侧首个值'),
            QLabel('    将有序数组放进原来的数组中')
        ]
        font = QFont()
        font.setPointSize(13)
        for i in label_list:
            i.setFont(font)
            # i.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.add_text(label_list)

        # Warning: 过多的修改Sheet会导致程序崩溃

    def sorted(self, left, right, deep=True):
        if left >= right:
            return

        mid = left + (right - left) // 2
        self.sorted(left, mid, False)
        self.sorted(mid+1, right, False)
        #
        self.text_view.append('合并分区[%d, %d], [%d, %d]' % (left, mid, mid+1, right))
        # self.text_list[1].setStyleSheet('background-color: rgb(0, 191, 255);')
        i, j = left, mid + 1
        for k in range(left, j):
            self.draw_widget.draw_list[k]['rect_brush_color'] = self.draw_widget.act_rect_color1
        for k in range(j, right + 1):
            self.draw_widget.draw_list[k]['rect_brush_color'] = self.draw_widget.act_rect_color2
        self.update()
        time.sleep(self.draw_widget.action_speed)
        # self.text_list[1].setStyleSheet('background-color: rgb(255, 255, 255);')
        # self.text_list[2].setStyleSheet('background-color: rgb(0, 191, 255);')
        for k in range(left, right+1):
            if i > mid:
                self.text_view.append('    左侧区域无元素, 拷贝右侧元素[%d]' % self.draw_widget.arr[j])
                # self.text_list[4].setStyleSheet('background-color: rgb(0, 191, 255);')
                self.draw_widget.merge_pop(j, k)
                j += 1
            elif j > right:
                self.text_view.append('    右侧区域无元素, 拷贝左侧元素[%d]' % self.draw_widget.arr[i])
                # self.text_list[3].setStyleSheet('background-color: rgb(0, 191, 255);')
                self.draw_widget.merge_pop(i, k)
                i += 1
            elif self.draw_widget.arr[i] > self.draw_widget.arr[j]:
                self.text_view.append('    左侧元素[%d]大于右侧元素[%d], 拷贝右侧元素' %
                                      (self.draw_widget.arr[i], self.draw_widget.arr[j]))
                # self.text_list[4].setStyleSheet('background-color: rgb(0, 191, 255);')
                self.draw_widget.merge_pop(j, k)
                j += 1
            else:
                self.text_view.append('    左侧元素[%d]小于或等于右侧元素[%d], 拷贝左侧元素' %
                                      (self.draw_widget.arr[i], self.draw_widget.arr[j]))
                # self.text_list[3].setStyleSheet('background-color: rgb(0, 191, 255);')
                self.draw_widget.merge_pop(i, k)
                i += 1
            while self.draw_widget.acting:
                time.sleep(self.draw_widget.action_speed)
            # self.text_list[3].setStyleSheet('background-color: rgb(255, 255, 255);')
            # self.text_list[4].setStyleSheet('background-color: rgb(255, 255, 255);')

        # self.text_list[2].setStyleSheet('background-color: rgb(255, 255, 255);')
        # self.text_list[5].setStyleSheet('background-color: rgb(0, 191, 255);')
        self.text_view.append('    将有序数组放进原来的数组中...')
        self.text_view.moveCursor(QTextCursor.End)

        self.draw_widget.merge_add(left)
        while self.draw_widget.acting:
            time.sleep(self.draw_widget.action_speed)
        # self.text_list[5].setStyleSheet('background-color: rgb(255, 255, 255);')

        if deep:
            self.text_view.append('    排序完成！')
            self.text_view.moveCursor(QTextCursor.End)
            self.button1.setEnabled(True)
            self.button2.setEnabled(True)
            self.button3.setEnabled(True)

    def start_sort(self):
        thread = threading.Thread(target=self.sorted, args=(0, len(self.arr) - 1), daemon=True)
        thread.start()


class CountSortView(sort_view.BlockSortWidget):
    def __init__(self, parent=None):
        super(CountSortView, self).__init__(parent)
        # 取消textView
        self.text_view.close()
        # 排序规则说明区
        label_list = [
            QLabel('创建计数数组'),
            QLabel('遍历数列中的每个元素，相应位置的计数器增加 1'),
            QLabel(''),
            QLabel('每轮计数，都从最小的值开始'),
            QLabel('当计数为非零数时, 将元素存储于列表'),
            QLabel('计数减1')
        ]
        font = QFont()
        font.setPointSize(13)
        for i in label_list:
            i.setFont(font)
        self.add_text(label_list)

    def sorted(self):
        self.text_list[1].setStyleSheet('background-color: rgb(0, 191, 255);')

        for i in range(len(self.draw_widget.arr)):
            self.draw_widget.add_signal.emit(i, self.draw_widget.arr[i])
            time.sleep(self.draw_widget.action_speed / 1000 + 0.05)

        self.text_list[1].setStyleSheet('')

        self.text_list[3].setStyleSheet('background-color: rgb(0, 191, 255);')
        self.text_list[4].setStyleSheet('background-color: rgb(0, 191, 255);')
        self.text_list[5].setStyleSheet('background-color: rgb(0, 191, 255);')
        self.draw_widget.slot_pop_animation()
        time.sleep(len(self.arr) * self.draw_widget.action_speed / 1000)
        self.text_list[3].setStyleSheet('')
        self.text_list[4].setStyleSheet('')
        self.text_list[5].setStyleSheet('')
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.button3.setEnabled(True)

    def start_sort(self):
        self.draw_widget._no_act = False
        thread = threading.Thread(target=self.sorted, daemon=True)
        thread.start()


class RadixSortView(sort_view.BlockSortWidget):
    def __init__(self, parent=None):
        super(RadixSortView, self).__init__(parent, 10000)
        # 取消textView
        self.text_view.close()
        # 排序规则说明区
        label_list = [
            QLabel('创建10个(0~9)桶(数组)'),
            QLabel('每次遍历从低位向高位取值 ()'),
            QLabel('  按照该位上的数, 将元素移至相应的桶中'),
            QLabel('  （按照该位上的数对数组进行稳定排序）'),
            QLabel(' '),
            QLabel('在每个桶中，从最小的数位开始'),
            QLabel('当桶不是空的, 将元素恢复至数列中')
        ]
        font = QFont()
        font.setPointSize(13)
        for i in label_list:
            i.setFont(font)
        self.add_text(label_list)

    def sorted(self):

        for j in range(len(str(max(self.arr)))-1, -1, -1):
            self.text_list[1].setText(
                '每次遍历从低位向高位取值 (当前按照%s排序)' % ['千位', '百位', '十位', '个位'][j+4-len(str(max(self.arr)))]
            )
            self.text_list[1].setStyleSheet('background-color: rgb(0, 191, 255);')
            time.sleep(self.draw_widget.action_speed / 1000)
            self.text_list[1].setStyleSheet('')

            self.text_list[2].setStyleSheet('background-color: rgb(0, 191, 255);')
            self.text_list[3].setStyleSheet('background-color: rgb(0, 191, 255);')
            for i in range(len(self.draw_widget.arr)):
                sss = format(self.draw_widget.arr[i], '0%dd' % len(str(max(self.arr))))
                self.draw_widget.add_signal.emit(i, int(sss[j]))
                time.sleep(self.draw_widget.action_speed / 1000 + 0.05)

            self.text_list[2].setStyleSheet('')
            self.text_list[3].setStyleSheet('')
            self.text_list[5].setStyleSheet('background-color: rgb(0, 191, 255);')
            self.text_list[6].setStyleSheet('background-color: rgb(0, 191, 255);')

            self.draw_widget.slot_pop_animation()
            time.sleep(len(self.arr) * (self.draw_widget.action_speed + 0.05) / 1000 + 1)

            self.text_list[5].setStyleSheet('')
            self.text_list[6].setStyleSheet('')

        self.text_list[1].setText('每次遍历从低位向高位取值 ()')
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.button3.setEnabled(True)

    def start_sort(self):
        self.draw_widget._no_act = False
        thread = threading.Thread(target=self.sorted, daemon=True)
        thread.start()
