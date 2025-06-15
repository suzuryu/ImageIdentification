import numpy as np
import os
import sys
from typing import Tuple, Dict, Union
import cv2

# Constants
CANNY_THRESHOLD_LOW = 100
CANNY_THRESHOLD_HIGH = 200
GAUSSIAN_KERNEL_SIZE = (5, 5)
GAUSSIAN_SIGMA_X = 1
MEDIAN_KERNEL_SIZE = 5
MAX_IMAGE_SIZE = 2000
SCORE_THRESHOLD = 0.5
SCORE_WEIGHTS = {
    'edge': 0.8,
    'color': 0.2
}
SCORE_MULTIPLIER = 0.625

def create_canny_img(gray_img_src: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create three edge-detected images using different preprocessing methods.
    
    Args:
        gray_img_src (np.ndarray): Input grayscale image
        
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: Three edge-detected images:
            - Canny edge detection on original image
            - Canny edge detection after Gaussian blur
            - Canny edge detection after Median blur
    """
    if isinstance(gray_img_src[0][0], np.ndarray):
        gray_img_src = cv2.cvtColor(gray_img_src, cv2.COLOR_BGR2GRAY)
    
    # Original Canny
    can_img = cv2.Canny(gray_img_src, CANNY_THRESHOLD_LOW, CANNY_THRESHOLD_HIGH)
    
    # Gaussian blur + Canny
    gau_img = cv2.GaussianBlur(gray_img_src, GAUSSIAN_KERNEL_SIZE, GAUSSIAN_SIGMA_X)
    gau_can_img = cv2.Canny(gau_img, CANNY_THRESHOLD_LOW, CANNY_THRESHOLD_HIGH)
    
    # Median blur + Canny
    med_img = cv2.medianBlur(gray_img_src, MEDIAN_KERNEL_SIZE)
    med_can_img = cv2.Canny(med_img, CANNY_THRESHOLD_LOW, CANNY_THRESHOLD_HIGH)
 
    return can_img, gau_can_img, med_can_img

def get_color(img_src: np.ndarray) -> float:
    """Calculate the color distribution score of the image.
    
    Args:
        img_src (np.ndarray): Input image
        
    Returns:
        float: Maximum value of the most used color normalized by image size
    """
    color_counts: Dict[Union[Tuple, int], int] = {}
    
    if isinstance(img_src[0][0], np.ndarray):
        for row in img_src:
            for pixel in row:
                pixel_tuple = tuple(pixel)
                color_counts[pixel_tuple] = color_counts.get(pixel_tuple, 0) + 1
    else:
        for row in img_src:
            for pixel in row:
                color_counts[pixel] = color_counts.get(pixel, 0) + 1

    return max(color_counts.values()) / len(img_src)

def calculate_difference(mat: np.ndarray, c_mat: np.ndarray) -> float:
    """Calculate the normalized difference between two matrices.
    
    Args:
        mat (np.ndarray): First matrix
        c_mat (np.ndarray): Second matrix
        
    Returns:
        float: Normalized difference between matrices
    """
    sum_mat = np.sum(mat) / 255
    diff = mat - c_mat
    sum_diff = np.sum(diff) / 255
    return sum_diff / sum_mat if sum_mat != 0 else 0

def calculate_score(gau_result: float, med_result: float, color_result: float) -> float:
    """Calculate the final score for image classification.
    
    Args:
        gau_result (float): Gaussian blur difference score
        med_result (float): Median blur difference score
        color_result (float): Color distribution score
        
    Returns:
        float: Final classification score
    """
    edge_score = gau_result + med_result
    if edge_score == 0:
        return 0
    
    return ((1 / edge_score) * SCORE_WEIGHTS['edge'] + 
            (color_result / 100) * SCORE_WEIGHTS['color']) * SCORE_MULTIPLIER

def resize_image(img_src: np.ndarray) -> np.ndarray:
    """Resize image if it exceeds maximum dimensions.
    
    Args:
        img_src (np.ndarray): Input image
        
    Returns:
        np.ndarray: Resized image if necessary
    """
    height, width = img_src.shape[:2]
    if height > MAX_IMAGE_SIZE or width > MAX_IMAGE_SIZE:
        return cv2.resize(img_src, (width // 2, height // 2))
    return img_src

def identify_image(img_src: np.ndarray) -> str:
    """Identify if the image is an illustration or a photograph.
    
    Args:
        img_src (np.ndarray): Input image
        
    Returns:
        str: 'illust' for illustration, 'picture' for photograph
    """
    can_img, gau_can_img, med_can_img = create_canny_img(img_src)
    gau_result = calculate_difference(can_img, gau_can_img)
    med_result = calculate_difference(can_img, med_can_img)
    color_result = get_color(img_src)
    
    score = calculate_score(gau_result, med_result, color_result)
    print(f"score: {round(score, 3)} -->", end="")
    
    return "illust" if score >= SCORE_THRESHOLD else "picture"

def main():
    """Main function to process command line arguments and identify image."""
    if len(sys.argv) != 2:
        print("Error: Please provide an image file path as argument")
        sys.exit(1)
    
    img_name = sys.argv[1]
    if not os.path.exists(img_name):
        print(f"Error: File '{img_name}' does not exist")
        sys.exit(1)
        
    try:
        img_src = cv2.imread(img_name, cv2.IMREAD_UNCHANGED)
        if img_src is None:
            print(f"Error: Could not read image '{img_name}'")
            sys.exit(1)
            
        img_src = resize_image(img_src)
        result = identify_image(img_src)
        print(result)
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
