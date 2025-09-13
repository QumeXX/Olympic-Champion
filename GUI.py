import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import ImageGrab
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from Logic import text_response
from AI import AI_func

class SnippingWidget(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.outsideSquareColor = "red"
        self.squareThickness = 2

        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()


    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.end_point = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end_point = event.pos()
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        r = QtCore.QRect(self.start_point, self.end_point).normalized()
        self.hide()
        img = ImageGrab.grab(bbox=r.getCoords())
        img.save("img.png")
        QtWidgets.QApplication.restoreOverrideCursor()
        self.closed.emit()
        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()


    def paintEvent(self, event):
        trans = QtGui.QColor(22, 100, 233)
        r = QtCore.QRectF(self.start_point, self.end_point).normalized()
        qp = QtGui.QPainter(self)
        trans.setAlphaF(0.2)
        qp.setBrush(trans)
        outer = QtGui.QPainterPath()
        outer.addRect(QtCore.QRectF(self.rect()))
        inner = QtGui.QPainterPath()
        inner.addRect(r)
        r_path = outer - inner
        qp.drawPath(r_path)
        qp.setPen(
            QtGui.QPen(QtGui.QColor(self.outsideSquareColor), self.squareThickness)
        )
        trans.setAlphaF(0)
        qp.setBrush(trans)
        qp.drawRect(r)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("Olympic Champion")

        self.button = QtWidgets.QPushButton('Take Screen')
        self.button.clicked.connect(self.activateSnipping)
        self.button.setStyleSheet("margin: 10px; width: 150px; height: 50px;")

        self.answer = QtWidgets.QTextEdit("Здесь появится ответ на ваш вопрос!")
        self.answer.style()

        layout = QtWidgets.QVBoxLayout(self.centralWidget)
        layout.addWidget(self.answer, 1)
        layout.addWidget(self.button, 0)

        self.snipper = SnippingWidget()
        self.snipper.closed.connect(self.on_closed)

    def activateSnipping(self):
        self.snipper.showFullScreen()
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
        self.hide()

    def on_closed(self):
        self.answer.setText("Ждем ответа...")
        self.show()
        self.adjustSize()

        self.ai_thread = Ai()
        self.ai_thread.result_ready.connect(self.update_result)
        self.ai_thread.start()

    def update_result(self, result):
        self.answer.setText(result)

class Ai(QThread):
    result_ready = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            msg = "Реши задание, напиши ответ." + text_response()
            self.result_ready.emit(AI_func(msg))
        except Exception:
            self.result_ready.emit("Поменяйте API код в настройках. Бесплатный период закончился!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(450, 450)
    w.show()
    sys.exit(app.exec_())