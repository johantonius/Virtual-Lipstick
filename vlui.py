import sysconfig
import face_recognition
from PIL import Image, ImageDraw
import sys
import string
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QDir, Qt,QFileInfo
from PyQt5.QtGui import QImage, QPainter, QPalette, QPixmap, QColor,QIntValidator
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,QFrame,
        QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy, QColorDialog, QLineEdit, QComboBox)

class Window(QMainWindow):
    #imagename = pyqtSignal('QString')
    def __init__(self):
        super(Window,self).__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Virtual Lipstick")
        self.resize(500, 400)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.resize(300,400)
        self.imageLabel.move(150, 100)


        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)
        

        self.btn_upload = QtWidgets.QPushButton('Browse', self)
        self.btn_upload.clicked.connect(self.btn_open)
        self.btn_upload.move(420,50)
        
        self.btn_color = QtWidgets.QPushButton('Lipstick Color', self)
        self.btn_color.clicked.connect(self.choose_color)
        self.btn_color.move(420,100)
        self.btn_color.resize(150,20)

        self.btn_Order = QtWidgets.QPushButton('Order', self)
        self.btn_Order.clicked.connect(self.buy)
        self.btn_Order.move(420,510)

        self.comboBox = QComboBox(self)
        self.comboBox.addItem("-Choose Lipstick Brand-")
        self.comboBox.addItem("Mac")
        self.comboBox.addItem("Wardah")
        self.comboBox.addItem("Kylie Cosmetic")
        self.comboBox.move(420, 150)
        self.comboBox.resize(180, 30)
        self.comboBox.activated.connect(self.style_choice)


        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.nameLabel.move(350,200)
        self.nameline = QLineEdit(self)
        self.nameline.move(420, 200)
        self.nameline.resize(200, 32)

        self.addressLabel = QLabel(self)
        self.addressLabel.setText('Address:')
        self.addressLabel.move(350,250)
        self.addressline = QLineEdit(self)
        self.addressline.move(420, 250)
        self.addressline.resize(200, 50)

        self.emailLabel = QLabel(self)
        self.emailLabel.setText('Email:')
        self.emailLabel.move(350,310)
        self.emailline = QLineEdit(self)
        self.emailline.move(420, 310)
        self.emailline.resize(200, 32)

        self.qtyLabel = QLabel(self)
        self.qtyLabel.setText('Quantity:')
        self.qtyLabel.move(350,360)
        self.qtyline = QLineEdit(self)
        self.onlyInt = QIntValidator()
        self.qtyline.setValidator(self.onlyInt)
        self.qtyline.move(420, 360)
        self.qtyline.resize(32, 32)
        self.qtyline.keyboard_type = 'numeric'

        self.priceLabel = QLabel(self)
        self.priceLabel.setText('Price:')
        self.priceLabel.move(350,410)
        self.pricelLabel = QLabel(self)
        self.pricelLabel.setText('Rp. 0')
        self.pricelLabel.move(420,410)

        self.totalpriceLabel = QLabel(self)
        self.totalpriceLabel.setText('Total :')
        self.totalpriceLabel.move(350,460)
        self.totalLabel = QLabel(self)

        self.facesLabel = QLabel(self)
        self.facesLabel.move(420, 120)


        self.btn_total = QtWidgets.QPushButton('Total', self)
        self.btn_total.clicked.connect(self.total)
        self.btn_total.move(500,460)


        self.val = 0
        self.alpha = 0
        self.show()

    def style_choice(self):
        if self.comboBox.currentText() == "Kylie Cosmetic":
            self.alpha = 225
            self.pricelLabel.setText('Rp. 350000')
        if self.comboBox.currentText() == "Mac":
            self.alpha = 200
            self.pricelLabel.setText('Rp. 200000')
        if self.comboBox.currentText() == "Wardah":
            self.alpha = 170
            self.pricelLabel.setText('Rp. 155000')


    def total(self):
        if self.qtyline.text() !="":
            if self.comboBox.currentText() == "Kylie Cosmetic":
                self.totalLabel.setText('Rp. %s' % str(int(self.qtyline.text())*350000))
            if self.comboBox.currentText() == "Mac":
                self.totalLabel.setText('Rp. %s' % str(int(self.qtyline.text())*200000))
            if self.comboBox.currentText() == "Wardah":
                self.totalLabel.setText('Rp. %s' % str(int(self.qtyline.text())*155000))
            self.totalLabel.move(420,460)
        else :
            QMessageBox.about(self, "Error", "Please input Quantity first")

    def btn_open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File",
                QDir.currentPath(), '*.jpg *.png')
        self.fileimage = fileName
        if fileName:
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.val = 1
       
        return fileName
  
    def buy(self):
        if self.nameline.text() != "" and self.addressline.text() != "" and self.qtyline.text() !="" and self.emailline.text()!="":
            QMessageBox.about(self, "Order", "Order Successfull. Payment will be emailed")
        else :
            QMessageBox.about(self, "Order", "Please complete the data")
    def choose_color(self):
        if self.val==0 :
            QMessageBox.about(self, "Error", "Please browse image first") 
            if self.comboBox.currentText() == "-Choose Lipstick Brand-":
                QMessageBox.about(self, "Error", "Please choose Lipstick Brand")
        else:
            if self.comboBox.currentText() == "-Choose Lipstick Brand-":
                QMessageBox.about(self, "Error", "Please choose Lipstick Brand")
            else :
                fname = self.fileimage
                imagelip = face_recognition.load_image_file(fname)
                face_locations = face_recognition.face_locations(imagelip)
                if len(face_locations) == 0:
                    self.facesLabel.setText("Found 0 face")
                else:
                    self.facesLabel.setText("")
                    selected_color = QColorDialog.getColor()
                    face_landmarks_list = face_recognition.face_landmarks(imagelip)
                    selected_color = QColorDialog.getColor()
                    r = selected_color.red()
                    g = selected_color.green()
                    b = selected_color.blue()
                    if selected_color.isValid():
                        pil_image = Image.fromarray(imagelip)
                        for face_landmarks in face_landmarks_list:
                            d = ImageDraw.Draw(pil_image, 'RGBA')
                            d.polygon(face_landmarks['top_lip'], fill=(r, g, b, self.alpha))
                            d.polygon(face_landmarks['bottom_lip'], fill=(r, g, b, self.alpha))
                            d.line(face_landmarks['top_lip'], fill=(r, g, b, 64), width=1)
                            d.line(face_landmarks['bottom_lip'], fill=(r, g, b, 64), width=1)

                    im = pil_image.convert("RGBA")
                    data = im.tobytes('raw', "RGBA")
                    qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_RGBA8888)
                    pixmap = QtGui.QPixmap.fromImage(qim)
                    self.imageLabel.setPixmap(pixmap)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    Main_Window = Window()
    Main_Window.show()
    sys.exit(app.exec_())