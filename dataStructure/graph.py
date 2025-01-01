"""
@File     : graph.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/4/26 15:56
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/4/26 15:56        1.0             None
"""

from PyQt5.QtGui import QMouseEvent, QPainter, QPen, QCursor, QColor
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPoint, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QInputDialog, \
    QDialog, QLabel

import sys
import threading
import time


class PushButton(QPushButton):
    long_pressed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QTimer()
        self.timer.timeout.connect(self._long_pressed)
        self.move_s = False

    def mousePressEvent(self, evt: QMouseEvent):
        super().mousePressEvent(evt)
        self.timer.start(200)
        self.move_s = True
        self.setCursor(Qt.PointingHandCursor)

    def mouseReleaseEvent(self, evt: QMouseEvent):
        # 长按后此方法仍会触发 clicked 事件，需要禁止信号发射。
        if self.timer.remainingTime() <= 0:
            self.blockSignals(True)
        self.timer.stop()
        self.move_s = False
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(evt)
        self.blockSignals(False)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self.move_s:
            self.move(self.pos().x() + e.pos().x() - 20, self.pos().y() + e.pos().y() - 20)
            self.parent().update()

    def _long_pressed(self):
        self.timer.stop()
        # noinspection PyUnresolvedReferences
        self.long_pressed.emit()


class GraphWindow(QWidget):
    add_node_finished = pyqtSignal()

    def __init__(self, parent=None):
        super(GraphWindow, self).__init__(parent)
        # 未使用结点列表
        self.unused_node: list[int] = [i for i in range(0, 26)]
        # 邻接表
        self.node_table = [[] for _ in range(26)]
        # 邻接矩阵
        self.node_matrix = [[None] * 26 for _ in range(26)]
        # 结点列表
        self.node_list = [None] * 26

        # 事件处理变量
        self.add_btn = False  # 加点
        self._build_edge = False  # 加边
        self._last_point = None
        self._new_point = None

        # 颜色对象
        self.def_node_color = 'rgb(59, 143, 195)'
        self.finished_color = 'rgb(255, 165, 0)'
        self.def_line_pen = QPen(QColor(0, 0, 0), 2, Qt.SolidLine)
        self.finished_line_pen = QPen(QColor(153, 50, 204), 3, Qt.SolidLine)

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
        paint.setPen(self.def_line_pen)
        if self._build_edge:
            paint.drawLine(self._last_point[0], self._new_point)
        for i in range(26):
            for j in range(i + 1, 26):
                if self.node_matrix[i][j] is not None:
                    paint.setPen(self.node_matrix[i][j])
                    # noinspection PyUnresolvedReferences
                    paint.drawLine(
                        self.node_list[i].geometry().center(),
                        self.node_list[j].geometry().center()
                    )

        # 消除画笔
        paint.end()

    def mousePressEvent(self, a0: QMouseEvent):
        if self.add_btn and a0.buttons() == Qt.LeftButton:
            self.add_btn = False
            self.add_node(a0.pos())
        elif self._build_edge and a0.buttons() == Qt.RightButton:
            self._build_edge = False
            self.update()

    def mouseMoveEvent(self, a0: QMouseEvent):
        self._new_point = a0.pos()
        self.update()

    def add_node(self, point: QPoint):
        if self.unused_node:
            name = self.unused_node.pop(0)
            node = self._build_node(name)
            node.move(point.x() - 20, point.y() - 20)
            node.show()
            node.clicked.connect(self.add_edge)
            # noinspection PyTypeChecker
            self.node_list[name] = node
            # noinspection PyUnresolvedReferences
            self.add_node_finished.emit()
        else:
            QMessageBox.warning(self, '警告', '超出结点数量限制', QMessageBox.Ok)

    def _build_node(self, char):
        btn = PushButton(chr(char + 65), self)  # 创建可视化对象
        btn.resize(40, 40)
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

    def add_edge(self):
        node = self.sender()
        if self._build_edge:
            self._build_edge = False
            self.setMouseTracking(False)
            # 有边删除边
            if self.node_matrix[self._last_point[1]][ord(node.text()) - 65] is not None:
                # 删除邻接矩阵
                self.node_matrix[self._last_point[1]][ord(node.text()) - 65] = None
                self.node_matrix[ord(node.text()) - 65][self._last_point[1]] = None
                # 删除邻接表
                self.node_table[self._last_point[1]].pop(
                    self.node_table[self._last_point[1]].index(ord(node.text()) - 65)
                )
                self.node_table[ord(node.text()) - 65].pop(
                    self.node_table[ord(node.text()) - 65].index(self._last_point[1])
                )
                self.update()
            # 无边添加边
            else:
                # 不存在环
                if ord(node.text()) - 65 == self._last_point[1]:
                    return
                # 将边添加到结构中
                # 邻接矩阵
                # noinspection PyTypeChecker
                self.node_matrix[self._last_point[1]][ord(node.text()) - 65] = self.def_line_pen
                # noinspection PyTypeChecker
                self.node_matrix[ord(node.text()) - 65][self._last_point[1]] = self.def_line_pen
                # 邻接表
                self.node_table[self._last_point[1]].append(ord(node.text()) - 65)
                self.node_table[ord(node.text()) - 65].append(self._last_point[1])
                self.update()
        else:
            self._build_edge = True
            self.setMouseTracking(True)
            self._last_point = (node.pos() + QPoint(20, 20), ord(node.text()) - 65)

    def del_node(self, iid):
        if self.node_list[iid] is None:
            QMessageBox.critical(self, '错误', '没有该结点', QMessageBox.Ok)
            return
        else:
            self.node_table[iid].clear()
            for j in range(26):
                if self.node_matrix[j][iid] is not None:
                    self.node_matrix[j][iid] = None
                    self.node_matrix[iid][j] = None
                    self.node_table[j].pop(self.node_table[j].index(iid))
            node = self.node_list[iid]
            node.close()
            node.deleteLater()
            self.node_list[iid] = None
            self.unused_node.append(iid)
            self.unused_node.sort()
            self.update()

    def set_node_color(self, iid, color_rgb: str):
        self.node_list[iid].setStyleSheet(
            """
                QPushButton {
                    border-radius: 20px;
                    background-color: %s;
                    color: white;
                    font: 24px;
                }
            """ % color_rgb)

    def set_edge_color(self, node_id1, node_id2, color_pen: QPen):
        self.node_matrix[node_id1][node_id2] = color_pen
        self.node_matrix[node_id2][node_id1] = color_pen
        self.update()

    def reset_color(self):
        for i in self.node_list:
            if i is not None:
                # noinspection PyUnresolvedReferences
                i.setStyleSheet(
                    """
                        QPushButton {
                            border-radius: 20px;
                            background-color: rgb(59, 143, 195);
                            color: white;
                            font: 24px;
                        }
                    """)
        for i in range(26):
            for j in range(i + 1, 26):
                if self.node_matrix[i][j] is not None:
                    # noinspection PyTypeChecker
                    self.node_matrix[i][j] = self.def_line_pen
                    # noinspection PyTypeChecker
                    self.node_matrix[j][i] = self.def_line_pen
        self.update()


class MW(QWidget):
    def __init__(self):
        super(MW, self).__init__(None)
        self.resize(800, 800)

        # 数据
        self.speed = 0.6

        # 主布局 （上控制，下图形)
        self.control = QHBoxLayout()  # 控制按钮布局
        self.window = GraphWindow()  # 图形区域
        # noinspection PyUnresolvedReferences
        self.window.add_node_finished.connect(self.new_node_finished)
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.control)
        self.main_layout.addWidget(self.window)
        self.setLayout(self.main_layout)
        # region 控制按钮区域
        self.btn_new_node = QPushButton('添加结点')
        self.btn_del_node = QPushButton('删除结点')
        self.btn_reset = QPushButton('初始化')
        self.btn_set_speed = QPushButton('设置速度')
        self.btn_dfs_anim = QPushButton('深度优先遍历')
        self.btn_bfs_anim = QPushButton('广度优先遍历')
        self.show_table_and_matrix = QPushButton('显示邻接表和邻接矩阵')
        # ========================================= #
        self.btn_new_node.clicked.connect(self.clk_btn_new_node)
        self.btn_del_node.clicked.connect(self.clk_btn_del_node)
        self.btn_reset.clicked.connect(self.clk_btn_reset)
        self.btn_set_speed.clicked.connect(self.clk_btn_set_speed)
        self.btn_dfs_anim.clicked.connect(self.clk_btn_dfs_anim)
        self.btn_bfs_anim.clicked.connect(self.clk_btn_bfs_anim)
        self.show_table_and_matrix.clicked.connect(self.clk_show_table_and_matrix)
        # ========================================= #
        self.control.addWidget(self.btn_new_node)
        self.control.addStretch(1)
        self.control.addWidget(self.btn_del_node)
        self.control.addStretch(1)
        self.control.addWidget(self.btn_reset)
        self.control.addStretch(1)
        self.control.addWidget(self.btn_set_speed)
        self.control.addStretch(1)
        self.control.addWidget(self.btn_dfs_anim)
        self.control.addStretch(1)
        self.control.addWidget(self.btn_bfs_anim)
        self.control.addStretch(1)
        self.control.addWidget(self.show_table_and_matrix)
        # endregion

    # 创建结点
    def clk_btn_new_node(self):
        self.btn_new_node.setEnabled(False)
        self.window.add_btn = True
        self.window.setCursor(Qt.PointingHandCursor)

    def new_node_finished(self):
        self.btn_new_node.setEnabled(True)
        self.window.setCursor(Qt.ArrowCursor)

    # 删除节点
    def clk_btn_del_node(self):
        arr = []
        for i in range(26):
            if self.window.node_list[i] is not None:
                arr.append(chr(i + 65))
        if arr:
            ch, ok = QInputDialog.getItem(self, '删除结点', '选择要删除的结点', arr, len(arr) - 1, False)
            if ok:
                nod = ord(ch) - 65
                self.window.del_node(nod)
        else:
            QMessageBox.critical(self, '错误', '无结点！', QMessageBox.Ok)

    # 初始化 重置色彩
    def clk_btn_reset(self):
        self.window.reset_color()

    # 设置速度
    def clk_btn_set_speed(self):
        num, ok = QInputDialog.getDouble(self, '设置演示速度', '单位：秒')
        if ok and num:
            self.speed = num

    # 判断图是否连通
    def is_connected_graph(self):
        # 判断是否有结点
        if len(self.window.unused_node) >= 26:
            QMessageBox.critical(self, '错误', '无结点！', QMessageBox.Ok)
            return False
        # 判断是否连通
        node_arr = {}
        node_nums = 0
        now_node = 0
        for i in range(26):
            if self.window.node_list[i] is not None:
                now_node = i
                break
        stack = []

        for i in range(26):
            if self.window.node_list[i] is not None:
                node_arr[i] = True
                node_nums += 1

        while node_nums > 0:
            if node_arr[now_node]:
                node_nums -= 1
                node_arr[now_node] = False

            for i in self.window.node_table[now_node]:
                if node_arr[i]:
                    stack.append(now_node)
                    now_node = i
                    break
            else:
                if stack:
                    now_node = stack.pop()
                else:
                    return False
        return True

    # 获取搜索开始结点
    def how_start(self):
        arr = []
        for i in range(26):
            if self.window.node_list[i] is not None:
                arr.append(chr(i + 65))
        if arr:
            ch, ok = QInputDialog.getItem(self, '搜索', '选择开始结点', arr, 0, False)
            if ok:
                return ord(ch) - 65

    # 深度优先遍历
    def clk_btn_dfs_anim(self):
        if self.is_connected_graph():
            self.window.reset_color()
            start_id = self.how_start()
            if start_id is None:
                pass
            else:
                th = threading.Thread(target=self.dfs, args=(start_id,), daemon=True)
                th.start()
        else:
            QMessageBox.critical(self, '错误', '非连通图！', QMessageBox.Ok)

    def dfs(self, start_id):
        # 访问过 标记为假
        node_arr = {}
        node_nums = 0
        now_node = start_id
        stack = []

        for i in range(26):
            if self.window.node_list[i] is not None:
                node_arr[i] = True
                node_nums += 1

        while node_nums > 0:
            if node_arr[now_node]:
                node_nums -= 1
                self.window.set_node_color(now_node, self.window.finished_color)
                node_arr[now_node] = False
                time.sleep(self.speed)

            for i in self.window.node_table[now_node]:
                if node_arr[i]:
                    self.window.set_edge_color(now_node, i, self.window.finished_line_pen)
                    time.sleep(self.speed)

                    stack.append(now_node)
                    now_node = i
                    break
            else:
                now_node = stack.pop()

    # 广度优先遍历
    def clk_btn_bfs_anim(self):
        if self.is_connected_graph():
            self.window.reset_color()
            start_id = self.how_start()
            if start_id is None:
                pass
            else:
                th = threading.Thread(target=self.bfs, args=(start_id,), daemon=True)
                th.start()
        else:
            QMessageBox.critical(self, '错误', '非连通图！', QMessageBox.Ok)

    def bfs(self, start_id):
        node_arr = {}
        node_nums = 0
        queue = []

        for i in range(26):
            if self.window.node_list[i] is not None:
                node_arr[i] = True
                node_nums += 1

        self.window.set_node_color(start_id, self.window.finished_color)
        time.sleep(self.speed)
        node_arr[start_id] = False
        for i in self.window.node_table[start_id]:
            queue.append((i, start_id))
        while queue:
            node = queue.pop(0)
            self.window.set_edge_color(node[1], node[0], self.window.finished_line_pen)
            time.sleep(self.speed)
            self.window.set_node_color(node[0], self.window.finished_color)
            time.sleep(self.speed)
            node_arr[node[0]] = False
            for i in self.window.node_table[node[0]]:
                if node_arr[i]:
                    for j in queue:
                        if j[0] == i:
                            break
                    else:
                        queue.append((i, node[0]))

    # 显示邻接表和邻接矩阵
    def clk_show_table_and_matrix(self):
        dia = QDialog(self)
        dia.setWindowTitle('邻接表和邻接矩阵')
        dia.setLayout(QHBoxLayout())
        table_layout = QVBoxLayout()
        matrix_layout = QVBoxLayout()
        dia.layout().addLayout(table_layout)
        dia.layout().addLayout(matrix_layout)

        # 处理邻接表
        kk = []
        for i in range(26):
            if self.window.node_table[i]:
                ss = [chr(x + 65) for x in self.window.node_table[i]]
                text = chr(i + 65) + ' {' + ', '.join(ss) + '};'
                xx = QLabel(text)
                table_layout.addWidget(xx, 1, Qt.AlignLeft | Qt.AlignCenter)
                kk.append(i)
        # 处理邻接矩阵
        text = ' 　│　' + '　'.join([chr(x + 65) for x in kk])
        matrix_layout.addWidget(QLabel(text), 1, Qt.AlignLeft | Qt.AlignCenter)
        text = ' ─┼─' + '─'.join(['─'] * len(kk))
        matrix_layout.addWidget(QLabel(text), 1, Qt.AlignLeft | Qt.AlignCenter)
        for i in kk:
            text = '%s　│　' % chr(i + 65)
            for j in kk:
                if self.window.node_matrix[i][j] is None:
                    text += '0　'
                else:
                    text += '1　'
            matrix_layout.addWidget(QLabel(text), 1, Qt.AlignLeft | Qt.AlignCenter)
        dia.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MW()
    win.show()
    sys.exit(app.exec_())
