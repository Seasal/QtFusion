# QtFusion, AGPL-3.0 license
import cv2
import numpy as np


class HeatmapGenerator:
    """
    Class for generating heatmaps from a specific layer of a model.

    Attributes:
        hook (SaveFeatures): Instance to save output features from a specific model layer.
        heatmap_intensity (float): Transparency of the heatmap.
        original_img_intensity (float): Transparency of the original image.
        color_map (int): OpenCV color map for generating the heatmap.
        norm_alpha (int): Minimum value for normalization.
        norm_beta (int): Maximum value for normalization.
        hist_eq_threshold (int): Threshold for histogram equalization.
    """

    def __init__(self, heatmap_intensity=0.4, color_map=cv2.COLORMAP_JET, hist_eq_threshold=200, norm_range=(0, 255)):
        """
        Initializes the HeatmapGenerator.

        Args:
            heatmap_intensity (float): Transparency of the heatmap.
            color_map (int): OpenCV color map for generating the heatmap.
            hist_eq_threshold (int): Threshold for histogram equalization.
            norm_range (tuple): Minimum and maximum values for normalization.
        """
        self.hook = self.SaveFeatures()
        self.heatmap_intensity = heatmap_intensity
        self.original_img_intensity = 1 - heatmap_intensity
        self.color_map = color_map
        self.norm_alpha, self.norm_beta = norm_range
        self.hist_eq_threshold = hist_eq_threshold

    class SaveFeatures:
        """
        Class for saving output features from a specific layer of a model.

        Attributes:
            features (Tensor or None): Saved feature maps.
        """

        def __init__(self):
            """
            Initializes SaveFeatures.
            """
            self.features = None

        def __call__(self, module, module_in, module_out):
            """
            Called during the forward pass of the model, saves the output features.

            Args:
                module: The current layer.
                module_in: Input to the current layer.
                module_out: Output from the current layer.
            """
            self.features = module_out

    def register_hook(self, reg_layer):
        """
        Registers a forward hook on the specified layer of the model.

        Args:
            reg_layer: The model layer to register the hook on.
        """
        reg_layer.register_forward_hook(self.hook)

    def get_heatmap(self, img):
        """
        Generates a heatmap.

        Args:
            img (ndarray): The original image in BGR format.

        Returns:
            ndarray: The original image superimposed with the heatmap.
        """
        feature_maps = self.hook.features

        if feature_maps is not None and len(feature_maps) > 0:
            # Extract and process the first feature map
            selected_feature_map = feature_maps[0].detach().cpu().numpy() if len(feature_maps) < 2 else (
                feature_maps[1][0].detach().cpu()[0].numpy())

            # Apply histogram equalization and thresholding
            equalized_feature_maps = np.array([cv2.equalizeHist(
                cv2.normalize(fm, None, alpha=self.norm_alpha,
                              beta=self.norm_beta,
                              norm_type=cv2.NORM_MINMAX).astype(np.uint8))
                for fm in selected_feature_map])
            _, equalized_feature_maps = cv2.threshold(equalized_feature_maps, self.hist_eq_threshold, self.norm_beta,
                                                      cv2.THRESH_BINARY)

            # Compute the mean of the equalized feature maps and normalize
            feature_map_mean = equalized_feature_maps.mean(axis=0)
            normalized_feature_map = cv2.normalize(feature_map_mean, None, alpha=self.norm_alpha, beta=self.norm_beta,
                                                   norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

            # Generate and superimpose the heatmap
            heatmap = cv2.applyColorMap(normalized_feature_map, self.color_map)
            heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
            superimposed_img = cv2.addWeighted(img, self.original_img_intensity, heatmap, self.heatmap_intensity, 0)
            return superimposed_img
        else:
            if feature_maps is None:
                raise ValueError("No feature maps detected. Check the model layer selection.")
            else:
                raise ValueError("Feature maps are empty. Check the input to the model.")
