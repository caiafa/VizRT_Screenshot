import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import test
from PIL import ImageChops, Image, ImageQt


class Window(QWidget, test.Ui_Form):
    def __init__(self, parent=None):
        super(Window, self).__init__()
        self.setupUi(self)
        self.imageQT = None
        self.test()

    def test(self):
        image = Image.open("d:\\1.jpg")
        self.imageQT = ImageQt.ImageQt(image)
        self.label.setPixmap(QPixmap.fromImage(self.imageQT))


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# pyuic5.bat -x interface.ui -o interface.py
