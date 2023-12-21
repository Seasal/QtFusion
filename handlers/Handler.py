# QtFusion, AGPL-3.0 license
"""
This package provides classes for handling media feeds and image files, facilitating the processing and analysis of
video streams and images. It includes classes for managing video feeds from cameras or video files and for processing
individual image files. The package leverages the capabilities of OpenCV and PySide6 to handle media data efficiently
and interactively.

Classes:
- MediaHandler: Handles media feeds, such as video files or live camera streams, providing functionalities like
  starting/stopping the feed, frame processing, and emitting signals for various media events.
- ImageHandler: Manages and processes image files, emitting signals to communicate the progress and results of the
  image processing tasks.
"""
import imghdr
import os
import platform
import cv2
from IMcore.IMprocessor import IMediaSignals, ImageSignals
from ..utils.ImageUtils import cv_imread


class MediaHandler(IMediaSignals):
    """
    The MediaHandler class is responsible for handling media feeds, such as video files or live camera streams.
    It inherits from IMediaSignals and thus has access to a range of signals for different media states and events.
    The class supports frame processing, where each frame captured from the media can be processed using
    user-defined functions.
    """

    def __init__(self, device=0, fps=30, parent=None):
        """
        Initializes the MediaHandler object with the same parameters as the IMediaSignals class.

        :param device: The camera device number or the path to a video file. Default is 0, which usually refers to the
                       primary camera.
        :param fps: Frames per second for the media playback. Default is 30.
        :param parent: The parent QObject. Default is None.
        """
        super().__init__(device, fps, parent)

        # Create a VideoCapture object in OpenCV to capture frames from the video feed.
        self.cap = cv2.VideoCapture()
        self.timer_media.timeout.connect(self._grabFrame)  # Connect the signal to the frame grabbing function.

    def addFrameProcessor(self, func):
        """
        Adds a frame processing function to the list. This function will be applied to each frame of the media.

        :param func: A function that takes an image as input and returns a processed image.
        """
        super().addFrameProcessor(func)

    def removeFrameProcessor(self, func):
        """
        Removes a frame processing function from the list.

        :param func: The function to remove from the frame processing list.
        """
        super().removeFrameProcessor(func)

    def getMediaInfo(self):
        """
        Returns information about the current media feed, such as resolution, fps, and total frames.

        :return: A dictionary containing media information, or a string indicating that no media is open.
        """
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
        """
        Sets the frames per second for the media feed. Adjusts the timer interval accordingly.

        :param fps: The new frame rate to set.
        """
        self.fps = fps
        if self.timer_media.isActive():
            self.timer_media.start(1000 // self.fps)  # Set the timer interval based on the new fps value.

    def isActive(self):
        """
        Checks if the media feed is currently active (playing).

        :return: True if the media feed is active, False otherwise.
        """
        return super().isActive()

    def startMedia(self):
        """
        Starts the media feed. Opens the media source and begins reading frames. Emits signals on status changes.
        """

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
        """
        Stops the media feed. Releases the media source and stops reading frames. Emits a signal indicating closure.
        """

        self.timer_media.stop()  # Stop the timer.
        if self.cap:
            self.cap.release()  # Release the VideoCapture object in OpenCV.
        self.mediaClosed.emit()  # Emit a signal that the media feed is closed.

    def setDevice(self, device):
        """
        Sets the media source device.

        :param device: The new camera device index or video file path to set.
        """
        super().setDevice(device)

    def _grabFrame(self):
        """
        Internal method called by the timer to grab and process frames from the media feed.
        Emits a signal with the processed frame.
        """

        flag, image = self.cap.read()  # Read a frame from the media feed.
        if flag:
            for func in self.frame_processors:  # Apply all frame processing functions to the frame.
                image = func(image)
            self.frameReady.emit(image)  # Emit a signal that the frame is ready.
        else:
            self.timer_media.stop()  # If a frame can't be read, stop the timer.


class ImageHandler(ImageSignals):
    """
    ImageHandler is responsible for managing and processing image files. It provides functionalities to process images
    individually or in batches if provided with a directory path. The class supports custom image processing
    functionalities, where each image can be processed using user-defined functions. Signals are emitted to indicate
    the progress and results of the image processing tasks.
    """

    def __init__(self, parent=None):
        """
        Constructs an ImageHandler with an optional parent.
        :param parent: The parent QObject. Default is None.
        """
        super().__init__(parent)

    def addFrameProcessor(self, func):
        """
        Adds a function to the list of image processors. Each processor is applied sequentially to the images.

        :param func: A callable function that takes an image as input and returns the processed image.
        """
        super().addFrameProcessor(func)

    def removeFrameProcessor(self, func):
        """
        Removes a function from the list of processors that are applied to each image.

        :param func: The function to be removed from the processing list.
        """
        super().removeFrameProcessor(func)

    def setPath(self, path):
        """
        Sets the path of the image or directory to be processed.

        :param path: The file or directory path to the image(s) to be processed.
        """
        super().setPath(path)

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
        Stops the ongoing image processing tasks. Emits an 'imageClosed' signal after processing is stopped.
        """
        super().stopProcess()

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
        return super().isActive()

    def getFileName(self):
        """
        Gets the name of the current file being processed.

        :return: The name of the current file.
        """
        return super().getFileName()
