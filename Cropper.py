import sys
import os
import cv2 as cv
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Cut(QMainWindow):
    def __init__(self):
        super(Cut, self).__init__()
        self.current_num = 1
        self.total_num = 0
        self.X = 0
        self.Y = 0

        # 固定裁剪框尺寸
        self.width = 224
        self.height = 224
        self.img_dir = ""
        self.save_dir = "E:/fun/Python/save/"

        self.resize(1024, 900)
        self.setWindowTitle("GUI")

        self.label1 = QLabel(self)
        self.label1.setFixedSize(1024, 768)
        self.label1.move(0, 0)

        self.btn1 = QPushButton('File', self)
        self.btn1.setFixedSize(100, 50)
        self.btn1.move(150, 800)
        self.btn1.clicked.connect(self.openDialog)

        self.btn2 = QPushButton('Next', self)
        self.btn2.setFixedSize(100, 50)
        self.btn2.move(300, 800)
        self.btn2.clicked.connect(self.loadNextImage)

        self.btn3 = QPushButton('Clear', self)
        self.btn3.setFixedSize(100, 50)
        self.btn3.move(450, 800)
        self.btn3.clicked.connect(self.clearRec)

        self.label2 = QLabel(self)
        self.label2.setFixedSize(200, 50)
        self.label2.move(600, 800)


    # 选择图片
    def openDialog(self):

        #self.img_dir = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", 'E:/design/project/data/data/')
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", 'E:/design/project/data/data/')
        self.img_dir = imgName[0:imgName.rfind('/')+1]
        cnt = 1
        for file in os.listdir(self.img_dir):
            if file ==  imgName[imgName.rfind('/')+1:]:
                self.current_num = cnt
            self.total_num += 1
            cnt += 1

        self.label2.setText(str(self.current_num) + ' of ' + str(self.total_num))
        jpg = QtGui.QPixmap(imgName).scaled(self.label1.width(), self.label1.height())
        self.label1.setPixmap(jpg)


    # 加载下一张图片
    def loadNextImage(self):

        imgName = self.img_dir + os.listdir(self.img_dir)[self.current_num - 1]
        img = cv.imread(imgName)
        img = img[int(self.Y - self.height / 2) : int(self.Y + self.height / 2), int(self.X - self.width / 2) : int(self.X + self.width / 2)]
        cv.imwrite('E:/fun/Python/save/' + os.listdir(self.img_dir)[self.current_num - 1], img)

        if self.current_num == self.total_num:
            print("It's the last image in the selected folder")
        else:
            self.current_num += 1
            self.label2.setText(str(self.current_num) + ' of ' + str(self.total_num))
            imgName = self.img_dir + os.listdir(self.img_dir)[self.current_num - 1]
            jpg = QtGui.QPixmap(imgName).scaled(self.label1.width(), self.label1.height())
            self.label1.setPixmap(jpg)


    # 消除矩形框
    def clearRec(self):

        imgName = self.img_dir + os.listdir(self.img_dir)[self.current_num - 1]
        img = cv.imread(imgName)
        jpg = QtGui.QPixmap(imgName).scaled(self.label1.width(), self.label1.height())
        self.label1.setPixmap(jpg)

    # 鼠标点击事件，显示矩形框
    def mousePressEvent(self, event):

        s = event.windowPos()
        self.X = int(s.x())
        self.Y = int(s.y())
        imgName = self.img_dir + os.listdir(self.img_dir)[self.current_num - 1]
        img = cv.imread(imgName)
        cv.rectangle(img, (self.X - int(self.width / 2), self.Y - int(self.height / 2)), (self.X + int(self.width / 2), self.Y + int(self.height / 2)), (0, 0, 255), 2)
        '''cv.imshow("img", img)
        cv.waitKey(0)    #wait for  key to exit
        cv.destroyAllWindows()  '''

        # 在label中显示opencv处理的图片
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # 将BGR转为RGB
        self.QtImg = QtGui.QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)#转化为QImage
        self.label1.setPixmap(QtGui.QPixmap.fromImage(self.QtImg))
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = Cut()
    my.show()
    sys.exit(app.exec_())