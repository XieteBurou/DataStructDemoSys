"""
@File     : simple.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/3/21 15:47
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/21 15:47        1.0             None
"""

import time
import threading

from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import QLabel

from match import my_string


class SimpleMatch(my_string.AnimationWidget):
    def __init__(self, parent=None):
        super(SimpleMatch, self).__init__(parent=parent)
        label_list = [
            QLabel('i 从 T串左侧 到 T串右侧'),
            QLabel('    j 从 P串左侧 到 P串右侧'),
            QLabel('        if str[i] == str[j] 则 j向右移动'),
            QLabel('        否则 i向右移动，j回到P串首位')
        ]
        font = QFont()
        font.setPointSize(13)
        for i in label_list:
            i.setFont(font)
        self.text_list = label_list
        for i in label_list:
            self.text_widget.layout().addWidget(i)

    def matching(self):
        for i in range(len(self.t_str) - len(self.p_str) + 1):
            self.text_list[0].setStyleSheet('background-color: rgb(0, 191, 255)')
            time.sleep(self.animation_widget.act_speed / 1000)
            self.text_list[0].setStyleSheet('')
            flag = True
            for j in range(len(self.p_str)):
                self.text_list[1].setStyleSheet('background-color: rgb(0, 191, 255);')
                time.sleep(self.animation_widget.act_speed / 1000)
                self.text_list[1].setStyleSheet('')
                if self.animation_widget.t_string[i+j] == self.animation_widget.p_string[j]:
                    self.text_list[2].setStyleSheet('background-color: rgb(0, 191, 255);')
                    self.animation_widget.set_arrow_btn_green()
                    time.sleep(self.animation_widget.act_speed / 1000)
                    if j < len(self.p_str) - 1:
                        self.text_view.append('    指针位置字符相同，向右移动指针')
                        self.animation_widget.arrow_signal.emit(1)
                        time.sleep(self.animation_widget.act_speed / 1000 + 0.05)
                    self.text_list[2].setStyleSheet('')
                else:
                    self.text_list[3].setStyleSheet('background-color: rgb(0, 191, 255);')
                    self.text_view.append('    指针位置字符不同! 退出内层循环, 指针移向P串首位')
                    self.animation_widget.set_arrow_btn_red()
                    time.sleep(self.animation_widget.act_speed / 1000)
                    self.text_list[3].setStyleSheet('')
                    flag = False
                    break
                self.text_view.moveCursor(QTextCursor.End)
            if flag:
                self.text_view.append('    在指针对应位置找到T串中出现的第一个P串！')
                self.text_view.moveCursor(QTextCursor.End)
                break
            else:
                if i < len(self.t_str) - len(self.p_str):
                    self.text_view.append('    向右移动P串！')
                    self.animation_widget.p_str_signal.emit(1)
                    time.sleep(self.animation_widget.act_speed / 1000 + 0.05)
                    self.animation_widget.arrow_signal.emit(0)
                    time.sleep(self.animation_widget.act_speed / 1000 + 0.05)
                else:
                    self.text_view.append('    未在T串中找到P串！')
                    self.text_view.moveCursor(QTextCursor.End)
        self.animation_widget._no_act = True
        self.button1.setEnabled(True)
        self.button2.setEnabled(True)
        self.button3.setEnabled(True)

    def start_match(self):
        self.animation_widget._no_act = False
        thread = threading.Thread(target=self.matching, daemon=True)
        thread.start()
