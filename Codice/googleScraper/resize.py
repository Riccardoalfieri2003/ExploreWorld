import cv2
import numpy as np


"""
def resize_with_padding(image, target_size):
    # Get the original dimensions
    h, w = image.shape[:2]

    # Calculate the scaling factor
    scale = min(target_size / h, target_size / w)

    # Resize the image
    resized_image = cv2.resize(image, (int(w * scale), int(h * scale)))

    # Create a square canvas
    delta_w = target_size - resized_image.shape[1]
    delta_h = target_size - resized_image.shape[0]
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    # Add padding
    padded_image = cv2.copyMakeBorder(resized_image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    return padded_image
"""

def resize(image, target_size):
    h, w = image.shape[:2]
    crop_size = min(h, w)

    # Calculate the center crop box
    start_x = (w - crop_size) // 2
    start_y = (h - crop_size) // 2

    # Crop and resize
    cropped_image = image[start_y:start_y+crop_size, start_x:start_x+crop_size]
    resized_image = cv2.resize(cropped_image, (target_size, target_size))
    return resized_image

"""
# Example usage
image = cv2.imread("Hawaii.jpg")
target_size = 224
processed_image = resize(image, target_size)

# Save the processed image with a specific name
output_filename = "Hawaii_resize.jpg"
cv2.imwrite(output_filename, processed_image)
"""

