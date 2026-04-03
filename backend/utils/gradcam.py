import cv2

def generate_gradcam(input_path, output_path):
    img = cv2.imread(input_path)
    cv2.imwrite(output_path, img)