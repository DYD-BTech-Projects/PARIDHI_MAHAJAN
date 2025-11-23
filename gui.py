import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QTextEdit, QScrollArea, QStackedWidget, QHBoxLayout,
    QInputDialog, QMessageBox, QGridLayout, QFileDialog,
    QFrame, QProgressBar
)
from PyQt6.QtGui import QFont, QPalette, QColor, QCursor
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

# -----------------------------
# FILE PASSWORDS
# -----------------------------
FILE_PASSWORDS = {
    "file1.txt": ("student1", "pass1"),
    "file2.txt": ("student2", "pass2"),
    "file3.txt": ("student3", "pass3"),
    "file4.txt": ("student4", "pass4"),
    "file5.txt": ("student5", "pass5"),
    "file6.txt": ("student6", "pass6"),
    "file7.txt": ("student7", "pass7"),
    "file8.txt": ("student8", "pass8"),
    "file9.txt": ("student9", "pass9"),
    "file10.txt": ("student10", "pass10")
}

# -----------------------------
# SPLASH SCREEN
# -----------------------------
class AnimatedSplash(QWidget):
    proceed = pyqtSignal()  # signal to move to instruction screen

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chowkidaar - File Monitor")
        self.setGeometry(200, 200, 800, 450)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#B0E0E6"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_title = QLabel("👮 Chowkidaar 🗃🗄")
        self.label_title.setFont(QFont("Algerian", 60, QFont.Weight.Bold))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: #1E3F66;")
        layout.addWidget(self.label_title)

        self.label_sub = QLabel("Your Real-Time File Access Monitor")
        self.label_sub.setFont(QFont("Arial", 18, QFont.Weight.DemiBold))
        self.label_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_sub.setStyleSheet("color: #FF4500;")
        layout.addWidget(self.label_sub)

        self.label_welcome = QLabel("Welcome!")
        self.label_welcome.setFont(QFont("Comic Sans MS", 20, QFont.Weight.Bold))
        self.label_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_welcome.setStyleSheet("color: #1E3F66;")
        layout.addWidget(self.label_welcome)

        self.btn_next = QPushButton("Let's Start ➡")
        self.btn_next.setFont(QFont("Comic Sans MS", 18, QFont.Weight.Bold))
        self.btn_next.setStyleSheet("background-color: #1E90FF; color: white; border-radius: 10px; padding: 10px 20px;")
        self.btn_next.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_next.clicked.connect(lambda: self.proceed.emit())
        layout.addWidget(self.btn_next, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        self.blink_state = True
        self.timer_blink = QTimer()
        self.timer_blink.timeout.connect(self.blink_subtitle)
        self.timer_blink.start(500)

        self.emoji_timer = QTimer()
        self.emoji_timer.timeout.connect(self.slide_emoji)
        self.emoji_timer.start(50)
        self.emoji_pos = 0
        self.direction = 1

    def blink_subtitle(self):
        self.blink_state = not self.blink_state
        color = "#FF4500" if self.blink_state else "#FFA07A"
        self.label_sub.setStyleSheet(f"color: {color};")

    def slide_emoji(self):
        spaces = " " * self.emoji_pos
        self.label_title.setText(f"{spaces}👮 Chowkidaar 🗃🗄")
        self.emoji_pos += self.direction
        if self.emoji_pos > 10 or self.emoji_pos < 0:
            self.direction *= -1

# -----------------------------
# INSTRUCTION SCREEN
# -----------------------------
class InstructionScreen(QWidget):
    proceed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chowkidaar - Instructions")
        self.setGeometry(200, 200, 850, 550)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#E0FFFF"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)

        label_title = QLabel("📖 How to Use the Application")
        label_title.setFont(QFont("Comic Sans MS", 26, QFont.Weight.Bold))
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_title.setStyleSheet("color: #1E3F66;")
        layout.addWidget(label_title)

        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setFont(QFont("Arial", 14))
        instructions.setStyleSheet("background-color: #F0FFFF; border: 2px solid #1E3F66; padding: 15px; color: #333333;")
        instructions.setHtml("""
        <h3 style="color:#1E3F66;">1. File Ownership</h3>
        <p style="font-size:14pt; color:#333333;">
        There are <b>9 files</b>, each created by a student. Each student is the <span style="color:#FF4500;"><b>owner</b></span> of their respective file.
        </p>
        <h3 style="color:#1E3F66;">2. Accessing Files</h3>
        <p style="font-size:14pt; color:#333333;">
        All files must be accessed via the following <span style="color:#1E90FF;"><b>system calls</b></span>:
        </p>
        <ul style="font-size:14pt; color:#333333;">
            <li><b>CreateFile()</b> - Open a file</li>
            <li><b>ReadFile()</b> - Read a file</li>
            <li><b>WriteFile()</b> - Modify a file</li>
            <li><b>CloseHandle()</b> - Close a file</li>
        </ul>
        <h3 style="color:#1E3F66;">3. Rules & Security</h3>
        <p style="font-size:14pt; color:#333333;">
        - Students can modify only their <span style="color:#FF4500;"><b>own file</b></span>.<br>
        - Each file has a <span style="color:#32CD32;"><b>password</b></span> that belongs to its owner.<br>
        - Wrong credentials will show a <span style="color:#FF0000;"><b>ACCESS DENIED</b></span> popup.<br>
        - Opening and reading files is allowed for all students.
        </p>
        <h3 style="color:#1E3F66;">Thank You!</h3>
        <p style="font-size:14pt; color:#333333;">
        You are now ready to start monitoring file access securely.<br>
        Press the arrow below to proceed to the application.
        </p>
        """)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(instructions)
        layout.addWidget(scroll)

        btn_start = QPushButton("Let's Start ➡")
        btn_start.setFont(QFont("Comic Sans MS", 18, QFont.Weight.Bold))
        btn_start.setStyleSheet("background-color: #1E90FF; color: white; border-radius: 10px; padding: 10px 20px;")
        btn_start.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_start.clicked.connect(lambda: self.proceed.emit())
        layout.addWidget(btn_start, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

# -----------------------------
# DASHBOARD SCREEN
# -----------------------------
class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chowkidaar - Real Time File Access Monitor")
        self.setGeometry(200, 200, 900, 650)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#B0E0E6"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.files_path = "C:\\file_monitor_project\\students"
        self.access_log = {}
        self.logs = []

        main_layout = QVBoxLayout()

        # Header layout: Top-right dotted light + Algerian font
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        self.label_dot = QLabel("●")
        self.label_dot.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.label_dot.setStyleSheet("color: red;")
        self.dot_blink_timer = QTimer()
        self.dot_blink_timer.timeout.connect(self.blink_dot)
        self.dot_blink_timer.start(500)
        header_layout.addWidget(self.label_dot)
        app_label = QLabel("Chowkidaar")
        app_label.setFont(QFont("Algerian", 36, QFont.Weight.Bold))
        app_label.setStyleSheet("color: #1E3F66;")
        header_layout.addWidget(app_label)
        main_layout.addLayout(header_layout)

        # System Calls buttons
        syscalls_layout = QHBoxLayout()
        self.btn_create = QPushButton("CreateFile()")
        self.btn_create.setStyleSheet("background-color:#90EE90; font-weight:bold; font-size:17pt; padding:10px; border-radius:10px;")
        self.btn_read = QPushButton("ReadFile()")
        self.btn_read.setStyleSheet("background-color:#ADD8E6; font-weight:bold; font-size:17pt; padding:10px; border-radius:10px;")
        self.btn_write = QPushButton("WriteFile()")
        self.btn_write.setStyleSheet("background-color:#FFB6C1; font-weight:bold; font-size:17pt; padding:10px; border-radius:10px;")
        self.btn_close = QPushButton("CloseHandle()")
        self.btn_close.setStyleSheet("background-color:#FFFF99; font-weight:bold; font-size:17pt; padding:10px; border-radius:10px;")
        for btn in [self.btn_create, self.btn_read, self.btn_write, self.btn_close]:
            syscalls_layout.addWidget(btn)
        main_layout.addLayout(syscalls_layout)

        # Scrollable area for file stats with progress bars
        self.stats_scroll = QScrollArea()
        self.stats_widget = QWidget()
        self.stats_layout = QVBoxLayout()
        self.stats_widget.setLayout(self.stats_layout)
        self.stats_scroll.setWidget(self.stats_widget)
        self.stats_scroll.setWidgetResizable(True)
        main_layout.addWidget(self.stats_scroll, stretch=2)

        # Live operation log panel
        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        self.log_panel.setFont(QFont("Consolas", 12))
        self.log_panel.setMaximumHeight(130)
        self.log_panel.setStyleSheet("background:#F8F8FF; border:2px solid #707070;")
        main_layout.addWidget(self.log_panel)

        self.setLayout(main_layout)
        self.load_files()

        # Connect buttons to actions
        self.btn_create.clicked.connect(lambda: self.perform_action("OPEN"))
        self.btn_read.clicked.connect(lambda: self.perform_action("READ"))
        self.btn_write.clicked.connect(lambda: self.perform_action("WRITE"))
        self.btn_close.clicked.connect(lambda: self.perform_action("CLOSE"))

    def blink_dot(self):
        self.label_dot.setStyleSheet("color: red;" if self.label_dot.styleSheet() == "color: #FFFFFF;" else "color: #FFFFFF;")

    def load_files(self):
        self.filenames = []
        self.access_log.clear()
        if os.path.exists(self.files_path):
            for fname in os.listdir(self.files_path):
                if fname.endswith(".txt"):
                    self.filenames.append(fname)
                    self.access_log[fname] = {"OPEN":0,"READ":0,"WRITE":0,"CLOSE":0}
        self.update_stats()

    def perform_action(self, action):
        fname, _ = QFileDialog.getOpenFileName(self, f"Select file for {action}", self.files_path, "Text Files (*.txt)")
        if not fname:
            return
        fname = os.path.basename(fname)
        uname, ok = QInputDialog.getText(self, "Username", "Enter your username:")
        if not ok or not uname:
            return
        owner, password = FILE_PASSWORDS.get(fname, (None, None))
        if action == "WRITE" and uname != owner:
            pwd, ok = QInputDialog.getText(self, "Password", f"Enter password for {fname}:")
            if not ok or pwd != password:
                QMessageBox.critical(self, "Access Denied", "ACCESS DENIED!")
                self.access_log[fname][action] += 1
                self.add_log(uname, action, fname, "denied")
                self.update_stats()
                return
        self.access_log[fname][action] += 1
        QMessageBox.information(self, "Success", f"{action} on {fname} by {uname} successful")
        self.add_log(uname, action, fname, "success")
        self.update_stats()

    def add_log(self, uname, action, fname, result):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        logline = f"{timestamp}\t{uname}\t{action}\t{fname}\t{result}"
        self.logs.append(logline)
        self.log_panel.setText('\n'.join(self.logs[-10:]))

    def update_stats(self):
        for i in reversed(range(self.stats_layout.count())):
            widget = self.stats_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        maxval = max([max(log.values()) for log in self.access_log.values()] or [1])
        for fname in self.filenames:
            entry = self.access_log[fname]
            frame = QFrame()
            framelayout = QVBoxLayout()
            frame.setLayout(framelayout)

            file_label = QLabel(f"<b>{fname}</b>")
            file_label.setFont(QFont("Consolas", 14))
            framelayout.addWidget(file_label)

            for act, color in zip(["OPEN","READ","WRITE","CLOSE"],["#32CD32","#00BFFF","#FF00FF","#FFD700"]):
                hbox = QHBoxLayout()
                act_label = QLabel(f'<span style="color:{color};font-weight:bold;">{act}:</span>')
                act_label.setFont(QFont("Consolas", 12))
                act_label.setTextFormat(Qt.TextFormat.RichText)
                bar = QProgressBar()
                bar.setMinimum(0)
                bar.setMaximum(maxval)
                bar.setValue(entry[act])
                bar.setStyleSheet(f"QProgressBar::chunk {{ background: {color}; }}")
                bar.setFormat(f"{entry[act]}")
                bar.setFixedWidth(200)
                hbox.addWidget(act_label)
                hbox.addWidget(bar)
                hbox.addStretch()
                framelayout.addLayout(hbox)

            self.stats_layout.addWidget(frame)
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            self.stats_layout.addWidget(line)

# -----------------------------
# MAIN APP
# -----------------------------
class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.splash = AnimatedSplash()
        self.instruction = InstructionScreen()
        self.dashboard = DashboardScreen()

        self.addWidget(self.splash)
        self.addWidget(self.instruction)
        self.addWidget(self.dashboard)

        self.splash.proceed.connect(lambda: self.setCurrentWidget(self.instruction))
        self.instruction.proceed.connect(lambda: self.setCurrentWidget(self.dashboard))

        self.setCurrentWidget(self.splash)
        self.setWindowTitle("Chowkidaar - File Access Monitor")
        self.setGeometry(200, 200, 900, 650)

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
