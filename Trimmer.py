import cv2
import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setAcceptDrops(True)
        self.setWindowTitle("Trimmer")

        mainLayout = QVBoxLayout()

        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)

        self.setLayout(mainLayout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            img = cv2.imread(file_path)
            b, g, r = cv2.split(img)
            coords_b = cv2.findNonZero(cv2.bitwise_not(b))
            coords_g = cv2.findNonZero(cv2.bitwise_not(g))
            coords_r = cv2.findNonZero(cv2.bitwise_not(r))
            xb, yb, wb, hb = cv2.boundingRect(coords_b)
            xg, yg, wg, hg = cv2.boundingRect(coords_g)
            xr, yr, wr, hr = cv2.boundingRect(coords_r)
            x = min(xb, xg, xr)
            y = min(yb, yg, yr)
            w = max(wb, wg, wr)
            h = max(hb, hg, hr)
            crop = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image
            base, ext = os.path.splitext(file_path)
            cv2.imwrite(base + '_cropped' + ext, crop)

            img_converted = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB) 
            height, width, channel = img_converted.shape
            img_qt = QImage(img_converted.data, width, height, width * channel, QImage.Format_RGB888)



            pixmap = QPixmap(img_qt)
            self.set_image(pixmap)

            event.accept()
        else:
            event.ignore()

    def set_image(self, pixmap):
        self.photoViewer.setPixmap(pixmap)

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())