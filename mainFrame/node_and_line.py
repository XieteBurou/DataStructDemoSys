"""
@File     : node_and_line.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/3/14 12:29
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/14 12:29        1.0             None
"""
import sys
import time
import typing
import threading

from PyQt5.QtCore import QLineF, QPointF, Qt, QRectF, QPropertyAnimation, QObject
from PyQt5.QtGui import QColor, QPen, QBrush, QPainter, QFont
from PyQt5.QtWidgets import QGraphicsObject, QWidget, QStyleOptionGraphicsItem, QApplication, QGraphicsScene, \
    QGraphicsView, QGraphicsItem, QGraphicsLineItem


class Default:
    # # 默认值::结点
    # 画笔
    def_node_color: QColor = QColor(238, 238, 238)  # 文字颜色, 边框颜色
    def_pen_widget: int = 2  # 文字宽度
    def_pen: QPen = QPen(def_node_color, def_pen_widget, Qt.SolidLine)  # QPen对象
    def_brush: QBrush = QBrush(QColor(59, 143, 195))  # 默认填充色
    # 文字
    def_font_size = 16  # 文字尺寸
    def_font = QFont('', def_font_size, def_pen_widget)  # 字体对象
    # # 默认值::边
    def_line_pen = QPen(Qt.black, def_pen_widget, Qt.SolidLine)

    # 活动
    act_color: QColor = QColor(255, 138, 39)  # 活动颜色

    act_pen: QPen = QPen(act_color, def_pen_widget, Qt.SolidLine)  # 活动画笔
    act_line_pen: QPen = QPen(act_color, def_pen_widget, Qt.SolidLine)
    act_brush: QBrush(act_color)

    # 已活动的
    acted_color: QColor = QColor(255, 138, 39)
    acted_line_pen: QPen = QPen(act_color, def_pen_widget, Qt.SolidLine)
    acted_pen: QPen = QPen(act_color, def_pen_widget, Qt.SolidLine)

    # 红色标记

    # 绿色标记


""" 注:
    圆心： Node.dot
    获取 Item 在 Scene 中的位置， 需要加上 Node.boundingRect().center()
"""
# 结点图形


class Node(QGraphicsObject):
    def __init__(self, dot: QPointF, node_text: str, radius: float = 20.0, parent=None):
        super(Node, self).__init__(parent)
        self.dot = dot  # 圆心
        self.radius = radius  # 半径
        self.char = node_text  # 结点名
        self.rect = QRectF(dot.x() - radius, dot.y() - radius, radius * 2, radius * 2)

    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget: typing.Optional[QWidget] = ...):
        painter.setPen(Default.def_pen)
        painter.setBrush(Default.def_brush)
        painter.setFont(Default.def_font)
        painter.drawEllipse(self.rect)
        painter.drawText(self.rect, Qt.AlignCenter, self.char)

    def boundingRect(self) -> QRectF:
        return self.rect

    def set_dot(self, p0: QPointF) -> None:
        self.setPos(p0 - self.rect.center())
        self.dot.setX(p0.x())
        self.dot.setY(p0.y())

    def set_x(self, x0: float) -> None:
        self.moveBy(x0 - self.dot.x(), 0)
        self.dot.setX(x0)

    def set_y(self, y0: float) -> None:
        self.moveBy(0, y0 - self.dot.y())
        self.dot.setY(y0)


class Edge(QGraphicsObject):
    def __init__(self, P0: QPointF, P1: QPointF, parent=None):
        super(Edge, self).__init__(parent)
        self.p0 = P0    # 父节点位置
        self.p1 = P1    # 子结点位置
        self.p2 = P0    # 中间点

    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget: typing.Optional[QWidget] = ...):
        painter.setPen(Default.def_line_pen)
        painter.drawLine(self.p0, self.p2)
        painter.drawLine(self.p2, self.p1)

    def boundingRect(self) -> QRectF:
        return QRectF(self.p0.x()-1, self.p0.y()-1, 2, 2)


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.scene = QGraphicsScene(0, 0, 400, 400)
        self.view = QGraphicsView(self.scene, self)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.view.resize(402, 402)
        self.view.setRenderHint(QPainter.Antialiasing)
        node = Node(QPointF(200, 50), 'A')
        self.node = node
        node.setFlag(QGraphicsItem.ItemIsMovable)
        print(node.pos())
        print(node.y())
        print(node.boundingRect())
        self.scene.addItem(node)
        node2 = Node(QPointF(200, 100), 'B')
        edge = Edge(node.dot, node2.dot)
        edge.setZValue(-1)
        self.scene.addItem(node2)
        self.scene.addItem(edge)
        # animation = QPropertyAnimation(self.node1, b'rotation', self.scene)
        # # animation.setStartValue(self.node1.rect())
        # # animation.setEndValue(QRectF(0, 0, 80, 80))
        # # animation.setDuration(3000)
        # # animation.start()

        th = threading.Thread(target=self.pri, daemon=True)
        th.start()

    def pri(self):
        while True:
            print(self.node.scenePos() + self.node.boundingRect().center())
            print()
            time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
