import sys
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QLineEdit, QProgressBar
)
from PySide6.QtWebEngineWidgets import QWebEngineView

class MiniBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 QWebEngineView Example")
        self.resize(1024, 768)

        # 1. Create the WebEngine View
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://wikipedia.org"))

        # 2. Create Navigation Controls
        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.refresh_btn = QPushButton("⟳")
        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL and press Enter...")

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumHeight(4)
        self.progress_bar.setTextVisible(False)

        # 3. Layout Setup
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.refresh_btn)
        nav_layout.addWidget(self.url_bar)

        main_layout = QVBoxLayout()
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # 4. Connect Signals and Slots
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.refresh_btn.clicked.connect(self.browser.reload)
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # Update UI based on browser events
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadProgress.connect(self.progress_bar.setValue)
        self.browser.loadFinished.connect(self.handle_load_finished)

    def navigate_to_url(self):
        """Loads the text from the URL bar into the browser."""
        text = self.url_bar.text()
        if not text.startswith(("http://", "https://")):
            text = "https://" + text
        self.browser.setUrl(QUrl(text))

    def update_url_bar(self, url):
        """Updates the text field when a link is clicked inside the website."""
        self.url_bar.setText(url.toString())

    def handle_load_finished(self, success):
        """Hides the progress bar when loading finishes."""
        if success:
            self.progress_bar.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiniBrowser()
    window.show()
    sys.exit(app.exec())
