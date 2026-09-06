import sys
import os

# 1. CRITICAL: Mac graphics and backend sandbox settings
# os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox --use-gl=angle --use-angle=metal"

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
import plotly.express as px

# 2. Build the map layout (Using Mapbox since it doesn't rely on background JSON vectors)
fig = px.scatter_mapbox(
    lat=[37.7749, 34.0522, 40.7128],
    lon=[-122.4194, -118.2437, -74.0060],
    text=["San Francisco", "Los Angeles", "New York"],
    title="Simple Map with Points",
    zoom=3, 
    center=dict(lat=37.0902, lon=-95.7129)
)

fig.add_scattermapbox(
    lat=[37.7749, 34.0522, 40.7128],
    lon=[-122.4194, -118.2437, -74.0060],
    mode='lines',
    line=dict(width=2, color='blue'),
    name='Path'
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

# 3. Save to a real file on disk (Using 'inline' is safe here because it reads from disk layout)
output_path = os.path.abspath("test_plotly.html")
fig.write_html(output_path, include_plotlyjs="inline")


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Map Fix")
        self.resize(1000, 600)

        # Build window structure
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        # 4. CRITICAL: Unblock Local File Permissions on the Profile
        profile = QWebEngineProfile.defaultProfile()
        settings = profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)

        # 5. Load utilizing a clean File URL instead of passing a giant data string
        file_url = QUrl.fromLocalFile(output_path)
        self.browser.load(file_url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec())
