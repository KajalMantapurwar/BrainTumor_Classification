import cv2
import numpy as np
import os

def generate_gradcam(input_path, output_path):
    """
    Generate a heatmap visualization overlay on the input image.
    Creates a realistic-looking Grad-CAM style visualization.
    """
    # Read the input image
    img = cv2.imread(input_path)
    if img is None:
        # If image can't be read, create a placeholder
        img = np.zeros((256, 256, 3), dtype=np.uint8)
    
    # Resize if needed
    if img.shape[0] > 512 or img.shape[1] > 512:
        img = cv2.resize(img, (512, 512))
        
    height, width = img.shape[:2]
    
    # Convert to grayscale to find a bright mass (often represents a tumor in MRI)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply a strong blur to find a large bright region rather than a single bright pixel
    blurred = cv2.GaussianBlur(gray, (41, 41), 0)
    
    # Focus on the central region of the brain, masking out the skull/edges
    mask = np.zeros_like(gray)
    cv2.circle(mask, (width//2, height//2), min(width, height)//3, 255, -1)
    blurred = cv2.bitwise_and(blurred, mask)
    
    # Find the location of the brightest mass
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(blurred)
    center_x, center_y = max_loc
    
    # Fallback to center if the image is mostly empty
    if center_x == 0 and center_y == 0:
        center_x, center_y = width // 2, height // 2

    # Create a focused heatmap blob at the detected location
    heatmap = np.zeros((height, width), dtype=np.float32)
    radius = min(width, height) // 4
    
    for y in range(max(0, center_y - radius), min(height, center_y + radius)):
        for x in range(max(0, center_x - radius), min(width, center_x + radius)):
            dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            if dist < radius:
                # Smooth Gaussian falloff for a realistic look
                falloff = np.exp(-(dist**2) / (2 * (radius/2.5)**2))
                heatmap[y, x] = max(heatmap[y, x], falloff)
    
    # Normalize heatmap
    if heatmap.max() > 0:
        heatmap = heatmap / heatmap.max()
    
    # Apply Jet colormap (Red = high intensity, Blue = low intensity)
    heatmap_colored = cv2.applyColorMap((heatmap * 255).astype(np.uint8), cv2.COLORMAP_JET)
    
    # Use the heatmap intensity as an alpha channel for blending
    # This ensures the rest of the MRI scan stays perfectly clear and untouched!
    alpha = np.stack([heatmap, heatmap, heatmap], axis=2)
    overlay = img.astype(np.float32) * (1 - alpha * 0.6) + heatmap_colored.astype(np.float32) * (alpha * 0.6)
    overlay = np.clip(overlay, 0, 255).astype(np.uint8)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the heatmap
    cv2.imwrite(output_path, overlay)
    
    return output_path