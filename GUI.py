import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGroupBox, QFileDialog, QLineEdit, QComboBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class CameraControlWidget(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.init_ui()

    def init_ui(self):
        self.group_box = QGroupBox(self.name)

        self.video_label = QLabel("[Video Feed Here]")
        self.video_label.setFixedSize(320, 240)
        self.video_label.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        self.video_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start Camera")
        self.stop_button = QPushButton("Stop Camera")
        #self.fps_label = QLabel("FPS: --")
        #self.roi_button = QPushButton("Select ROI")

        self.roi_dropdown = QComboBox()
        self.roi_dropdown.addItems(["Full Frame", "Reduced Frame"])

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        #layout.addWidget(self.fps_label)
        #layout.addWidget(self.roi_button)
        layout.addWidget(QLabel("ROI Mode:"))
        layout.addWidget(self.roi_dropdown)

        self.group_box.setLayout(layout)

class DualCameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thermal Camera Dashboard")
        self.init_ui()

    def init_ui(self):
        self.pi_1m_widget = CameraControlWidget("PI 1M")
        self.pi_640_widget = CameraControlWidget("PI 640i")

        self.job_label = QLabel("Job File:")
        self.job_path = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.save_button = QPushButton("Save Recording")

        # Connect Browse Button
        self.browse_button.clicked.connect(self.browse_job_file)

        # Layouts
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.pi_1m_widget.group_box)
        top_layout.addWidget(self.pi_640_widget.group_box)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.job_label)
        bottom_layout.addWidget(self.job_path)
        bottom_layout.addWidget(self.browse_button)
        bottom_layout.addWidget(self.save_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def browse_job_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Job File")
        if file_path:
            self.job_path.setText(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DualCameraApp()
    window.show()
    sys.exit(app.exec_())