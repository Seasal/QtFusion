# QtFusion, AGPL-3.0 license
import imghdr
import os
import platform
import cv2
from PySide6.QtCore import QTimer, Signal, QObject

from .ImageUtils import cv_imread


class MediaHandler(QObject):
    """A class used to handle media feeds, such as video files or live streams from a camera."""

    # Signals are declared as class attributes and are emitted in response to changes to the object’s state.
    frameReady = Signal(object)  # Emitted when a new frame is ready.
    mediaOpened = Signal()  # Emitted when the media feed is successfully opened.
    mediaClosed = Signal()  # Emitted when the media feed is closed.
    mediaFailed = Signal(str)  # Emitted when opening the media feed fails, sending the error message as a string.
    stopOtherActivities = Signal()  # Emitted when the media feed starts, indicating other activities should be stopped.

    def __init__(self, device=0, fps=30, parent=None):
        """Constructor for the MediaHandler class."""
        super().__init__(parent)

        # Device could be an integer representing the camera number or a string representing a video file path.
        self.device = device
        self.fps = fps  # The frames per second of the media.
        self.frame_processors = []  # List of frame processing functions.

        # Create a VideoCapture object in OpenCV to capture frames from the video feed.
        self.cap = cv2.VideoCapture()
        self.timer_media = QTimer()  # Timer for capturing frames at regular intervals.
        # Connect the timer's timeout signal to the frame grabbing function.
        self.timer_media.timeout.connect(self._grabFrame)

    def addFrameProcessor(self, func):
        """Add a frame processing function to the list."""
        self.frame_processors.append(func)

    def removeFrameProcessor(self, func):
        """Remove a frame processing function from the list."""
        self.frame_processors.remove(func)

    def getMediaInfo(self):
        """Return information about the media feed, including width, height, fps, and total frame count."""
        info = {}
        if self.cap and self.cap.isOpened():
            info['width'] = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            info['height'] = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            info['fps'] = self.cap.get(cv2.CAP_PROP_FPS)
            info['frames'] = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        else:
            info = "No media device is opened yet"
        return info

    def setFps(self, fps):
        """Set the frames per second of the media feed."""
        self.fps = fps
        if self.timer_media.isActive():
            self.timer_media.start(1000 // self.fps)  # Set the timer interval based on the new fps value.

    def isActive(self):
        """Return True if the media feed is active, False otherwise."""
        return self.timer_media.isActive()

    def startMedia(self):
        """Start the media feed."""
        self.stopOtherActivities.emit()   # Emit a signal to stop other activities.

        # Determine the device type. If it's an integer, it's a camera number. If it's a string, it's a video file path.
        if isinstance(self.device, int):
            if platform.system() == 'Windows':
                flag = self.cap.open(self.device, cv2.CAP_DSHOW)
            else:
                flag = self.cap.open(self.device, cv2.CAP_ANY)
        else:
            flag = self.cap.open(self.device, cv2.CAP_FFMPEG)
        # If the media feed can't be opened, emit a failure signal with an error message.
        if not flag:
            self.mediaFailed.emit('Unable to open device: {}'.format(self.device))
        else:
            # If the media feed is successfully opened, emit a success signal and start the timer.
            self.mediaOpened.emit()
            self.timer_media.start(1000 // self.fps)

    def stopMedia(self):
        """Stop the media feed."""

        self.timer_media.stop()  # Stop the timer.
        if self.cap:
            self.cap.release()  # Release the VideoCapture object in OpenCV.
        self.mediaClosed.emit()  # Emit a signal that the media feed is closed.

    def setDevice(self, device):
        """Set the device number or video file path."""

        self.device = device

    def _grabFrame(self):
        """The slot function for the timer, used to grab frames from the media feed."""

        flag, image = self.cap.read()  # Read a frame from the media feed.
        if flag:
            for func in self.frame_processors:  # Apply all frame processing functions to the frame.
                image = func(image)
            self.frameReady.emit(image)  # Emit a signal that the frame is ready.
        else:
            self.timer_media.stop()  # If a frame can't be read, stop the timer.


class ImageHandler(QObject):
    """
    ImageHandler is a class responsible for managing and processing image files. It emits various signals to communicate
    the progress and results of the image processing tasks.
    """
    frameReady = Signal(object)  # Signal emitted when an image has been processed. It carries the processed image.
    imageOpened = Signal()  # Signal emitted when an image processing task starts.
    imageClosed = Signal()  # Signal emitted when an image processing task ends.

    # Signal emitted when an error occurs during image processing. It carries an error message.
    imageFailed = Signal(str)

    # Signal emitted before starting an image processing task.
    # It can be used to stop other activities that could interfere with the image processing.
    stopOtherActivities = Signal()

    def __init__(self, parent=None):
        """
        Constructs an ImageHandler with an optional parent.
        """
        super().__init__(parent)
        self.path = None  # Path of the image or directory to be processed.
        self.file_name = None  # Name of the current file being processed.
        self.frame_processors = []  # List of functions that will be applied to each image.
        self.processing = False  # Boolean flag indicating whether an image is currently being processed.

    def addFrameProcessor(self, func):
        """
        Adds a function to the list of processors that will be applied to each image.

        :param func: The function to be added.
        """
        self.frame_processors.append(func)

    def removeFrameProcessor(self, func):
        """
        Removes a function from the list of processors that are applied to each image.

        :param func: The function to be removed.
        """
        self.frame_processors.remove(func)

    def setPath(self, path):
        """
        Sets the path of the image or directory to be processed.

        :param path: The path to be set.
        """
        self.path = path

    def startProcess(self):
        """
        Starts the image processing tasks. If the path is a file, a single image will be processed. If the path is a
        directory, all the images in the directory will be processed. Emits the 'stopOtherActivities' signal before
        starting the processing, and the 'imageOpened' signal once the processing starts.
        """
        self.stopOtherActivities.emit()
        if self.path and not self.processing:
            self.processing = True
            self.imageOpened.emit()
            if os.path.isfile(self.path):
                self._processImage(self.path)
            elif os.path.isdir(self.path):
                for filename in os.listdir(self.path):
                    if not self.processing:
                        break
                    file_path = os.path.join(self.path, filename)
                    if os.path.isfile(file_path) and imghdr.what(file_path) is not None:
                        self.file_name = file_path
                        self._processImage(file_path)
            else:
                self.imageFailed.emit('Path does not exist: {}'.format(self.path))
            self.processing = False

    def stopProcess(self):
        """
        Stops the image processing tasks. Emits the 'imageClosed' signal after stopping the processing.
        """
        self.processing = False
        self.imageClosed.emit()

    def _processImage(self, image_path):
        """
        Processes a single image file. Applies all the functions in 'frame_processors' to the image. Emits the
        'frameReady' signal if the image is successfully processed, or the 'imageFailed' signal if an error occurs.

        :param image_path: The path of the image to be processed.
        """
        try:
            image = cv_imread(image_path)
            for func in self.frame_processors:
                image = func(image)
            self.frameReady.emit(image)
        except Exception as e:
            self.imageFailed.emit('Failed to open image at {}: {}'.format(image_path, str(e)))

    def isActive(self):
        """
        Checks if the ImageHandler is currently processing an image.

        :return: True if an image is being processed, False otherwise.
        """
        return self.processing

    def getFileName(self):
        """
        Gets the name of the current file being processed.

        :return: The name of the current file.
        """
        return self.file_name
