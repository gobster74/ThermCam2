from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QLineEdit, QSlider, QFileDialog
)
from PyQt5.QtCore import Qt
import sys

class ThermalCameraDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thermal Camera Dashboard")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # --- Header with buttons and FPS display ---
        header_layout = QHBoxLayout()

        self.start_btn = QPushButton("Start Camera")
        self.stop_btn = QPushButton("Stop Camera")
        self.fps_label = QLabel("FPS: 25")
        self.fps_slider = QSlider(Qt.Horizontal)
        self.fps_slider.setMinimum(1)
        self.fps_slider.setMaximum(60)
        self.fps_slider.setValue(25)
        self.fps_slider.valueChanged.connect(self.update_fps_label)

        header_layout.addWidget(self.start_btn)
        header_layout.addWidget(self.stop_btn)
        header_layout.addWidget(self.fps_label)
        header_layout.addWidget(self.fps_slider)

        # --- ROI and Job File ---
        controls_layout = QHBoxLayout()

        self.roi_dropdown = QComboBox()
        self.roi_dropdown.addItems(["Full Frame", "Center", "Top Left", "Custom"])

        self.job_file_input = QLineEdit()
        self.job_file_input.setPlaceholderText("Select Job File")
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_job_file)

        controls_layout.addWidget(QLabel("ROI:"))
        controls_layout.addWidget(self.roi_dropdown)
        controls_layout.addWidget(QLabel("Job File:"))
        controls_layout.addWidget(self.job_file_input)
        controls_layout.addWidget(self.browse_btn)

        # --- Save recording ---
        save_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Recording")
        save_layout.addStretch()
        save_layout.addWidget(self.save_btn)
        save_layout.addStretch()

        # --- Live Preview Placeholder ---
        self.preview_label = QLabel("Live Preview or Logs Here")
        self.preview_label.setStyleSheet("border: 1px solid #ccc; background: #f5f5f5;")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(150)

        # Add all layouts to the main layout
        layout.addLayout(header_layout)
        layout.addLayout(controls_layout)
        layout.addLayout(save_layout)
        layout.addWidget(self.preview_label)

        self.setLayout(layout)

    def update_fps_label(self):
        fps = self.fps_slider.value()
        self.fps_label.setText(f"FPS: {fps}")

    def browse_job_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Job File", "", "Job Files (*.job)")
        if file_path:
            self.job_file_input.setText(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ThermalCameraDashboard()
    window.show()
    sys.exit(app.exec_())
