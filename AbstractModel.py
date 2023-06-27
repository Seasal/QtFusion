# QtFusion, AGPL-3.0 license
from abc import ABC, abstractmethod


# The Detector class is an abstract base class, representing a generic detector in an object detection scenario.
# It defines a set of methods that any specific detector should implement: loading a model, preprocessing an image,
# making predictions and postprocessing the predictions. It provides a standard interface for different types of
# detectors, allowing them to be used interchangeably in higher-level code. The specific implementation of these methods
# will depend on the characteristics of the specific detector, such as the type of model it uses, and is left to the
# subclasses that inherit from this class.

class Detector(ABC):
    def __init__(self, model_path, device='cpu', imgsz=640):
        """
        Initialize a Detector instance.

        :param model_path: The file path of the model.
        :param device: The device for inference, e.g., 'cpu' or 'cuda'.
        :param imgsz: The size of the input image.
        """
        self.model_path = model_path  # Assigns the file path of the model to an instance variable
        self.device = device  # Assigns the device for inference to an instance variable
        self.imgsz = imgsz  # Assigns the size of the input image to an instance variable

    @abstractmethod
    def load_model(self, model_path):
        """
        Load model.

        This method is implemented by subclasses, as different models may have different loading methods.

        :return: The loaded model.
        """
        pass

    @abstractmethod
    def preprocess(self, img):
        """
        Image preprocessing.

        This method is implemented by subclasses, as different models may require different preprocessing.

        :param img: The original input image.
        :return: The preprocessed image.
        """
        pass

    @abstractmethod
    def predict(self, img):
        """
        Make a prediction on the input image.

        This method is implemented by subclasses, as different models may have different prediction methods.

        :param img: The preprocessed input image.
        :return: The prediction result of the model.
        """
        pass

    @abstractmethod
    def postprocess(self, prediction):
        """
        Postprocess the prediction result.

        This method is implemented by subclasses, as different models may require different postprocessing.

        :param prediction: The prediction result of the model.
        :return: The postprocessed result, typically including bounding boxes, categories, and confidence scores.
        """
        pass
