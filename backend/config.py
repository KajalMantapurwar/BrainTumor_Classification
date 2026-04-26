import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Secret key (for JWT & security)
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")

    # Upload folder
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

    # Output folders
    OUTPUT_FOLDER = os.path.join(os.getcwd(), "outputs")
    GRADCAM_FOLDER = os.path.join(OUTPUT_FOLDER, "gradcam")
    REPORT_FOLDER = os.path.join(OUTPUT_FOLDER, "reports")

    # Allowed file types (MRI images)
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

    # Max upload size (16MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # JWT settings
    JWT_EXPIRATION_HOURS = 24

    # Debug mode
    DEBUG = True