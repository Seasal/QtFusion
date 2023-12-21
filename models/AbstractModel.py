# QtFusion, AGPL-3.0 license
from abc import ABC, abstractmethod

"""
The Detector class is an abstract base class, representing a generic detector in an object detection scenario.
It defines a set of methods that any specific detector should implement: loading a model, preprocessing an image,
making predictions, and postprocessing the predictions. This class provides a standard interface for different types of
detectors, allowing them to be used interchangeably in higher-level code. The specific implementation of these methods
will depend on the characteristics of the specific detector, such as the type of model it uses, and is left to the
subclasses that inherit from this class. This abstraction allows for flexibility and extensibility, as new types of 
detectors can be easily integrated by simply implementing these core methods. It ensures consistency in how detectors 
are used, regardless of their internal workings, making it easier to work with a variety of detection models and 
techniques. This approach also facilitates testing and maintenance, as changes to the detection process can be made 
in a centralized manner without affecting client code.
"""


class Detector(ABC):
    def __init__(self, model_path, device='cpu', imgsz=640):
        """
        Initialize a Detector instance.

        This constructor sets up the initial state of the Detector object with the necessary parameters.

        :param model_path: The file path of the model. This path is used to load the model for object detection.
        :param device: The device on which the model will perform inference. Default is 'cpu', but can be set to 'cuda'
                       for inference on an NVIDIA GPU.
        :param imgsz: The size of the input image. The image will be resized to this size before being fed into the model.
        """
        self.model_path = model_path  # The file path to the pre-trained model for detection.
        self.device = device  # The computational device ('cpu' or 'cuda') for model inference.
        self.imgsz = imgsz  # The target size of the input images for the model.

    @abstractmethod
    def load_model(self, model_path):
        """
        Abstract method to load a model.

        This method should be implemented by subclasses to load the model from the given path. The implementation
        of this method will vary depending on the model's framework (like TensorFlow, PyTorch) and format.

        :return: The loaded model ready for inference.
        """
        pass

    @abstractmethod
    def preprocess(self, img):
        """
        Abstract method for image preprocessing.

        This method should be implemented by subclasses to perform necessary preprocessing steps before the image
        is fed into the model for inference. Preprocessing steps may include resizing, normalization, etc.

        :param img: The original input image.
        :return: The preprocessed image suitable for the model.
        """
        pass

    @abstractmethod
    def predict(self, img):
        """
        Abstract method to make a prediction on the input image.

        This method should be implemented by subclasses to feed the preprocessed image into the model and
        obtain the raw prediction output.

        :param img: The preprocessed input image.
        :return: The raw prediction output from the model.
        """
        pass

    @abstractmethod
    def postprocess(self, prediction):
        """
        Abstract method for postprocessing the prediction result.

        This method should be implemented by subclasses to convert the raw prediction output of the model into a
        more interpretable and useful format, such as bounding boxes, classes, and confidence scores.

        :param prediction: The raw prediction result from the model.
        :return: The postprocessed result, which may include bounding boxes, class labels, and confidence scores.
        """
        pass
