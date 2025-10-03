from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys
import winsound
import cv2



ui_file = 'security-cam.ui'
Ui_MainWindow, BaseClass = loadUiType(ui_file)


### Main Application Class ###
class MainApp(QMainWindow, Ui_MainWindow):
    volume = 500
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        # Add your custom logic here
        self.MONITORING.clicked.connect(self.start_monitoring)
        self.EXIT.clicked.connect(self.close_application)
        self.VOLUME.clicked.connect(self.set_volume)
        self.VOLUMESLIDER.setVisible(False)
        self.VOLUMESLIDER.valueChanged.connect(self.set_volume_level)



    def start_monitoring(self):
        # Placeholder for starting monitoring logic
        print("Monitoring started...")
        webcam = cv2.VideoCapture(0)
        while True:
            _,im = webcam.read()
            _,im2 = webcam.read()
            diff = cv2.absdiff(im,im2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            _,tresh = cv2.threshold(blur, 20,255,cv2.THRESH_BINARY)
            dilated = cv2.dilate(tresh, None,iterations=3)
            contours,_ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for c in contours:
                if cv2.contourArea(c) < 5000:
                    continue
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(im, (x,y), (x+w, y+h), (0,255,0), 2)
                cv2.imwrite('intruder.jpg', im)
                image = QImage('intruder.jpg')
                pm = QPixmap.fromImage(image)
                self.CAMWINDOW.setPixmap(pm)

                winsound.Beep(self.volume, 100)
                cv2.putText(im, "Status: {}".format('Movement'), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),3)
            cv2.imshow("Security Cam",im)
            key = cv2.waitKey(10)
            if key == 27:
                break
        webcam.release()
        cv2.destroyAllWindows()

    def close_application(self):
        # Placeholder for starting monitoring logic
        self.close()

    def set_volume(self):
        # Placeholder for starting monitoring logic
        self.VOLUMESLIDER.setVisible(True)

    def set_volume_level(self):
        self.VOLUMELEVEL.setText(str(self.VOLUMESLIDER.value()//10))
        self.volume = self.VOLUMESLIDER.value() * 10
        winsound.Beep(1000, self.volume)
        cv2.waitKey(1000)
        self.VOLUMESLIDER.setVisible(False)
    



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()