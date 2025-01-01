"""
@File     : double_tree.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/4/10 12:34
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/25 12:34        1.0             None
"""
import math
import sys
import threading
import time

from PyQt5.QtCore import Qt, QRectF, pyqtSignal
from PyQt5.QtGui import QColor, QPen, QPainter, QTextCursor
from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QApplication, QTextBrowser, QGridLayout, QLabel, \
    QVBoxLayout, QHBoxLayout, QDialog, QComboBox, QCheckBox, QInputDialog


class AddNodeDialog(QDialog):
    sig = pyqtSignal(list)

    def __init__(self, e_dic, parent=None):
        super(AddNodeDialog, self).__init__(parent)

        self.dic = e_dic

        # 父结点
        lable1 = QLabel('添加结点')
        lable2 = QLabel('的')
        self.combo = QComboBox()
        for i in e_dic:
            self.combo.addItem(chr(i + 65))
        self.combo.currentIndexChanged.connect(self.__init__data)
        layout1 = QHBoxLayout()
        layout1.addWidget(lable1)
        layout1.addWidget(self.combo)
        layout1.addWidget(lable2)

        # 创建左、右孩子多选按钮
        self.left_child_btn = QCheckBox('左孩子')
        self.right_child_btn = QCheckBox('右孩子')
        self.left_child_btn.setChecked(True)
        self.right_child_btn.setChecked(True)
        self.left_child_btn.setEnabled(False)
        self.right_child_btn.setEnabled(False)

        # 创建功能按钮
        btn1 = QPushButton('确定')
        btn2 = QPushButton('取消')
        btn1.clicked.connect(self.click_btn_1)
        btn2.clicked.connect(self.click_btn_2)
        layout2 = QHBoxLayout()
        layout2.addWidget(btn1, 1, Qt.AlignRight | Qt.AlignBottom)
        layout2.addWidget(btn2, 1, Qt.AlignRight | Qt.AlignBottom)
        layout2.setSpacing(10)

        # 创建主布局
        layout = QVBoxLayout(self)
        layout.addLayout(layout1)
        layout.addWidget(self.left_child_btn)
        layout.addWidget(self.right_child_btn)
        layout.addLayout(layout2)

        # 初始化
        self.__init__data()

    def __init__data(self):
        ss = ord(self.combo.currentText()) - 65
        self.set_check_btn_enable(ss)

    def set_check_btn_enable(self, idd):
        if self.dic[idd] == 3:
            self.left_child_btn.setEnabled(True)
            self.right_child_btn.setEnabled(True)
        elif self.dic[idd] == 2:
            self.left_child_btn.setEnabled(False)
            self.right_child_btn.setEnabled(True)
        elif self.dic[idd] == 1:
            self.left_child_btn.setEnabled(True)
            self.right_child_btn.setEnabled(False)

    def click_btn_1(self):
        add_list = [ord(self.combo.currentText()) - 65]
        if self.left_child_btn.isChecked():
            add_list.append(0)
        if self.right_child_btn.isChecked():
            add_list.append(1)
        # noinspection PyUnresolvedReferences
        self.sig.emit(add_list)
        self.close()

    def click_btn_2(self):
        self.close()


class DbTWidget(QWidget):
    def __init__(self, parent=None):
        super(DbTWidget, self).__init__(parent)

        # 树数据
        self.tree = DoubleTree()
        # 屏幕控制数据
        self.text_view = QTextBrowser()
        self.speed = 0.8

        self.__init_ui()

    def __init_ui(self):
        right_layout = QVBoxLayout()
        right_layout.addLayout(self.__button_layout())
        right_layout.addWidget(self.text_view)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tree, 5)
        main_layout.addLayout(right_layout, 1)
        self.setLayout(main_layout)

    def __button_layout(self):
        button1 = QPushButton('添加结点')
        button2 = QPushButton('删除结点')
        button3 = QPushButton('初始化')
        button4 = QPushButton('先序遍历')
        button5 = QPushButton('中序遍历')
        button6 = QPushButton('后序遍历')
        button7 = QPushButton('设置速度')
        button8 = QPushButton('用数组表示')

        button1.clicked.connect(self.click_btn1)
        button2.clicked.connect(self.click_btn2)
        button3.clicked.connect(self.click_btn3)
        button4.clicked.connect(self.click_btn4)
        button5.clicked.connect(self.click_btn5)
        button6.clicked.connect(self.click_btn6)
        button7.clicked.connect(self.click_btn7)
        button8.clicked.connect(self.click_btn8)
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
        layout.addWidget(button7, 4, 0)
        layout.addWidget(button8, 4, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)

        return layout

    def click_btn1(self):
        dic = {}
        for i in self.tree.tree_dic:
            aa = 2 * i in self.tree.tree_dic
            bb = 2 * i + 1 in self.tree.tree_dic
            if not aa and not bb:
                dic[self.tree.tree_dic[i]] = 3
            elif aa and not bb:
                dic[self.tree.tree_dic[i]] = 2
            elif not aa and bb:
                dic[self.tree.tree_dic[i]] = 1
        # 创建对象
        dia = AddNodeDialog(dic)
        # noinspection PyUnresolvedReferences
        dia.sig.connect(self.add_node)
        dia.exec()

    def add_node(self, lis):
        parent_name = lis.pop(0)
        kk = 0
        for i in self.tree.tree_dic:
            if self.tree.tree_dic[i] == parent_name:
                kk = 2 * i
                break
        for i in lis:
            self.tree.add_node(kk + i)
            self.text_view.append(
                '添加结点%s的子结点%s' % (chr(self.tree.tree_dic[kk // 2] + 65), chr(self.tree.tree_dic[kk + i] + 65)))

    def click_btn2(self):
        lis = []
        for i in self.tree.tree_dic:
            if 2 * i not in self.tree.tree_dic and 2 * i + 1 not in self.tree.tree_dic:
                if i == 1:
                    continue
                lis.append(chr(self.tree.tree_dic[i] + 65))
        if len(lis) > 0:
            ch, ok = QInputDialog.getItem(self, '删除结点', '选择要删除的结点', lis, len(lis) - 1, False)
            if ok:
                self.text_view.append('删除结点:%s' % ch)
                nod = ord(ch) - 65
                for i in self.tree.tree_dic:
                    if self.tree.tree_dic[i] == nod:
                        nod = i
                        break
                self.tree.delete_node(nod)
        else:
            QMessageBox.warning(self, '警告', '无叶子结点！', QMessageBox.Ok)

    def click_btn3(self):
        self.text_view.clear()
        self.tree.init_color()

    def click_btn4(self):
        # 先序遍历
        self.tree.init_color()
        self.text_view.clear()
        self.text_view.append("先序遍历>>>")
        th = threading.Thread(target=self.first_root, daemon=True)
        th.start()

    def first_root(self):
        root = 1
        stack = []
        lis = ''
        while root > 0 or stack:
            if root == 0:
                root = stack.pop() * 2 + 1
            while root in self.tree.tree_dic:
                if root != 1:
                    self.tree.set_edge_color(root, self.tree.finished_line_pen)
                    time.sleep(self.speed)
                node_name = chr(self.tree.tree_dic[root] + 65)
                lis += node_name + ' '
                self.text_view.append('遍历结点%s, 入栈, 遍历左孩子' % node_name)
                self.tree.set_node_color(root, self.tree.finished_color)
                time.sleep(self.speed)
                stack.append(root)
                root *= 2
            self.text_view.append('子结点为空, 出栈, 遍历出栈结点的右孩子')
            self.tree.set_node_color(root // 2, self.tree.animation_color)
            time.sleep(self.speed)
            if root > 3:
                self.tree.set_edge_color(root // 2, self.tree.animation_line_pen)
                time.sleep(self.speed)
                self.tree.set_node_color(root // 4, self.tree.animation_color)
                time.sleep(self.speed)
            root //= 2
            while root % 2 == 1 and root != 1:
                self.tree.set_node_color(root // 2, self.tree.animation_color)
                time.sleep(self.speed)
                if root > 3:
                    self.tree.set_edge_color(root // 2, self.tree.animation_line_pen)
                    time.sleep(self.speed)
                    self.tree.set_node_color(root // 4, self.tree.animation_color)
                    time.sleep(self.speed)
                root //= 2
            root = 0
        self.text_view.append('遍历完成，先序遍历序列为>>>')
        self.text_view.append(lis)
        self.text_view.moveCursor(QTextCursor.End)

    def click_btn5(self):
        # 中序遍历
        self.tree.init_color()
        self.text_view.clear()
        self.text_view.append("中序遍历>>>")
        th = threading.Thread(target=self.middle_root, daemon=True)
        th.start()

    def middle_root(self):
        root = 1
        stack = []
        lis = ''
        while root > 0 or stack:
            if root == 0:
                root = stack.pop()
                node_name = chr(self.tree.tree_dic[root] + 65)
                lis += node_name + ' '
                self.text_view.append('遍历结点%s, 遍历右子结点' % node_name)
                self.tree.set_node_color(root, self.tree.finished_color)
                time.sleep(self.speed)
                if root > 1 and 2 * root + 1 not in self.tree.tree_dic:
                    self.tree.set_edge_color(root, self.tree.finished_line_pen)
                    time.sleep(self.speed)
                root = 2 * root + 1

            while root in self.tree.tree_dic:
                if root != 1:
                    self.tree.set_edge_color(root, self.tree.animation_line_pen)
                    time.sleep(self.speed)
                self.text_view.append('结点%s入栈, 寻找左子结点' % chr(self.tree.tree_dic[root] + 65))
                self.tree.set_node_color(root, self.tree.animation_color)
                time.sleep(self.speed)
                stack.append(root)
                root *= 2
            self.text_view.append('子结点为空, 出栈, 遍历出栈结点')
            if root % 2 == 1:
                root //= 2
                while root // 2 > 1 \
                        and self.tree.edge_dic[root // 2] != self.tree.finished_line_pen \
                        and root // 2 not in stack:
                    self.tree.set_edge_color(root // 2, self.tree.finished_line_pen)
                    time.sleep(self.speed)
                    root //= 2
            root = 0
        self.text_view.append('遍历完成，中序遍历序列为:')
        self.text_view.append(lis)
        self.text_view.moveCursor(QTextCursor.End)

    def click_btn6(self):
        # 后续遍历
        self.tree.init_color()
        self.text_view.clear()
        self.text_view.append("后序遍历>>>")
        th = threading.Thread(target=self.last_root, daemon=True)
        th.start()

    def last_root(self):
        root = 1
        lis = ''
        last_pop = 0
        self.text_view.append('指针指向根节点')
        self.tree.set_node_color(root, self.tree.animation_color)
        time.sleep(self.speed)

        while root > 0:
            while 2 * root in self.tree.tree_dic:
                self.text_view.append('左子结点不为空，指针指向向左子结点')
                root *= 2
                self.tree.set_edge_color(root, self.tree.animation_line_pen)
                time.sleep(self.speed)
                self.tree.set_node_color(root, self.tree.animation_color)
                time.sleep(self.speed)

            while root > 0:
                if 2 * root + 1 in self.tree.tree_dic and 2 * root + 1 != last_pop:
                    self.text_view.append('右子结点不为空，指针指向向右子结点')
                    root = 2 * root + 1
                    self.tree.set_edge_color(root, self.tree.animation_line_pen)
                    time.sleep(self.speed)
                    self.tree.set_node_color(root, self.tree.animation_color)
                    time.sleep(self.speed)
                    break
                else:
                    node_name = chr(self.tree.tree_dic[root] + 65)
                    self.text_view.append('结点%s无子结点或子结点已遍历，遍历该结点' % node_name)
                    self.tree.set_node_color(root, self.tree.finished_color)
                    time.sleep(self.speed)
                    lis += node_name + ' '
                    last_pop = root
                    if root > 1:
                        self.text_view.append('指针指向该结点的父结点')
                        self.tree.set_edge_color(root, self.tree.finished_line_pen)
                        time.sleep(self.speed)
                    root //= 2
        self.text_view.append('遍历完成，后序遍历序列为:')
        self.text_view.append(lis)
        self.text_view.moveCursor(QTextCursor.End)

    def click_btn7(self):
        num, ok = QInputDialog.getDouble(self, '设置演示速度', '单位：秒')
        if ok and num:
            self.speed = num

    def click_btn8(self):
        if self.tree.is_complete_binary_tree():
            lis = [self.tree.node_num]
            for i in range(1, self.tree.node_num + 1):
                lis.append(chr(self.tree.tree_dic[i] + 65))
            QMessageBox.about(self, '使用数组形式记录二叉树', str(lis))
        else:
            QMessageBox.warning(self, '警告...', '非满二叉树', QMessageBox.Ok)


class DoubleTree(QWidget):
    def __init__(self, parent=None):
        super(DoubleTree, self).__init__(parent)
        self.setMinimumSize(800, 600)

        # 二叉树使用字典记录，键是线性表中的index，值是ID
        # index从1开始, 左孩子 2*index, 右孩子2*index+1
        self.node_num = 0
        self.tree_dic = {1: 0}
        # 边字典
        self.edge_dic = {}
        # 结点按钮链表
        # noinspection PyTypeChecker
        self.node_list: list[QPushButton] = [None] * 26
        # 未使用的结点
        self.unused_node: list[int] = [i for i in range(0, 26)]

        # 可视化数据
        self._r = 20
        self._space = 60

        # 颜色对象
        self.def_node_color = 'rgb(59, 143, 195)'
        self.animation_color = 'rgb(153, 50, 204)'
        self.finished_color = 'rgb(255, 165, 0)'
        self.def_line_pen = QPen(QColor(59, 143, 195), 2, Qt.SolidLine)
        self.animation_line_pen = QPen(QColor(153, 50, 204), 2, Qt.SolidLine)
        self.finished_line_pen = QPen(QColor(255, 165, 0), 2, Qt.SolidLine)

        # 初始化
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
        deep = math.floor(math.log2(index))
        ii = index - pow(2, deep) + 1
        # 判断父结点是否存在
        if index != 1 and index // 2 not in self.tree_dic:
            QMessageBox.warning(self, '警告', '位置错误！', QMessageBox.Ok)
            return
        # 深度不得超出6层
        if deep >= 6:
            QMessageBox.warning(self, '警告', '树的高度超出限制！', QMessageBox.Ok)
            return
        # 计算ID
        if self.node_num >= 26:
            QMessageBox.warning(self, '警告', '结点数量超出限制！', QMessageBox.Ok)
            return
        elif name is None:
            name = self.unused_node.pop(0)
        else:
            if name in self.unused_node:
                self.unused_node.pop(self.unused_node.index(name))
            else:
                QMessageBox.warning(self, '警告', '结点重复！', QMessageBox.Ok)
                return
        # 计算位置
        y = self._space + deep * (self._space + 2 * self._r) - self._r
        x = self.width() // (pow(2, deep) + 1) * ii - self._r
        # 获取图形结点
        node = self._build_node(name)
        # 移动到指定位置
        node.move(x, y)
        node.show()

        # 判断父结点, 添加边
        if index // 2 > 0:
            self.edge_dic[index] = self.def_line_pen
            self.update()

        # 加入二叉树字典tree_dic
        self.tree_dic[index] = name
        # 加入按钮列表
        self.node_list[name] = node
        # 结点数+1
        self.node_num += 1

    def delete_node(self, index):
        """
        删除位置index上的坐标
        """
        if index * 2 in self.tree_dic or index * 2 + 1 in self.tree_dic:
            # 弹窗提醒
            QMessageBox.warning(self, '警告', '非叶子结点！', QMessageBox.Ok)
            return
        else:
            # 修改结点列表, 取出按钮并删除
            node = self.node_list[self.tree_dic[index]]
            node.close()
            node.deleteLater()
            # noinspection PyTypeChecker
            self.node_list[self.tree_dic[index]] = None
            # 未使用字符列表
            self.unused_node.append(self.tree_dic[index])
            self.unused_node.sort()
            # 修改树字典
            self.tree_dic.pop(index)
            # 修改边字典
            if index != 1:
                self.edge_dic.pop(index)
            # 修改结点数量
            self.node_num -= 1
            # 刷新
            self.update()

    def set_node_color(self, index: int, color_rgb: str):
        self.node_list[self.tree_dic[index]].setStyleSheet(
            """
                QPushButton {
                    border-radius: 20px;
                    background-color: %s;
                    color: white;
                    font: 24px;
                }
            """ % color_rgb)

    def set_edge_color(self, index: int, color_pen: QPen):
        self.edge_dic[index] = color_pen
        self.update()

    def init_color(self):
        for i in self.node_list:
            if i is not None:
                i.setStyleSheet(
                    """
                        QPushButton {
                            border-radius: 20px;
                            background-color: rgb(59, 143, 195);
                            color: white;
                            font: 24px;
                        }
                    """)
        for i in self.edge_dic:
            self.edge_dic[i] = self.def_line_pen
        self.update()

    def is_complete_binary_tree(self) -> bool:
        """判断是否是完全二叉树"""
        for i in range(1, self.node_num + 1):
            if i not in self.tree_dic:
                break
        else:
            return True
        return False

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
                self.node_list[self.tree_dic[i // 2]].geometry().center(),
                self.node_list[self.tree_dic[i]].geometry().center()
            )

        # 消除画笔
        paint.end()

    def resizeEvent(self, a0) -> None:
        for i in self.tree_dic:
            # 计算第几层的第几个
            deep = math.floor(math.log2(i))
            ii = i - pow(2, deep) + 1
            # 计算位置
            y = self._space + deep * (self._space + 2 * self._r) - self._r
            x = self.width() // (pow(2, deep) + 1) * ii - self._r
            # 移动到指定位置
            self.node_list[self.tree_dic[i]].move(x, y)
        # 刷新
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DbTWidget()
    win.show()

    sys.exit(app.exec_())
