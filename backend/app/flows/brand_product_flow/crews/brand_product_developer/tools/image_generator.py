from openai import OpenAI
import base64
import re
import os
import logging
import traceback
import requests
import json
from app.flows.brand_product_flow.crews.brand_product_developer.tools.azure_blob_uploader import upload_image_to_azure_blob

logger = logging.getLogger(__name__)
image_provider = os.getenv("AI_IMAGE_PROVIDER")

def ai_generate_image(prompt: str, product_name: str) -> str:
    try:
        if image_provider == "AZURE":
            # Use Azure OpenAI endpoint with POST request
            azure_endpoint = os.getenv("IMAGE_API_BASE")
            api_version =  os.getenv("IMAGE_API_VERSION")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.getenv('IMAGE_API_KEY')}"
            }
            
            payload = {
                "prompt": prompt,
                "size": "1024x1024",
                "n": 1,
                "model": "dall-e-3",
                "style" : "vivid",
                "quality" : "hd",
                "n" : 1
            }
            
            response = requests.post(
                f"{azure_endpoint}",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(f"Azure OpenAI API request failed with status {response.status_code}: {response.text}")
            
            response_data = response.json()
            image_url = response_data['data'][0]['url']
            image_response = requests.get(image_url)
            if image_response.status_code != 200:
                raise Exception(f"Failed to download image from Azure URL: {image_response.text}")
            image_bytes = image_response.content
            
        elif image_provider == "OPENAI":
            # Use OpenAI client for other providers
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                n=1,
                size="1024x1024",
                quality="high",
                background="transparent"
            )
            image_base64 = response.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)
        else:
            raise ValueError(f"Invalid image provider: {image_provider}")
        
        filename = re.sub(r'[\W_]+', '_', product_name).lower() + ".png"

        with open(filename, "wb") as f:
            f.write(image_bytes)
        logger.info(f"Image saved locally: {filename}")

        try:
            image_url = upload_image_to_azure_blob(filename, product_name)
        except Exception as e:
            logger.error(f"Azure Blob Storage upload failed: {e}", exc_info=True)
            return f"Error: Upload to Azure Blob Storage failed. Details: {str(e)}"

        os.remove(filename)
        return image_url

    except Exception as e:
        logger.error("Image generation failed", exc_info=True)
        return f"Error: Image generation failed. Details: {str(e)}"



