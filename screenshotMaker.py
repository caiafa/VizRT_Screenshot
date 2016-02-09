import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import interface
import error
from getScreenshot import Screenshot, ScreenshotError
from PIL import ImageChops
from readPopupFile import Popups
import configuration
import logging


def image_equal(image1, image2):
    return ImageChops.difference(image1, image2).getbbox() is None


class Dialog(QDialog, error.Ui_Dialog):
    def __init__(self, error_message):
        super(Dialog, self).__init__()
        self.setupUi(self)
        self.errorMessage.setText(error_message)


# noinspection PyBroadException
class Window(QWidget, interface.Ui_Form):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.__setup_buttons()
        self.image1 = None
        self.image2 = None
        self.fill_drop_down()

    def fill_drop_down(self):
        popup_ids = Popups(popup_list=configuration.popup_list_path).active
        self.popupIdField.addItems(popup_ids)

    def __setup_buttons(self):
        self.actionButton.clicked.connect(self.__generate_snapshot)
        self.saveButton1.clicked.connect(self.save_image_1)
        self.saveButton2.clicked.connect(self.save_image_2)

    def __generate_snapshot(self):
        popup_id = self.popupIdField.currentText()[0:5]
        self.__disable_save_buttons()

        if len(popup_id) == 5:
            try:
                self.image1 = Screenshot(scene_name=popup_id, frame_index='$1', mode='named')
                self.image2 = Screenshot(scene_name=popup_id, frame_index='$2', mode='named')

                self.__display_captures()
                self.__enable_save_buttons()
            except FileNotFoundError:
                self.error = Dialog('id-ul nu poate fi gasit')
                self.error.show()
            except ScreenshotError:
                self.error = Dialog('ceva nu a mers')
                self.error.show()
        else:
            self.error = Dialog('id-ul trebuie sa aiba 5 caractere')
            self.error.show()

    def __disable_save_buttons(self):
        self.saveButton1.setEnabled(False)
        self.saveButton2.setEnabled(False)

    def __enable_save_buttons(self):
        self.saveButton1.setEnabled(True)
        self.saveButton2.setEnabled(True)

    def save_image_1(self):
        self.__save_files(self.image1)

    def save_image_2(self):
        self.__save_files(self.image2)

    def __save_files(self, image):
        save_location = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.jpg)")
        if save_location:
            try:
                image.composite_image.save(save_location[0].replace('.jpg', '_1.jpg'))
            except:
                pass
        else:
            self.saveFiles()

    def __display_captures(self):
        try:
            self.labelTab1.setPixmap(QPixmap.fromImage(self.image1.qt_image).scaledToWidth(960))
            self.labelTab2.setPixmap(QPixmap.fromImage(self.image2.qt_image).scaledToWidth(960))
        except:
            pass


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error("main crashed {0}".format(str(e)))

        # pyuic5.bat -x interface.ui -o interface.py
        # self.label.setPixmap(QPixmap.fromImage(self.imageQT))
