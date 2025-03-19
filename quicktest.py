import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
)
from multiprocessing import Queue
import obj  #code

class CameraGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.camera_handler = obj.CameraHandler(log_dir="camera_logs")
        self.command_queue = Queue()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Camera Control Panel")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.status_label = QLabel("Status: Idle", self)
        layout.addWidget(self.status_label)

        start_button = QPushButton("Start", self)
        start_button.clicked.connect(self.start_cameras)
        layout.addWidget(start_button)

        stop_button = QPushButton("Stop", self)
        stop_button.clicked.connect(self.stop_cameras)
        layout.addWidget(stop_button)

        roi_button = QPushButton("Select ROI", self)
        roi_button.clicked.connect(self.select_roi)
        layout.addWidget(roi_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_cameras(self):
        self.camera_handler.start_cameras()
        self.status_label.setText("Status: Cameras Started")

    def stop_cameras(self):
        self.camera_handler.stop_cameras()
        self.status_label.setText("Status: Cameras Stopped")

    def select_roi(self):
        self.status_label.setText("Status: ROI Selection Started") #to be made

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = CameraGUI()
    gui.show()
    sys.exit(app.exec_())
