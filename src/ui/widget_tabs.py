from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
import ui.widget_main as widget_main
import ui.widget_mdb as widget_mdb

class Ui_widget_tabs(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.tabWidget.currentChanged.connect(self.tab_changed)
        self.adjust_size()

    def tab_changed(self, index: int) -> None:
        # Change size of window to fit the tab
        self.adjust_size()

    def adjust_size(self) -> None:
        current_tab = self.tabWidget.currentWidget()
        current_size = current_tab.size()

        # Add offsets on all sides
        current_size.setWidth(current_size.width() + 28)
        current_size.setHeight(current_size.height() + 48)

        print(current_size)
        self.setFixedSize(current_size)

    def setupUi(self, widget_tabs):
        if not widget_tabs.objectName():
            widget_tabs.setObjectName(u"widget_tabs")
        widget_tabs.resize(678, 459)
        
        # Disable resizing
        widget_tabs.setFixedSize(widget_tabs.size())

        widget_tabs.setWindowTitle(u"Carotene")
        self.verticalLayout = QVBoxLayout(widget_tabs)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(widget_tabs)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tab_home = widget_main.Ui_widget_main()
        self.tab_home.setObjectName(u"tab_home")
        self.tabWidget.addTab(self.tab_home, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_home), u"Home")
        self.tab_2 = widget_mdb.Ui_widget_mdb()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabWidget.addTab(self.tab_4, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(widget_tabs)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(widget_tabs)
    # setupUi

    def retranslateUi(self, widget_tabs):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("widget_tabs", u"MDB", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("widget_tabs", u"Assembly", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("widget_tabs", u"Story", None))
        pass
    # retranslateUi

