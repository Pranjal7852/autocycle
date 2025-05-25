# tools/cloudinary_tool.py
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

cloudinary.config(
  cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
  api_key=os.getenv("CLOUDINARY_API_KEY"),
  api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_image_to_cloudinary(file_path: str, product_name: str) -> str:
    result = cloudinary.uploader.upload(
        file_path,
        public_id=f"product_images/{product_name}",
        overwrite=True,
        resource_type="image"
    )
    return result["secure_url"]
