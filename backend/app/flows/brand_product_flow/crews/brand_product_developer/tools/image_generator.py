from openai import OpenAI
import base64
import re
import os
import logging
import traceback
import requests
import json
import io
from app.flows.brand_product_flow.crews.brand_product_developer.tools.azure_blob_uploader import upload_image_to_azure_blob
from app.flows.brand_product_flow.crews.brand_product_developer.tools.gcs_blob_uploader import upload_image_to_gcs
from google import genai
from google.genai import types
from PIL import Image

logger = logging.getLogger(__name__)
image_provider = os.getenv("AI_IMAGE_PROVIDER", "GEMINI")
storage_provider = os.getenv("STORAGE_PROVIDER", "GCS") 

def ai_generate_image(prompt: str, product_name: str) -> str:
    try:
        if image_provider == "GPT":
            # Use Azure OpenAI endpoint with POST request
            azure_endpoint = os.getenv("GPT_IMAGE_URL")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.getenv('GPT_IMAGE_API_KEY')}"
            }
            
            payload = {
                "prompt": prompt,
                "size": "1024x1024",
                "n": 1,
                "quality" : "high",
                "output_compression" : 100,
                "output_format" : "png",
            }
            
            response = requests.post(
                f"{azure_endpoint}",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(f"GPT OpenAI API request failed with status {response.status_code}: {response.text}")
            
            response_data = response.json()
            
            image_base64 = response_data['data'][0]['b64_json']
            image_bytes = base64.b64decode(image_base64)
        
        elif image_provider == "AZURE":
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
        
        elif image_provider == "GEMINI":
            # Use Google Gemini image generation model
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            
            response = client.models.generate_images(
                model="imagen-4.0-generate-001",
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                )
            )

            print("IMAGE DEBUG",response)
            
            # Extract image from response
            image_bytes = response.generated_images[0].image.image_bytes
            
            if image_bytes is None:
                raise Exception("No image data found in Gemini response")
        
        else:
            raise ValueError(f"Invalid image provider: {image_provider}")
        
        filename = re.sub(r'[\W_]+', '_', product_name).lower() + ".png"

        with open(filename, "wb") as f:
            f.write(image_bytes)
        logger.info(f"Image saved locally: {filename}")

        try:
            # Upload to storage based on configured provider
            if storage_provider == "GCS":
                image_url = upload_image_to_gcs(filename, product_name)
            elif storage_provider == "AZURE":
                image_url = upload_image_to_azure_blob(filename, product_name)
            else:
                raise ValueError(f"Invalid storage provider: {storage_provider}. Must be 'AZURE' or 'GCS'")
        except Exception as e:
            logger.error(f"{storage_provider} Storage upload failed: {e}", exc_info=True)
            return f"Error: Upload to {storage_provider} Storage failed. Details: {str(e)}"

        os.remove(filename)
        return image_url

    except Exception as e:
        logger.error("Image generation failed", exc_info=True)
        return f"Error: Image generation failed. Details: {str(e)}"



