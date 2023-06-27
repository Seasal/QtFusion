# QtFusion, AGPL-3.0 license
import random
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageQt

from . import fontC, fontB


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
    Create a horizontal bar chart as an image.

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
    if max(value) == 0:
        value_name = [random.randint(0, 100) for _ in label_name]
        value_name = [value_name[i] / max(value_name) * (height - 50) for i in range(len(value_name))]
    else:
        value_name = [value[i] / max(value) * (height - 50) for i in range(len(value))]

    # Initialize the drawing area
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    num = len(label_name)
    per_width = (width - margin * num) / num
    x1, y1, x2, y2 = 10, height - 25, per_width + 10, height - value_name[0]
    for i in range(num):
        # Draw each bar
        t_size = draw.textsize(label_name[i], fontB)
        y2 = height - value_name[i] - 25
        color = tuple(colors[i])
        rgba = (color[0], color[1], color[2], int(256 * alpha))
        draw.rectangle([(x1, y1), (x2, y2)], fill=rgba, outline=color, width=2)

        # Write the label for the bar
        bias = (per_width - t_size[0]) / 2
        draw.text((x1 + bias, y1 + 5), label_name[i], fill=color_text, font=fontB)

        # Write the value on the bar
        t_size = draw.textsize(str(int(value[i])), fontB)
        bias_num = (per_width - t_size[0]) / 2
        draw.text((x1 + bias_num, y2 - t_size[1] - 2), str(int(value[i])), fill=color_text, font=fontB)
        x1 += margin + per_width
        x2 = per_width + x1

    # Convert the PIL Image to a QPixmap
    pixmap = ImageQt.toqpixmap(img)
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
    if max(value) == 0:
        value_name = [random.randint(0, 100) for _ in label_name]
        value_name = [value_name[i] / max(value_name) * (width - 50) for i in range(len(value_name))]
    else:
        value_name = [value[i] / max(value) * (width - 50) for i in range(len(value))]

    # Initialize the drawing area
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    num = len(label_name)
    per_height = (height - margin * num - 10) / num
    x1, y1, x2, y2 = 10, 10, 10 + value_name[0], per_height + 10
    for i in range(num):
        # Draw each bar
        t_size = draw.textsize(label_name[i], fontB)
        x2 = value_name[i] + 10
        color = tuple(colors[i])
        rgba = (color[0], color[1], color[2], int(256 * alpha))
        draw.rectangle([(x1, y1), (x2, y2)], fill=rgba, outline=color, width=2)

        # Write the label for the bar
        bias = (per_height - t_size[1]) / 2
        draw.text((x1, y1 + bias), label_name[i], fill=color_text, font=fontB)

        # Write the value on the bar
        t_size_2 = draw.textsize(str(int(value[i])), fontB)
        bias_num = (per_height - t_size_2[1]) / 2
        if t_size[0] + 5 < x2:
            draw.text((x2 + 5, y1 + bias_num), str(int(value[i])), fill=color_text, font=fontB)
        else:
            draw.text((x1 + t_size[0] + 5, y1 + bias_num), str(int(value[i])), fill=color_text, font=fontB)
        y1 += margin + per_height
        y2 = per_height + y1

    # Convert the PIL Image to a QPixmap
    pixmap = ImageQt.toqpixmap(img)
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
    if max(value) == 0:
        value_name = [random.randint(0, 100) for _ in label_name]
        value_name = [value_name[i] / max(value_name) * (width - 90) for i in range(len(value_name))]
    else:
        value_name = [value[i] / max(value) * (width - 90) for i in range(len(value))]

    # Creating a new image with transparent background
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    num = len(label_name)
    per_height = (height - margin * num - 10) / num
    x1, y1, x2, y2 = 10, 10, 10 + value_name[0], per_height + 10
    for i in range(num):
        t_size = draw.textsize(label_name[i], fontB)
        x2 = value_name[i] + 10
        color = tuple(colors[i])
        rgba = (color[0], color[1], color[2], int(256 * alpha))
        # Drawing the bar
        draw.rectangle([(x1, y1), (x2, y2)], fill=rgba, outline=color, width=2)

        # Drawing the bar label
        bias = (per_height - t_size[1]) / 2
        draw.text((x1, y1 + bias), label_name[i], fill=color_text, font=fontB)

        # Drawing the value label
        str_value = '%.2f%%' % value[i]
        t_size_2 = draw.textsize(str_value, fontB)
        bias_num = (per_height - t_size_2[1]) / 2
        if t_size[0] + 5 < x2:
            draw.text((x2 + 5, y1 + bias_num), str_value, fill=color_text, font=fontB)
        else:
            draw.text((x1 + t_size[0] + 5, y1 + bias_num), str_value, fill=color_text, font=fontB)
        y1 += margin + per_height
        y2 = per_height + y1

    # Convert image to QPixmap for display in a PyQt application
    pixmap = ImageQt.toqpixmap(img)
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
    draw = ImageDraw.Draw(img, "RGBA")

    tl = line_thickness or round(0.002 * (img.width + img.height) / 2) + 1  # Default line thickness
    if color is not None:
        color = tuple(color)
    else:
        color = tuple([random.randint(0, 255) for _ in range(3)])  # Random color if not provided
    c1, c2 = (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3]))

    # Calculate rectangle dimensions
    w, h = (rect[2] - rect[0], rect[3] - rect[1])
    len_edge = int(w / 10), int(h / 10)

    rgba = (color[0], color[1], color[2], int(256 * alpha))
    # Draw the rectangle
    draw.rectangle([c1, c2], fill=rgba, outline=color, width=0)

    # Draw rectangle corners
    draw.line([c1, (c1[0], c1[1] + len_edge[1])], fill=color, width=tl)
    draw.line([c1, (c1[0] + len_edge[0], c1[1])], fill=color, width=tl)
    draw.line([(c1[0] + w, c1[1]), (c2[0] - len_edge[0], c1[1])], fill=color, width=tl)
    draw.line([(c1[0] + w, c1[1]), (c2[0], c1[1] + len_edge[1])], fill=color, width=tl)
    draw.line([c2, (c2[0], c2[1] - len_edge[1])], fill=color, width=tl)
    draw.line([c2, (c2[0] - len_edge[0], c2[1])], fill=color, width=tl)
    draw.line([(c1[0], c2[1]), (c1[0], c2[1] - len_edge[1])], fill=color, width=tl)
    draw.line([(c1[0], c2[1]), (c1[0] + len_edge[0], c2[1])], fill=color, width=tl)

    # Add text if provided
    label_img = image.copy()
    if addText and fontC:
        t_size = draw.textsize(addText, fontC)
        c1_text = c1[0], c1[1] - t_size[1] - 3
        c2_text = c1[0] + t_size[0] + 3, c1[1] - 3
        # Make sure the text box doesn't go outside the image
        if c1_text[1] < 0:
            c1_text = c1_text[0], 0
        if c2_text[1] < 0:
            c2_text = c2_text[0], 0

        draw.rectangle([c1_text, c2_text], fill=color, outline="#FF0000", width=0)
        draw.text((c1[0], c1_text[1]), addText, fill="#FFFFFF", font=fontC)
        label_img = np.array(img)
    return label_img


def drawRectBox(image, rect, color=None, alpha=0.25, addText=None, line_thickness=None):
    """
    Draws a rectangular bounding box on an image.

    :param image: A numpy array representing the image to draw on.
    :param rect: A list/tuple of 4 integers specifying the bounding box coordinates (x1, y1, x2, y2).
    :param color: Optional; A list/tuple of 3 integers specifying the color of the box (R, G, B). If None, a random color will be used.
    :param alpha: Optional; A float value representing the alpha (transparency) of the box. Default is 0.25.
    :param addText: Optional; A string of text to add to the box. If None, no text is added.
    :param line_thickness: Optional; An integer specifying the thickness of the lines of the box. If None, a thickness is calculated based on the dimensions of the image.
    :return: A numpy array representing the image with the drawn box and text.
    """
    # Convert numpy array image to PIL Image object
    img = Image.fromarray(image)
    # Create a drawing context on the image
    draw = ImageDraw.Draw(img, "RGBA")

    # Calculate line thickness if not provided
    tl = line_thickness or round(0.002 * (img.width + img.height) / 2) + 1

    # If a specific color is not provided, generate a random one
    if color is not None:
        color = tuple(color)
    else:
        color = tuple([random.randint(0, 255) for _ in range(3)])

    # Get the corners of the rectangle
    c1, c2 = (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3]))

    # Prepare the color with alpha for the rectangle fill
    rgba = (color[0], color[1], color[2], int(255 * alpha))

    # Draw the rectangle on the image
    draw.rectangle([c1, c2], fill=rgba, outline=color, width=tl)
    label_img = image.copy()  # Create a copy of the original image for the text

    # If text is provided and a font object exists, add text on the box
    if addText and fontC:
        # Get the size of the text box
        t_size = draw.textsize(addText, fontC)
        # Position of the text box
        c1_text = c1[0], c1[1] - t_size[1] - 3
        c2_text = c1[0] + t_size[0] + 3, c1[1] - 3
        # Make sure the text box doesn't go outside the image
        if c1_text[1] < 0:
            c1_text = c1_text[0], 0
        if c2_text[1] < 0:
            c2_text = c2_text[0], 0

        # Draw the rectangle for the text
        draw.rectangle([c1_text, c2_text], fill=color, outline="#FF0000", width=0)
        # Draw the text
        draw.text((c1[0], c1_text[1]), addText, fill="#FFFFFF", font=fontC)
        # Convert the final image back to a numpy array
        label_img = np.array(img)

    # Return the final image
    return label_img
