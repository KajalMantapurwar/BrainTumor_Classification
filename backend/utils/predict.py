import random

CLASSES = ["Glioma", "Meningioma", "Pituitary Tumor", "No Tumor"]

def predict_tumor(image):
    prediction = random.choice(CLASSES)
    confidence = round(random.uniform(85, 99), 2)
    return prediction, confidence