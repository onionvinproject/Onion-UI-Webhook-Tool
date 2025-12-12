from PySide6.QtWidgets import (QWidget, QLineEdit, QPushButton, QTextEdit, 
                            QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, 
                            QGroupBox, QScrollArea, QFrame, QApplication,
                            QStackedWidget)
from PySide6.QtCore import Qt, QSize, QDateTime
from PySide6.QtGui import QColor, QFont, QPixmap, QIcon
import requests
import threading
import sys
import random
import json
import ctypes
import io
import tempfile
import os
import urllib.request
import time

class ProxyList(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border: 2px solid #2d2d2d;
                border-radius: 15px;
            }
        """)
        self.proxies = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        self.proxy_toggle = QPushButton("Enable Proxies")
        self.proxy_toggle.setCheckable(True)
        self.proxy_toggle.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                border: none;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-family: 'Triplex Sans', sans-serif;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:checked {
                background-color: #f5f5f5;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:checked:hover {
                background-color: #ff1f1f;
            }
        """)
        self.proxy_toggle.clicked.connect(self.toggle_proxies)
        layout.addWidget(self.proxy_toggle)

        self.proxy_list = QTextEdit()
        self.proxy_list.setPlaceholderText("Proxies here (one per line)\nhttp://user:pass@host:port")
        self.proxy_list.setEnabled(False)
        self.proxy_list.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-family: 'Triplex Sans', sans-serif;
                font-size: 12px;
            }
            QTextEdit:disabled {
                background-color: #1a1a1a;
                color: #666666;
            }
        """)
        self.proxy_list.textChanged.connect(self.update_proxies)
        layout.addWidget(self.proxy_list)

        self.setLayout(layout)

    def toggle_proxies(self):
        enabled = self.proxy_toggle.isChecked()
        self.proxy_list.setEnabled(enabled)
        self.proxy_toggle.setText("Disable Proxies" if enabled else "Enable Proxies")

    def update_proxies(self):
        self.proxies = [line.strip() for line in self.proxy_list.toPlainText().split('\n') if line.strip()]

    def get_random_proxy(self):
        return random.choice(self.proxies) if self.proxies else None

    def get_proxies(self):
        return self.proxies

class CommandLog(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border: 2px solid #2d2d2d;
                border-radius: 15px;
            }
        """)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def add_log(self, message, type="info"):
        color = {
            "info": "#ffffff",
            "success": "#00cc66",
            "error": "#ff3333",
            "warning": "#ffcc00"
        }.get(type, "#ffffff")
        
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        formatted_message = f'<span style="color: #888888">[{timestamp}]</span> <span style="color: {color}">{message}</span>'
        self.log_area.append(formatted_message)
        self.log_area.verticalScrollBar().setValue(self.log_area.verticalScrollBar().maximum())

class NebulaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("onion.ico"))
        self.setWindowTitle("Onion | Webhook Spammer | .gg/onionvin")
        self.setGeometry(100, 100, 1000, 500)
        self._stop_event = threading.Event()
        self._spam_thread = None
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                font-family: 'Triplex Sans', sans-serif;
            }
        """)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout() 
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        self.webhook_input = QLineEdit()
        self.webhook_input.setPlaceholderText("Webhook URL")
        self.webhook_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 15px;
                padding: 12px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #ff3333;
            }
        """)
        left_layout.addWidget(self.webhook_input)

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Message")
        self.message_input.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 15px;
                padding: 12px;
                color: white;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 2px solid #ff3333;
            }
        """)
        left_layout.addWidget(self.message_input)

        options_layout = QHBoxLayout()
        
        self.tts_check = QCheckBox("TTS")
        self.tts_check.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 13px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 5px;
                border: 2px solid #3d3d3d;
            }
            QCheckBox::indicator:checked {
                background-color: #f5f5f5;
                border: 2px solid #dcdcdc;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #eaeaea;
            }
        """)
        options_layout.addWidget(self.tts_check)

        self.name_check = QCheckBox("Custom Name")
        self.name_check.setStyleSheet(self.tts_check.styleSheet())
        options_layout.addWidget(self.name_check)

        self.avatar_check = QCheckBox("Custom Avatar")
        self.avatar_check.setStyleSheet(self.tts_check.styleSheet())
        options_layout.addWidget(self.avatar_check)

        left_layout.addLayout(options_layout)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Webhook Name")
        self.name_input.setEnabled(False)
        self.name_input.setStyleSheet(self.webhook_input.styleSheet())
        self.name_check.stateChanged.connect(lambda: self.name_input.setEnabled(self.name_check.isChecked()))
        left_layout.addWidget(self.name_input)

        self.avatar_input = QLineEdit()
        self.avatar_input.setPlaceholderText("Avatar URL")
        self.avatar_input.setEnabled(False)
        self.avatar_input.setStyleSheet(self.webhook_input.styleSheet())
        self.avatar_check.stateChanged.connect(lambda: self.avatar_input.setEnabled(self.avatar_check.isChecked()))
        left_layout.addWidget(self.avatar_input)

        self.send_button = QPushButton("Spam")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #00cc66;
                border: none;
                border-radius: 15px;
                padding: 15px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #eaeaea;
            }
            QPushButton:pressed {
                background-color: #dcdcdc;
            }
        """)
        self.send_button.clicked.connect(self.toggle_webhook)
        left_layout.addWidget(self.send_button)

        main_layout.addLayout(left_layout)
        self.proxy_section = ProxyList()
        main_layout.addWidget(self.proxy_section)
        self.log_section = CommandLog()
        main_layout.addWidget(self.log_section)

        self.setLayout(main_layout)

    def spam_webhook(self):
        session = requests.Session()
        proxies = self.proxy_section.get_proxies() if self.proxy_section.proxy_toggle.isChecked() else []
        proxy_index = 0

        while not self._stop_event.is_set():
            try:
                current_proxy = proxies[proxy_index] if proxies else None
                if current_proxy:
                    session.proxies = {
                        'http': f'http://{current_proxy}',
                        'https': f'http://{current_proxy}'
                    }
                    proxy_index = (proxy_index + 1) % len(proxies)

                payload = {
                    "content": self.message_input.toPlainText(),
                    "tts": self.tts_check.isChecked()
                }

                if self.name_check.isChecked() and self.name_input.text().strip():
                    payload["username"] = self.name_input.text().strip()
                if self.avatar_check.isChecked() and self.avatar_input.text().strip():
                    payload["avatar_url"] = self.avatar_input.text().strip()

                response = session.post(
                    self.webhook_input.text(),
                    json=payload,
                    timeout=10
                )

                if response.status_code == 204:
                    self.log_section.add_log("✅ Sent", "success")
                elif response.status_code == 429:
                    self.log_section.add_log("🟨 Ratelimit", "warning")
                    retry_after = response.json().get('retry_after', 5)
                    if not self._stop_event.wait(timeout=retry_after/1000.0):
                        continue
                elif response.status_code == 400:
                    self.log_section.add_log("❌ Invalid webhook", "error")
                else:
                    self.log_section.add_log(f"❌ Error {response.status_code}", "error")
            except Exception as e:
                self.log_section.add_log(f"❌ Error: {str(e)}", "error")
            
            if not self._stop_event.is_set():
                self._stop_event.wait(timeout=0.1)

    def start_spam(self):
        if not self._spam_thread or not self._spam_thread.is_alive():
            self._stop_event.clear()
            self.send_button.setText("Stop")
            self.send_button.setStyleSheet("""
                QPushButton {
                    background-color: #f5f5f5;
                    border: none;
                    border-radius: 15px;
                    padding: 15px;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #ff1f1f;
                }
                QPushButton:pressed {
                    background-color: #9c0303;
                }
            """)
            self._spam_thread = threading.Thread(target=self.spam_webhook, daemon=True)
            self._spam_thread.start()
            self.log_section.add_log("Started webhook spammer", "success")

    def stop_spam(self):
        if self._spam_thread and self._spam_thread.is_alive():
            self._stop_event.set()
            self._spam_thread.join(timeout=2)
            self.send_button.setText("Start")
            self.send_button.setStyleSheet("""
                QPushButton {
                    background-color: #00cc66;
                    border: none;
                    border-radius: 15px;
                    padding: 15px;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #00b359;
                }
                QPushButton:pressed {
                    background-color: #009933;
                }
            """)
            self.log_section.add_log("Stopped webhook spammer", "info")

    def toggle_webhook(self):
        if not self._spam_thread or not self._spam_thread.is_alive():
            self.start_spam()
        else:
            self.stop_spam()

if sys.platform == 'win32':
    ctypes.windll.user32.ShowWindow(
        ctypes.windll.kernel32.GetConsoleWindow(), 0)

app = QApplication(sys.argv)
window = NebulaWindow()
window.show()
sys.exit(app.exec())
