"""
@File     : mainWindow.py
@Project  : DataStructureDemonstrationSystem
@Time     : 2022/3/5 16:15
@Author   : Ma T
@Software : PyCharm
@Last Modify Time      @Version     @Description
--------------------       --------        -----------
2022/3/5 16:15        1.0             None
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QDockWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout

from sort import *
from dataStructure import *
from match import *
from mainFrame import myWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Data
        self.tab_list = dict()

        # UI
        # 浮动控件：项目
        self.dock = QDockWidget('项目', self)
        # 浮动控件：项目 的子控件， 树控件
        self.dock_tree = QTreeWidget()
        # 选项卡控件
        self.tab = myWidget.MyQTab()

        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('欢迎使用-数据结构演示系统')
        self.resize(1200, 800)

        # 主体窗口设置
        # 加入浮动控件：项目
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        # 设置主框架和布局
        layout = QVBoxLayout()
        layout.addWidget(self.tab)
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # 部件UI
        self.__set_menu_ui()
        self.__set_tree_ui()
        # 信号机制
        self.__linked_signal()
        self.show()

    def __set_menu_ui(self):
        """
        菜单栏UI

        :return: None
        """
        # 获取菜单栏
        menu = self.menuBar()
        menu.setStyleSheet(
            """
            QMenuBar {
                background-color: white;
                border-top: 1px solid #D3D3D3;
                border-bottom: 1px solid #D3D3D3;
            }
            QMenuBar::item:selected {
                background-color: GhostWhite;
                border-top: 1px solid #D3D3D3;
                border-right: 1px solid #D3D3D3;
                border-left: 1px solid #D3D3D3;
            }
            """
        )

        # 加入菜单
        view = menu.addMenu('视图（&V）')
        view.setStyleSheet(
            """

            """
        )
        # view子菜单
        view.addAction(self.dock.toggleViewAction())

    def __set_tree_ui(self):
        """
        浮动窗口种树的UI

        :return: None
        """
        # 树的根节点1
        tree_root_sj = QTreeWidgetItem(self.dock_tree)
        tree_root_sj.setText(0, '数据结构部分')
        child_linked_list = QTreeWidgetItem(tree_root_sj)
        child_linked_list.setText(0, '链表')
        child_queue = QTreeWidgetItem(tree_root_sj)
        child_queue.setText(0, '队列')
        child_stack = QTreeWidgetItem(tree_root_sj)
        child_stack.setText(0, '栈')
        child_binary_tree = QTreeWidgetItem(tree_root_sj)
        child_binary_tree.setText(0, '树')
        child_graph = QTreeWidgetItem(tree_root_sj)
        child_graph.setText(0, '图')

        # 树的根节点2
        tree_root_sf = QTreeWidgetItem(self.dock_tree)
        tree_root_sf.setText(0, '算法部分')

        child_px = QTreeWidgetItem(tree_root_sf)
        child_px.setText(0, '排序算法')
        px_BUB = QTreeWidgetItem(child_px)
        px_BUB.setText(0, '冒泡排序')
        px_SEL = QTreeWidgetItem(child_px)
        px_SEL.setText(0, '选择排序')
        px_INS = QTreeWidgetItem(child_px)
        px_INS.setText(0, '插入排序')
        px_MER = QTreeWidgetItem(child_px)
        px_MER.setText(0, '归并排序')
        px_QUI = QTreeWidgetItem(child_px)
        px_QUI.setText(0, '快速排序')
        px_R_Q = QTreeWidgetItem(child_px)
        px_R_Q.setText(0, '随机快速排序')
        px_COU = QTreeWidgetItem(child_px)
        px_COU.setText(0, '计数排序')
        px_RAD = QTreeWidgetItem(child_px)
        px_RAD.setText(0, '基数排序')

        child_tree = QTreeWidgetItem(tree_root_sf)
        child_tree.setText(0, '树形算法')
        tree_BH = QTreeWidgetItem(child_tree)
        tree_BH.setText(0, '二叉树')

        child_str = QTreeWidgetItem(tree_root_sf)
        child_str.setText(0, '字符串匹配算法')
        str_PS = QTreeWidgetItem(child_str)
        str_PS.setText(0, '朴素字符串匹配')
        str_KMP = QTreeWidgetItem(child_str)
        str_KMP.setText(0, 'Knuth-Morris-Pratt算法')

        # 浮动控件：项目
        # 加入子控件：树
        self.dock.setWidget(self.dock_tree)

        # 项目子控件：树
        self.dock_tree.setColumnCount(1)
        self.dock_tree.expandAll()
        self.dock_tree.doubleClicked.connect(self.clicked_tree)
        self.dock_tree.setHeaderLabel('选择项->')

    def __linked_signal(self):
        """
        绑定各种信号

        :return: None
        """
        # 连接关闭页面的信号
        self.tab.close_tab_signal.connect(self.close_tab)

    def clicked_tree(self):
        """
        点击树的响应事件

        :return: None
        """
        item = self.dock_tree.currentItem()

        if item.text(0) in self.tab_list:
            self.tab.setCurrentIndex(self.tab_list[item.text(0)])

        elif item.text(0) == '链表':
            # 创建链表页面
            tab = linkedList.LinkedList()
            self.tab.addTab(tab, '链表')

            # 记录页面，设置为活动页面
            self.tab_list['链表'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '队列':
            tab = my_queue.Queue()
            self.tab.addTab(tab, '队列')
            self.tab_list['队列'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '栈':
            tab = my_stack.Stack()
            self.tab.addTab(tab, '栈')
            self.tab_list['栈'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '树':
            tab = tree.TreeWidget()
            self.tab.addTab(tab, '树')
            self.tab_list['树'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '图':
            tab = graph.MW()
            self.tab.addTab(tab, '图')
            self.tab_list['图'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '二叉树':
            tab = double_tree.DbTWidget()
            self.tab.addTab(tab, '二叉树')
            self.tab_list['二叉树'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '冒泡排序':
            tab = sort.BubbleSortView()
            self.tab.addTab(tab, '冒泡排序')
            self.tab_list['冒泡排序'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '选择排序':
            tab = sort.SelectSortView()
            self.tab.addTab(tab, '选择排序')
            self.tab_list['选择排序'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '插入排序':
            tab = sort.InsertSortView()
            self.tab.addTab(tab, '插入排序')
            self.tab_list['插入排序'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '归并排序':
            tab = sort.MergeSortView()
            self.tab.addTab(tab, '归并排序')
            self.tab_list['归并排序'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '快速排序':
            tab = sort.QuickSortView()
            self.tab.addTab(tab, '快速排序')
            self.tab_list['快速排序'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '随机快速排序':
            tab = sort.RandomQuickSortView()
            self.tab.addTab(tab, '随机快速排序')
            self.tab_list['随机快速排序'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '计数排序':
            tab = sort.CountSortView()
            self.tab.addTab(tab, '计数排序')
            self.tab_list['计数排序'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '基数排序':
            tab = sort.RadixSortView()
            self.tab.addTab(tab, '基数排序')
            self.tab_list['基数排序'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == '朴素字符串匹配':
            tab = simple.SimpleMatch()
            self.tab.addTab(tab, '朴素字符串匹配')
            self.tab_list['朴素字符串匹配'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

        elif item.text(0) == 'Knuth-Morris-Pratt算法':
            tab = kmp.KMPMatch()
            self.tab.addTab(tab, 'Knuth-Morris-Pratt算法')
            self.tab_list['Knuth-Morris-Pratt算法'] = self.tab.count() - 1
            self.tab.setCurrentIndex(self.tab.count() - 1)

    def close_tab(self, index):
        """
        关闭选项卡时处理事务

        :param index: 关闭页面的下标
        :return: None
        """
        for i in self.tab_list:
            if self.tab_list[i] == index:
                self.tab_list.pop(i)
                break

        for i in self.tab_list:
            if self.tab_list[i] > index:
                self.tab_list[i] -= 1
