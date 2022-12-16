import os
import pytube
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()

        # Create a line edit for entering the YouTube URL
        self.url_input = QLineEdit()

        # Create a button for starting the download
        self.download_button = QPushButton("Download")

        # Create a list widget to hold the download progress
        self.progress_list = QListWidget()

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter the YouTube URL:"))
        layout.addWidget(self.url_input)
        layout.addWidget(self.download_button)
        layout.addWidget(QLabel("Download progress:"))
        layout.addWidget(self.progress_list)
        self.setLayout(layout)

        # Connect the download button to the download function
        self.download_button.clicked.connect(self.download)

    def download(self):
        """Download the video at the specified URL"""
        # Get the URL from the input
        url = self.url_input.text()

        # Create a YouTube object using the URL
        yt = pytube.YouTube(url)

        # Get the video with the highest resolution
        video = yt.streams.filter(progressive=True).order_by('resolution').desc().first()

        # Set the download progress callback
        video.register_on_progress_callback(self.update_progress)

        # Get the file name
        file_name = yt.title + "." + video.subtype

        # Download the video
        video.download(os.getcwd(), file_name)

        # Add a message to the progress list
        self.progress_list.addItem("Download complete: " + file_name)

    def update_progress(self, stream, chunk, file_handle, bytes_remaining):
        """Update the progress list with the download progress"""
        # Calculate the download progress
        progress = (stream.filesize - bytes_remaining) / stream.filesize * 100

        # Update the progress list
        self.progress_list.addItem("{:.2f}% downloaded".format(progress))

if __name__ == "__main__":
    app = QApplication([])
    downloader = YouTubeDownloader()
    downloader.show()
    app.exec_()
