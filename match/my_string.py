"""
@File     : my_string.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/3/19 21:49
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/19 21:49        1.0             None
"""
import random
from abc import abstractmethod

from PyQt5.QtCore import pyqtSignal, QPointF, QRectF, Qt, QPropertyAnimation, QRegExp
from PyQt5.QtGui import QFont, QPainter, QColor, QPen, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextBrowser, QDialog, QLabel, \
    QLineEdit, QFormLayout, QInputDialog


class NewStrButton(QDialog):
    new_str_signal = pyqtSignal(str, str)

    def __init__(self, t_str='', p_str='', parent=None):
        super(NewStrButton, self).__init__(parent)
        self.t_str = t_str
        self.p_str = p_str
        self.t_label = QLabel()
        self.p_label = QLabel()
        self.t_line_edit = QLineEdit()
        self.p_line_edit = QLineEdit()
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('创建字符串-在T串中找到P串')

        self.t_label.setText(self.t_str)
        self.t_label.setFont(QFont('', 14))
        self.p_label.setText(self.p_str)
        self.p_label.setFont(QFont('', 14))

        btn1 = QPushButton('随机创建T串')
        btn2 = QPushButton('随机创建P串')
        btn3 = QPushButton('确定')
        btn4 = QPushButton('取消')
        btn5 = QPushButton('确定')
        btn6 = QPushButton('确定')

        btn1.clicked.connect(self.__click_bt1)
        btn2.clicked.connect(self.__click_bt2)
        btn3.clicked.connect(self.__click_bt3)
        btn4.clicked.connect(self.__click_bt4)
        btn5.clicked.connect(self.__click_bt5)
        btn6.clicked.connect(self.__click_bt6)

        validator = QRegExpValidator()
        validator.setRegExp(QRegExp('[a-z]*$'))
        self.t_line_edit.setValidator(validator)
        self.p_line_edit.setValidator(validator)
        self.t_line_edit.setPlaceholderText('输入T串')
        self.p_line_edit.setPlaceholderText('输入P串')

        layout_t = QHBoxLayout()
        layout_p = QHBoxLayout()
        layout_t.addWidget(self.t_line_edit)
        layout_t.addWidget(btn5)
        layout_p.addWidget(self.p_line_edit)
        layout_p.addWidget(btn6)
        layout_ok = QHBoxLayout()
        layout_ok.addWidget(btn3)
        layout_ok.addWidget(btn4)
        layout_ok.setAlignment(Qt.AlignCenter)
        layout = QFormLayout()
        layout.addRow(QLabel('T串:'), self.t_label)
        layout.addRow(QLabel('P串:'), self.p_label)
        layout.addRow(btn1)
        layout.addRow(btn2)
        layout.addRow(QLabel('自定义T串:'), layout_t)
        layout.addRow(QLabel('自定义P串:'), layout_p)
        layout.addRow(QLabel(), layout_ok)
        self.setLayout(layout)

    def __click_bt1(self):
        s = ''
        for i in range(random.randint(18, 23)):
            s += ['a', 'b', 'c'][random.randint(0, 2)]
        self.t_str = s
        self.t_label.setText(self.t_str)

    def __click_bt2(self):
        s = ''
        for i in range(random.randint(3, 6)):
            s += ['a', 'b', 'c'][random.randint(0, 2)]
        self.p_str = s
        self.p_label.setText(self.p_str)

    def __click_bt3(self):
        # noinspection PyUnresolvedReferences
        self.new_str_signal.emit(self.t_str, self.p_str)
        self.close()

    def __click_bt4(self):
        self.close()

    def __click_bt5(self):
        if len(self.t_line_edit.text()) > 23:
            self.t_label.setText('输入字符串过长')
        else:
            self.t_str = self.t_line_edit.text()
            self.t_label.setText(self.t_str)

    def __click_bt6(self):
        if len(self.p_line_edit.text()) > 20:
            self.p_label.setText('输入字符串过长')
        else:
            self.p_str = self.p_line_edit.text()
            self.p_label.setText(self.p_str)


class AnimationView(QWidget):
    _width = 34
    _height = 34
    _border_px = 2
    _v_space = 10

    _bottom = 100
    _top = 100

    _fontSize = 16

    arrow_signal = pyqtSignal(int)
    p_str_signal = pyqtSignal(int)

    def __init__(self, t_string='', p_string='', parent=None, ):
        super(AnimationView, self).__init__(parent)
        # 数组
        self.t_string = t_string
        self.p_string = p_string
        # 绘图数据
        self.arrow_button = QPushButton('↑', self)
        self.t_button_list = []
        self.p_button_list = []
        # 动画标记
        self._no_act = True
        self.act_speed = 500
        # 绑定信号
        # noinspection PyUnresolvedReferences
        self.arrow_signal.connect(self.move_arrow)
        # noinspection PyUnresolvedReferences
        self.p_str_signal.connect(self.move_p_str)
        # 初始化
        self.__init_ui()

    def __init_ui(self):
        self.resize(800, 400)
        self.setMinimumSize(800, 400)

    def __init_data(self):
        def clear_btn(btn0: QPushButton):
            btn0.close()
            btn0.deleteLater()

        x0 = (self.width() - len(self.t_string) * (self._width - self._border_px)) // 2
        for i in self.t_button_list:
            clear_btn(i)
        for i in self.p_button_list:
            clear_btn(i)
        self.t_button_list.clear()
        self.p_button_list.clear()

        # 箭头
        self.arrow_button.resize(self._width, self._height)
        self.arrow_button.move(x0, self._top + self._height + self._v_space)
        self.arrow_button.setFont(QFont('', self._fontSize + 10, 2))
        self.arrow_button.setEnabled(False)
        self.arrow_button.setStyleSheet(
                """
                    QPushButton {
                        border-style: outset;
                        border-width: 0px;
                        color: rgb(10, 10, 10);
                    }
                """
            )
        # 绘制T串
        for i in range(len(self.t_string)):
            btn = QPushButton(self.t_string[i], self)
            btn.setEnabled(False)
            btn.setFont(QFont('', self._fontSize, 2))
            btn.resize(self._width, self._height)
            btn.move(x0 + i * (self._width - self._border_px), self._top)
            btn.setStyleSheet("""
                            QPushButton {  
                                 border-style: outset;
                                 border-width: 2px;
                                 border-color: rgb(28, 28, 28); 
                                 color: rgb(30, 144, 255);
                            }  
                        """)
            btn.show()
            self.t_button_list.append(btn)
        # 绘制P串
        for i in range(len(self.p_string)):
            btn = QPushButton(self.p_string[i], self)
            btn.setEnabled(False)
            btn.setFont(QFont('', self._fontSize, 2))
            btn.resize(self._width, self._height)
            btn.move(x0 + i * (self._width - self._border_px), self._top + 2 * (self._v_space + self._height))
            btn.setStyleSheet("""
                   QPushButton {  
                        border-style: outset;
                        border-width: 2px;
                        border-color: rgb(28, 28, 28); 
                        color: rgb(255, 52, 179);
                   }  
               """)
            btn.show()
            self.p_button_list.append(btn)

    def set_all_str(self, t_s, p_s):
        self.t_string = t_s
        self.p_string = p_s
        self.__init_data()

    def resizeEvent(self, a0) -> None:
        if self._no_act:
            self.__init_data()

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
        # 消除画笔
        paint.end()

    def set_arrow_btn_red(self):
        self.arrow_button.setStyleSheet("""
                    QPushButton {
                                border-style: outset;
                                border-width: 0px;
                                color: rgb(248, 10, 10);
                            }
                    """)

    def set_arrow_btn_green(self):
        self.arrow_button.setStyleSheet("""
                    QPushButton {
                                border-style: outset;
                                border-width: 0px;
                                color: rgb(10, 140, 10);
                            }
                    """)

    def move_arrow(self, x0=0):
        # x0 == 0, 移动到p_str的开头
        self.arrow_button.setStyleSheet("""
                            QPushButton {
                                        border-style: outset;
                                        border-width: 0px;
                                        color: rgb(10, 10, 10);
                                    }
                            """)

        animation = QPropertyAnimation(self.arrow_button, b'pos', self)
        animation.setStartValue(self.arrow_button.pos())
        if x0 == 0:
            animation.setEndValue(QPointF(self.p_button_list[0].x(), self.arrow_button.y()))
        else:
            animation.setEndValue(
                QPointF(
                    self.arrow_button.x() + x0 * (self._width - self._border_px),
                    self.arrow_button.y()
                )
            )
        animation.setDuration(self.act_speed)
        animation.start()

    def move_p_str(self, x0=1):
        for i in self.p_button_list:
            animation = QPropertyAnimation(i, b'pos', self)
            animation.setStartValue(i.pos())
            animation.setEndValue(QPointF(i.x() + x0 * (self._width - self._border_px), i.y()))
            animation.setDuration(self.act_speed)
            animation.start()


class AnimationWidget(QWidget):
    def __init__(self, parent=None):
        super(AnimationWidget, self).__init__(parent)
        # 字符串
        self.t_str = ''
        self.p_str = ''
        # 动画区对象
        self.animation_widget = AnimationView()
        # 文本区
        self.text_list = []
        self.text_widget = QWidget()
        self.text_view = QTextBrowser()

        self.__init_data()
        self.__init_ui()

    def __init_data(self):
        self.t_str = ''
        self.p_str = ''
        for i in range(random.randint(18, 23)):
            self.t_str += ['a', 'b', 'c'][random.randint(0, 2)]
        for i in range(random.randint(3, 5)):
            self.p_str += ['a', 'b', 'c'][random.randint(0, 2)]
        self.animation_widget.set_all_str(self.t_str, self.p_str)

    def __init_ui(self):
        self.text_widget.setLayout(QVBoxLayout())
        self.text_widget.layout().setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.text_widget.setStyleSheet('QWidget{border: 1px solid #D3D3D3;}')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.text_widget)
        bottom_layout.addWidget(self.text_view)
        bottom_layout.addLayout(self.__button_layout())

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.animation_widget)
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
        self.animation_widget.set_all_str(self.t_str, self.p_str)
        self.start_match()
        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)

    def btn_clicked2(self):
        self.animation_widget.set_all_str(self.t_str, self.p_str)
        self.text_view.clear()

    def btn_clicked3(self):
        dialog = NewStrButton(self.t_str, self.p_str, self)
        # noinspection PyUnresolvedReferences
        dialog.new_str_signal.connect(self.animation_widget.set_all_str)
        dialog.exec()
        self.t_str = self.animation_widget.t_string
        self.p_str = self.animation_widget.p_string

    def btn_clicked4(self):
        num, ok = QInputDialog.getDouble(self, '设置演示速度', '单位：秒')
        if ok and num:
            self.animation_widget.act_speed = num * 1000

    @abstractmethod
    def start_match(self):
        pass

