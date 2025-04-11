import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGroupBox, QFileDialog, QGridLayout, QLineEdit
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class CameraControlWidget(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.init_ui()
        #self.setWindowTitle("Thermal Camera Dashboard")
        #self.setGeometry(100, 100, 600, 400)
        #self.init_ui()

    def init_ui(self):
        #layout = QVBoxLayout()
         # --- Display two cameras with buttons and FPS display (is it really a thing) ---
        self.group_box = QGroupBox(self.name)

        self.video_label = QLabel("Video Feed")
        self.video_label.setFixedSize(320, 240) #fixed size later, trying sizes 
        self.video_label.setStyleSheet("background-color: lightgray; border: 1px solid black")
        self.video_label.setAlignment(Qt.AlignCenter)

        self.start_btn = QPushButton("Start Camera")
        self.stop_btn = QPushButton("Stop Camera")
        self.fps_label = QLabel("FPS: --")
        self.roi_btn = QPushButton("Select ROI")

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.fps_label)
        layout.addWidget(self.roi_btn)

        self.group_box.setLayout(layout)

class MultCamApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thermal Camera Dashboard")
        self.init_ui()
        
    def init_ui(self):
        self.pi_1m_widget = CameraControlWidget("PI 1M")
        self.pi_640_widget = CameraControlWidget("PI 640i")
        self.pi_xx_widget = CameraControlWidget("PI xx")

        self.job_label = QLabel("Job File:")
        self.job_path = QLineEdit()
        self.browse_btn = QPushButton("Browse")
        self.save_btn = QPushButton("Save Recording")

        #connect browse btn
        self.browse_btn.clicked.connect(self.browse_job_file)
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.pi_1m_widget.group_box)
        top_layout.addWidget(self.pi_640_widget.group_box)
       #top_layout.addWidget(self.pi_xx_widget.group_box)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.job_label)
        bottom_layout.addWidget(self.job_path)
        bottom_layout.addWidget(self.browse_btn)
        bottom_layout.addWidget(self.save_btn)

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
    window = MultCamApp()
    window.show()
    sys.exit(app.exec_())




        

        # --- Header with buttons and FPS display ---
        # header_layout = QHBoxLayout()

        # self.start_btn = QPushButton("Start Camera")
        # self.stop_btn = QPushButton("Stop Camera")
        # self.fps_label = QLabel("FPS: 25")
        # self.fps_slider = QSlider(Qt.Horizontal)
        # self.fps_slider.setMinimum(1)
        # self.fps_slider.setMaximum(60)
        # self.fps_slider.setValue(25)
        # self.fps_slider.valueChanged.connect(self.update_fps_label)

        # header_layout.addWidget(self.start_btn)
        # header_layout.addWidget(self.stop_btn)
        # header_layout.addWidget(self.fps_label)
        # header_layout.addWidget(self.fps_slider)

        # --- ROI and Job File ---
        # controls_layout = QHBoxLayout()

        # self.roi_dropdown = QComboBox()
        # self.roi_dropdown.addItems(["Full Frame", "Reduced Frame"])

        # self.job_file_input = QLineEdit()
        # self.job_file_input.setPlaceholderText("Select Job File")
        # self.browse_btn = QPushButton("Browse")
        # self.browse_btn.clicked.connect(self.browse_job_file)

        # controls_layout.addWidget(QLabel("ROI:"))
        # controls_layout.addWidget(self.roi_dropdown)
        # controls_layout.addWidget(QLabel("Job File:"))
        # controls_layout.addWidget(self.job_file_input)
        # controls_layout.addWidget(self.browse_btn)

        # # --- Save recording ---
        # save_layout = QHBoxLayout()
        # self.save_btn = QPushButton("Save Recording")
        # save_layout.addStretch()
        # save_layout.addWidget(self.save_btn)
        # save_layout.addStretch()

        # # --- Live Preview Placeholder ---
        # self.preview_label = QLabel("Live Preview or Logs Here")
        # self.preview_label.setStyleSheet("border: 1px solid #ccc; background: #f5f5f5;")
        # self.preview_label.setAlignment(Qt.AlignCenter)
        # self.preview_label.setMinimumHeight(150)

        # # Add all layouts to the main layout
        # layout.addLayout(header_layout)
        # layout.addLayout(controls_layout)
        # layout.addLayout(save_layout)
        # layout.addWidget(self.preview_label)

#         self.setLayout(layout)

#     def update_fps_label(self):
#         fps = self.fps_slider.value()
#         self.fps_label.setText(f"FPS: {fps}")

#     def browse_job_file(self):
#         file_path, _ = QFileDialog.getOpenFileName(self, "Select Job File", "", "Job Files (*.job)")
#         if file_path:
#             self.job_file_input.setText(file_path)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = ThermalCameraDashboard()
#     window.show()
#     sys.exit(app.exec_())
