"""
@File     : tree.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/3/13 20:00
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/13 20:00        1.0             None
"""
import math
import threading
import time

from PyQt5.QtCore import pyqtSignal, QRectF, QPointF, Qt
from PyQt5.QtGui import QFont, QPainter, QColor, QPen
from PyQt5.QtWidgets import QPushButton, QGridLayout, QTextBrowser, QVBoxLayout, QDialog, QWidget, QInputDialog, \
    QApplication, QLabel, QMessageBox

import sys


class TreeWidget(QWidget):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)

        # 树数据
        self.tree = MyTree()
        # 屏幕控制数据
        self.text_view = QTextBrowser()
        self.speed = 0.8

        self.__init_data()
        self.__init_ui()

    def __init_data(self):
        pass

    def __add_node(self):
        pass

    def __init_ui(self):
        right_layout = QVBoxLayout()
        right_layout.addLayout(self.__button_layout())
        right_layout.addWidget(self.text_view)

        main_layout = QGridLayout()
        main_layout.addWidget(self.tree, 0, 0)
        main_layout.addLayout(right_layout, 0, 1)
        main_layout.setColumnStretch(0, 5)
        main_layout.setColumnStretch(1, 2)
        self.setLayout(main_layout)

    def __button_layout(self):
        button1 = QPushButton('添加结点')
        button2 = QPushButton('删除结点')
        button3 = QPushButton('初始化')
        button4 = QPushButton('深度优先搜索')
        button5 = QPushButton('广度优先搜索')
        button6 = QPushButton('转换二叉树')
        button7 = QPushButton('设置速度')
        self.label1 = QLabel('结点数量: %d' % self.tree.tree_nodes)
        self.label2 = QLabel('树的高度：%d' % self.tree.tree_deep)

        button1.clicked.connect(self.click_btn1)
        button2.clicked.connect(self.click_btn2)
        button3.clicked.connect(self.click_btn3)
        button4.clicked.connect(self.click_btn4)
        button5.clicked.connect(self.click_btn5)
        button6.clicked.connect(self.click_btn6)
        button7.clicked.connect(self.click_btn7)
        # 站位按钮
        btn1 = QPushButton()
        btn2 = QPushButton()
        btn1.setStyleSheet("""QPushButton{border: 0;}""")
        btn2.setStyleSheet("""QPushButton{border: 0;}""")

        layout = QGridLayout()
        layout.addWidget(btn1, 0, 0, 1, 2)
        layout.addWidget(btn2, 5, 0, 1, 2)
        layout.addWidget(button1, 1, 0)
        layout.addWidget(button2, 2, 0)
        layout.addWidget(button3, 3, 0)
        layout.addWidget(button4, 1, 1)
        layout.addWidget(button5, 2, 1)
        layout.addWidget(button6, 3, 1)
        layout.addWidget(button7, 4, 0, 1, 2)
        layout.addWidget(self.label1, 5, 0)
        layout.addWidget(self.label2, 5, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)

        return layout

    def click_btn1(self):
        li = []  # ItemList
        for i in range(self.tree.max_nodes):
            if i not in self.tree.unused_node:
                li.append(chr(i + 65))
        ch, ok = QInputDialog.getItem(self, '添加结点', '选择添加结点的父节点', li, self.tree.tree_nodes - 1, False)
        if ok:
            par = ord(ch) - 65
            flag = self.tree.add_node(par)
            if flag is False:
                QMessageBox.warning(self, '警告', '树的高度超出限制！', QMessageBox.Ok)
            else:
                self.label1.setText('结点数量: %d' % self.tree.tree_nodes)
                self.label2.setText('树的高度: %d' % self.tree.tree_deep)
                self.text_view.append('添加结点:%s' % chr(self.tree.tree_list[par][-1] + 65))

    def click_btn2(self):
        li = []  # ItemList
        for i in range(1, 26):
            if len(self.tree.tree_list[i]) == 1:
                li.append(chr(i + 65))
        if len(li) > 0:
            ch, ok = QInputDialog.getItem(self, '删除结点', '选择要删除的结点', li, len(li) - 1, False)
            if ok:
                nod = ord(ch) - 65
                flag = self.tree.del_node(nod)
                self.label1.setText('结点数量: %d' % self.tree.tree_nodes)
                self.label2.setText('树的高度: %d' % self.tree.tree_deep)
                self.text_view.append('删除结点:%s' % chr(nod + 65))
        else:
            QMessageBox.warning(self, '警告', '无叶子结点！', QMessageBox.Ok)

    def click_btn3(self):
        self.tree.reset()
        self.text_view.clear()

    def click_btn4(self):
        """深度优先搜索"""
        self.tree.reset()
        self.text_view.clear()
        th = threading.Thread(target=self.dfs_act, daemon=True)
        th.start()

    def dfs_act(self):
        stack = [0]
        self.text_view.append('根结点%s入栈' % chr(65))
        while stack:
            self.text_view.append('栈不为空，执行出栈操作')
            node = stack.pop(0)
            if node > 0:
                self.tree.set_line_color(node, self.tree.tree_list[node][0], self.tree.finished_line_pen)
                time.sleep(self.speed)
            self.tree.set_node_color(node, self.tree.finished_color)
            self.text_view.append('搜索到结点%s' % chr(node + 65))
            time.sleep(self.speed)

            for i in self.tree.tree_list[node][:0:-1]:
                stack.insert(0, i)
                self.text_view.append('结点%s的子结点%s入栈' % (chr(node + 65), chr(i + 65)))

    def click_btn5(self):
        # 广度优先搜索
        self.tree.reset()
        self.text_view.clear()
        th = threading.Thread(target=self.bfs_act, daemon=True)
        th.start()

    def bfs_act(self):
        queue = [0]
        self.text_view.append('根结点%s入队' % chr(65))
        while queue:
            self.text_view.append('队不为空，执行出队操作')
            node = queue.pop(0)
            if node > 0:
                self.tree.set_line_color(node, self.tree.tree_list[node][0], self.tree.animation_line_pen)
                time.sleep(self.speed)
            self.tree.set_node_color(node, self.tree.animation_color)
            self.text_view.append('搜索到结点%s' % chr(node + 65))
            time.sleep(self.speed)

            for i in self.tree.tree_list[node][1:]:
                queue.append(i)
                self.text_view.append('结点%s的子结点%s入队' % (chr(node + 65), chr(i + 65)))

    def click_btn6(self):
        # 转换二叉树
        queue = [0]
        dt_dic = {0: 0}
        while queue:
            node = queue.pop(0)
            kk = 0
            for i in dt_dic:
                if dt_dic[i] == node:
                    kk = i * 2 + 1
            if len(self.tree.tree_list[node]) > 1:
                dt_dic[kk] = self.tree.tree_list[node][1]
                queue.append(dt_dic[kk])
                for i in self.tree.tree_list[node][2:]:
                    kk = kk * 2 + 2
                    dt_dic[kk] = i
                    queue.append(i)
        dialog_win = DBTree(dt_dic, self)
        dialog_win.exec_()

    def click_btn7(self):
        # 设置速度
        num, ok = QInputDialog.getDouble(self, '设置演示速度', '单位：秒')
        if ok and num:
            self.speed = num


class MyTree(QWidget):
    def __init__(self, parent=None):
        """
        用邻接表表示树
        结点用【A-Z】表示
        初始化结点将保留根节点
        邻接表中第【0】位表示父节点的位置
        [0-25] -> [A-Z] : chr(%d + 65)
        [A-Z] -> [0-25] : ord('%s') - 65
        树的结点使用按钮
        树的线用painter
        """
        super(MyTree, self).__init__(parent)
        self.resize(800, 800)
        self.tree_nodes = 0  # 树结点的数量
        self.tree_deep = 0  # 树的高度
        self.max_nodes = 26  # 最大结点数
        # noinspection PyTypeChecker
        self.unused_node: list[int] = None  # 未使用的结点
        self.tree_list: list[list[int]] = [[] for _ in range(self.max_nodes)]  # 树的邻接表
        # 可视化部分
        # noinspection PyTypeChecker
        self.node_list: list[[QPushButton, float]] = [None] * 26  # 点列表
        self.edge_list = [[None] * 26 for _ in range(26)]  # 边列表
        # 绘图数据
        self._r = 20
        self._space = 60
        self.no_action = True  # 没有动画的标记

        self.def_color = QColor(59, 143, 195)
        self.def_node_color = 'rgb(59, 143, 195)'
        self.def_line_pen = QPen(self.def_color, 2, Qt.SolidLine)
        self.animation_color = 'rgb(153, 50, 204)'
        self.finished_color = 'rgb(255, 165, 0)'
        self.animation_line_pen = QPen(QColor(153, 50, 204), 2, Qt.SolidLine)
        self.finished_line_pen = QPen(QColor(255, 165, 0), 2, Qt.SolidLine)

        self.init_data()

    def init_data(self):
        self.tree_nodes = 1
        self.tree_deep = 1
        self.unused_node = [i for i in range(1, 26)]
        self.tree_list = [[] for _ in range(self.max_nodes)]
        self.edge_list = [[None] * 26 for _ in range(26)]
        self.tree_list[0].append(0)
        self.update()

        for i in self.node_list:
            if i is not None:
                btn = i[0]
                btn.close()
                btn.deleteLater()

        self.node_list = [None] * 26
        root = self._build_node(0)
        root.move(int(self.width() / 2) - self._r, int(self._space))
        root.show()
        # noinspection PyTypeChecker
        self.node_list[0] = [root, self.width() / 2]

    def reset(self):
        for i in range(26):
            if self.node_list[i] is not None:
                self.set_node_color(i, self.def_node_color)
        for i in range(26):
            for j in range(i, 26):
                if self.edge_list[i][j] is not None:
                    self.edge_list[i][j] = self.def_line_pen
        self.update()

    def paintEvent(self, a0) -> None:
        # 获取窗口
        main_rect = QRectF(3, 3, self.width() - 6, self.height() - 6)

        # 创建画笔
        paint = QPainter()
        paint.begin(self)

        # 填充背景
        paint.fillRect(main_rect, Qt.white)
        paint.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
        paint.drawRect(main_rect)
        # 画边
        paint.setRenderHint(QPainter.Antialiasing)
        for i in range(26):
            for j in range(i + 1, 26):
                if self.edge_list[i][j] is not None:
                    paint.setPen(self.edge_list[i][j])
                    paint.drawLine(self.node_list[i][0].geometry().center(), self.node_list[j][0].geometry().center())

        # 消除画笔
        paint.end()

    def resizeEvent(self, a0) -> None:
        if not self.no_action:
            return
        root_btn = self.node_list[0][0]
        root_btn.move(int(self.width() / 2) - self._r, self._space)
        self.node_list[0][1] = self.width() / 2
        my_queue = [0]
        while my_queue:
            parent = my_queue.pop(0)
            radius = self.node_list[parent][1]
            child_nums = len(self.tree_list[parent]) - 1
            center = self.node_list[parent][0].geometry().center().x()
            for i in range(1, len(self.tree_list[parent])):
                node_num = self.tree_list[parent][i]
                my_queue.append(node_num)
                self.node_list[node_num][1] = radius / child_nums
                btn = self.node_list[node_num][0]
                btn.move(int(center - radius + (2 * i - 1) * (radius / child_nums) - self._r + 1), btn.y())

    def _build_node(self, char):
        btn = QPushButton(chr(char + 65), self)  # 创建可视化对象
        btn.resize(40, 40)
        btn.setEnabled(False)
        btn.setStyleSheet(
            """
                QPushButton {
                    border-radius: 20px;
                    background-color: rgb(59, 143, 195);
                    color: white;
                    font: 24px;
                }
            """)
        return btn

    def add_node(self, parent):
        if self.tree_nodes > 25:
            return False
        elif self.tree_deep > 8:
            return False
        self.tree_nodes += 1  # 结点数+1
        node_num: int = self.unused_node.pop(0)  # 取节点名
        self.tree_list[parent].append(node_num)  # 加入邻接表
        self.tree_list[node_num].append(parent)
        # 深度 +1
        deep = 2
        i = node_num
        while self.tree_list[i][0] != 0:
            i = self.tree_list[i][0]
            deep += 1
        if self.tree_deep < deep:
            self.tree_deep += 1

        btn = self._build_node(node_num)
        # 位置
        center = self.node_list[parent][0].geometry().center().x()
        # noinspection PyTypeChecker
        radius: int = self.node_list[parent][1]
        child_nums = len(self.tree_list[parent]) - 1
        i = node_num
        deep = 2
        while self.tree_list[i][0] != 0:
            i = self.tree_list[i][0]
            deep += 1
        # noinspection PyTypeChecker
        self.node_list[node_num] = [btn, radius / child_nums]  # btn信息加入到node_list
        left = center - radius
        right = center + radius
        node_center_x = right - radius / child_nums
        node_center_y = (self._r * 2 + self._space) * deep - self._r
        btn.move(int(node_center_x - self._r + 1), int(node_center_y - self._r))
        btn.show()

        # 添加边
        # noinspection PyTypeChecker
        self.edge_list[parent][node_num] = self.def_line_pen
        self.edge_list[node_num][parent] = self.def_line_pen

        # 修改父节点的所有子结点位置
        for i in range(1, len(self.tree_list[parent]) - 1):
            node_num = self.tree_list[parent][i]
            # noinspection PyTypeChecker
            self.node_list[node_num][1] = radius / child_nums
            btn = self.node_list[node_num][0]
            btn.move(int(left + (2 * i - 1) * (radius / child_nums) - self._r + 1), int(node_center_y - self._r))

        self.resizeEvent(None)

    def del_node(self, node_num):
        if len(self.tree_list[node_num]) > 1:
            return False
        elif node_num == 0:
            return False
        else:
            btn = self.node_list[node_num][0]
            btn.close()
            btn.deleteLater()

            # 将删除的结点加入未使用结点的列表并排序
            self.unused_node.append(node_num)
            self.unused_node.sort()
            # 获取父节点
            parent = self.tree_list[node_num][0]
            # 去掉邻接矩阵的边
            self.edge_list[parent][node_num] = None
            self.edge_list[node_num][parent] = None
            # 结点数减一
            self.tree_nodes -= 1
            # 判断深度是否-1, 获取父节点的兄弟结点判断是否全为叶子结点
            deep = 2
            i = node_num
            while self.tree_list[i][0] != 0:
                i = self.tree_list[i][0]
                deep += 1
            # 当前结点清空
            self.node_list[node_num] = None
            self.tree_list[node_num].clear()
            self.tree_list[parent].pop(self.tree_list[parent].index(node_num))
            # 深搜最大高度
            if deep == self.tree_deep:
                my_stack = [(0, 1)]
                while my_stack:
                    i = my_stack.pop()
                    if i[1] == self.tree_deep:
                        break
                    for j in self.tree_list[i[0]][1:]:
                        my_stack.append((j, i[1] + 1))
                else:
                    self.tree_deep -= 1
            # 修改兄弟节点的位置
            center = self.node_list[parent][0].geometry().center().x()
            radius = self.node_list[parent][1]
            child_nums = len(self.tree_list[parent]) - 1

            for i in range(1, len(self.tree_list[parent])):
                node_num = self.tree_list[parent][i]
                self.node_list[node_num][1] = radius / child_nums
                btn = self.node_list[node_num][0]
                btn.move(int(center - radius + (2 * i - 1) * (radius / child_nums) - self._r + 1), btn.y())

            self.resizeEvent(None)

    def set_node_color(self, node_num, color_rgb):
        self.node_list[node_num][0].setStyleSheet(
            """
                QPushButton {
                    border-radius: 20px;
                    background-color: %s;
                    color: white;
                    font: 24px;
                }
            """ % color_rgb)

    def set_line_color(self, i0, j0, len_pen):
        self.edge_list[i0][j0] = len_pen
        self.edge_list[j0][i0] = len_pen
        self.update()


class DBTree(QDialog):
    def __init__(self, tree_dic, parent=None):
        super(DBTree, self).__init__(parent)
        self.resize(1200, 800)

        self.tree_dic = tree_dic
        self.edge_dic = {}
        # noinspection PyTypeChecker
        self.node_list: list[QPushButton] = [None] * 26

        self._r = 20
        self._space = 60

        self.def_node_color = 'rgb(59, 143, 195)'
        self.animation_color = 'rgb(153, 50, 204)'
        self.finished_color = 'rgb(255, 165, 0)'
        self.def_line_pen = QPen(QColor(59, 143, 195), 2, Qt.SolidLine)
        self.animation_line_pen = QPen(QColor(153, 50, 204), 2, Qt.SolidLine)
        self.finished_line_pen = QPen(QColor(255, 165, 0), 2, Qt.SolidLine)

        for i in self.tree_dic:
            self.add_node(i, self.tree_dic[i])

    def _build_node(self, char):
        btn = QPushButton(chr(char + 65), self)  # 创建可视化对象
        btn.resize(40, 40)
        btn.setEnabled(False)
        btn.setStyleSheet(
            """
                QPushButton {
                    border-radius: 20px;
                    background-color: rgb(59, 143, 195);
                    color: white;
                    font: 24px;
                }
            """)
        return btn

    def add_node(self, index, name=None):
        """
        parent->id
        child->1 or 2
        name: None or [0~26]
        """
        # 计算第几层的第几个
        deep = math.floor(math.log2(index + 1))
        ii = index + 2 - pow(2, deep)
        # 计算位置
        if deep == 0:
            x = self.width() // 3 * 2 - self._r
            y = self._space - self._r
        else:
            y = self._space + deep * (self._space + 2 * self._r) - self._r
            x = self.width() // (pow(2, deep - 1) + 1) * ii - self._r
        # 获取图形结点
        node = self._build_node(name)
        # 移动到指定位置
        node.move(x, y)
        node.show()

        # 判断父结点, 添加边
        if index != 0:
            self.edge_dic[index] = self.def_line_pen
            self.update()

        # 加入按钮列表
        self.node_list[name] = node

    def paintEvent(self, a0) -> None:
        # 获取窗口
        main_rect = QRectF(3, 3, self.width() - 6, self.height() - 6)

        # 创建画笔
        paint = QPainter()
        paint.begin(self)

        # 填充背景
        paint.fillRect(main_rect, Qt.white)
        paint.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
        paint.drawRect(main_rect)
        # 画边
        paint.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        for i in self.edge_dic:
            paint.setPen(self.edge_dic[i])
            paint.drawLine(
                self.node_list[self.tree_dic[(i - 1) // 2]].geometry().center(),
                self.node_list[self.tree_dic[i]].geometry().center()
            )

        # 消除画笔
        paint.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TreeWidget()
    win.show()

    sys.exit(app.exec_())
