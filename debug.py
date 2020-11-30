from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui     as gi
class HeaderBannerOneLineCloseButton(qt.QWidget):
#    icon_path = resources.resource_path("icons/close-white.png")
    stylesheet = """
        * {
            background: #2196f3;
            height: 56px;
        }
        QLabel#title {
            color: white;
            font-family: Ubuntu-Medium;
            font-size: 18px;
            padding-left: 31px;
            padding-right: 31px;
        }
/*
        QPushButton#closeButton {
            background-origin: content;
            background-repeat: no-repeat;
            background-position: center middle;
            background-image: url("D:/_Qt/img/close.png");   
            border: none;
        }  
*/        
/*  ++++++++++++++++++++++++++++++ */
        QToolButton{
            background:#2196f3;
            font-size:11px;
        }
        QToolButton:hover{
            background: #FF00FF;
            font-size:11px;        
        }
        """  # % (colors.primary1, icon_path)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("container")
        self.setStyleSheet(self.stylesheet)
        self.setSizePolicy(qt.QSizePolicy(qt.QSizePolicy.Expanding,
                                          qt.QSizePolicy.Fixed))
        self.titleLabel = qt.QLabel("header banner made of a label and a button", self)
        self.titleLabel.setObjectName("title")
        self.titleLabel.setSizePolicy(qt.QSizePolicy(qt.QSizePolicy.Expanding,
                                                     qt.QSizePolicy.Expanding))
#        self.closeButton = qt.QPushButton("closeButton", self)
#        self.closeButton.setObjectName("closeButton")
        close = qt.QToolButton(self)                          # +++
        close.setIcon(gi.QIcon('D:/_Qt/img/close.png'))       # +++
        close.setMinimumHeight(10)                            # +++
        close.clicked.connect(self.close)                     # +++
        layout = qt.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.titleLabel)
#        layout.addWidget(self.closeButton)
        layout.addWidget(close)                               # +++
        self.setLayout(layout)
    def setText(self, text):
        self.titleLabel.setText(text)
if __name__ == "__main__":
    import sys
    app = qt.QApplication(sys.argv)
    win = HeaderBannerOneLineCloseButton()
    win.setFixedSize(450, 35)                  # +++
    win.show()
    sys.exit(app.exec_())
 