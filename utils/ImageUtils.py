# QtFusion, AGPL-3.0 license
import random
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageQt
from IMcore.IMplots import imHBar, imVBar, imRectBox, imVBarPer, imRectEdge
from .. import fontC, fontB


def get_cls_color(cls_name):
    """
    Returns a list of color codes based on the class name.

    :param cls_name: Class name string.
    :return: List of RGB color codes.
    """
    pre_colors = [[132, 56, 255], [82, 0, 133], [203, 56, 255], [255, 149, 200], [255, 55, 199],
                  [72, 249, 10], [146, 204, 23], [61, 219, 134], [26, 147, 52], [0, 212, 187],
                  [255, 56, 56], [255, 157, 151], [255, 112, 31], [255, 178, 29], [207, 210, 49],
                  [44, 153, 168], [0, 194, 255], [52, 69, 147], [100, 115, 255], [0, 24, 236]]
    generated_colors = pre_colors if len(cls_name) <= len(pre_colors) \
        else [[random.randint(0, 255) for _ in range(3)] for _ in
              range(len(cls_name))]  # Assign a unique color for each class
    return generated_colors


def horizontal_bar(label_name, value, colors, width, height, color_text='#000000', alpha=0.8, margin=20):
    """
    Creates a horizontal bar chart as an image.

    Args:
        label_name (list): Labels for each bar.
        value (list): Values that each bar represents.
        colors (list): Color for each bar.
        width (int): Width of the output image.
        height (int): Height of the output image.
        color_text (str, optional): Color of the text. Defaults to '#000000'.
        alpha (float, optional): Alpha value of the bar colors for transparency. Defaults to 0.8.
        margin (int, optional): Margin between each bar. Defaults to 20.

    Returns:
        QPixmap: An image of the bar chart.
    """
    # Generate random values for demonstration if the maximum value is 0
    value_name = None
    if max(value) == 0:
        value_name = [random.randint(0, 100) for _ in label_name]

    pixmap = imHBar(label_name, value, colors, width, height, value_name, color_text, alpha, margin, fontB)
    return pixmap


def vertical_bar(label_name, value, colors, width, height, color_text='#000000', alpha=0.7, margin=20):
    """
    Create a vertical bar chart as an image.

    :param label_name: The labels for each bar.
    :param value: The values that each bar represents.
    :param colors: The color of each bar.
    :param width: The width of the output image.
    :param height: The height of the output image.
    :param color_text: The color of text.
    :param alpha: The alpha value of the bars' colors, for transparency.
    :param margin: The margin between each bar.
    :return: The image of the bar chart as a QPixmap.
    """
    # If the max value is 0, generate random values for demonstration.
    value_name = None
    if max(value) == 0:
        value_name = [random.randint(0, 100) for _ in label_name]

    pixmap = imVBar(label_name, value, colors, width, height, value_name, color_text, alpha, margin, fontB)
    return pixmap


def verticalBar(label_name, value, colors, width, height, color_text='#000000', alpha=0.7, margin=20):
    """
    Generate a vertical bar chart as a QPixmap.

    :param label_name: List of bar labels.
    :param value: List of bar values.
    :param colors: List of RGB color tuples for each bar.
    :param width: The width of the generated chart image.
    :param height: The height of the generated chart image.
    :param color_text: The color of text.
    :param alpha: The alpha value (transparency) of the bars.
    :param margin: The margin between bars.
    :return: QPixmap of the generated chart.
    """
    # Handling case where all values are zero
    value_name = None
    if max(value) == 0:
        value_name = [random.randint(0, 100) for _ in label_name]

    pixmap = imVBarPer(label_name, value, colors, width, height, value_name, color_text, alpha, margin, fontB)
    return pixmap


def cv_imread(file_path):
    """
    Read an image file using cv2 in a way that also supports Unicode paths.

    :param file_path: The path to the image file.
    :return: The loaded image as a numpy array.
    """
    # Using cv2.imdecode to support Unicode paths
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)

    # Convert grayscale images to RGB
    if len(cv_img.shape) > 2:
        if cv_img.shape[2] > 3:
            cv_img = cv_img[:, :, :3]
    elif len(cv_img.shape) == 2:
        cv_img = np.stack((cv_img, cv_img, cv_img), axis=2)
    return cv_img


def drawRectEdge(image, rect, color=None, alpha=0.2, addText=None, line_thickness=None):
    """
    Draw a rectangle with annotated edges on an image.

    :param image: The image to draw on, as a numpy array.
    :param rect: The coordinates of the rectangle as (x1, y1, x2, y2).
    :param color: The color of the rectangle as an RGB tuple.
    :param alpha: The alpha value (transparency) of the rectangle.
    :param addText: Text to add to the rectangle.
    :param line_thickness: The thickness of the rectangle's outline.
    :return: The modified image.
    """
    # Convert image to PIL Image for drawing
    img = Image.fromarray(image)
    # Add text if provided
    label_img = image.copy()
    if addText and fontC:
        img = imRectEdge(img, rect, color, alpha, addText, line_thickness, fontC)
        label_img = np.array(img)
    return label_img


def drawRectBox(image, rect, color=None, alpha=0.25, addText=None, line_thickness=None):
    """
    Draws a rectangular bounding box on an image.

    :param image: A numpy array representing the image to draw on.
    :param rect: A list/tuple of 4 integers specifying the bounding box coordinates (x1, y1, x2, y2).
    :param color: Optional; A list/tuple of 3 integers specifying the color of the box (R, G, B). If None, a random
    color will be used.
    :param alpha: Optional; A float value representing the alpha (transparency) of the box. Default is 0.25.
    :param addText: Optional; A string of text to add to the box. If None, no text is added.
    :param line_thickness: Optional; An integer specifying the thickness of the lines of the box. If None, a thickness
    is calculated based on the dimensions of the image.
    :return: A numpy array representing the image with the drawn box and text.
    """
    # Convert numpy array image to PIL Image object
    img = Image.fromarray(image)
    label_img = image.copy()
    # If text is provided and a font object exists, add text on the box
    if addText and fontC:
        img = imRectBox(img, rect, color, alpha, addText, line_thickness, fontC)
        # Convert the final image back to a numpy array
        label_img = np.array(img)

    # Return the final image
    return label_img
