from openai import OpenAI
import base64
import re
import os
import logging
import traceback
from app.flows.brand_product_flow.crews.brand_product_developer.tools.cloudinary_uploader import upload_image_to_cloudinary

logger = logging.getLogger(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image_via_openai(prompt: str, product_name: str) -> str:
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="low",
        )
        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        filename = re.sub(r'[\W_]+', '_', product_name).lower() + ".png"

        with open(filename, "wb") as f:
            f.write(image_bytes)
        logger.info(f"Image saved locally: {filename}")

        try:
            image_url = upload_image_to_cloudinary(filename, product_name)
        except Exception as e:
            logger.error(f"Cloudinary upload failed: {e}", exc_info=True)
            return f"Error: Upload to Cloudinary failed. Details: {str(e)}"

        os.remove(filename)
        return image_url

    except Exception as e:
        logger.error("Image generation failed", exc_info=True)
        return f"Error: Image generation failed. Details: {str(e)}"
