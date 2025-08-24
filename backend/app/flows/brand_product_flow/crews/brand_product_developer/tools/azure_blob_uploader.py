import os
import logging
from azure.storage.blob import BlobServiceClient, ContentSettings
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

def get_azure_blob_client():
    """Get Azure Blob Service Client"""
    try:
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_string:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable not set")
        
        return BlobServiceClient.from_connection_string(connection_string)
    except Exception as e:
        logger.error(f"Failed to create Azure Blob Service Client: {e}")
        raise

def upload_image_to_azure_blob(file_path: str, product_name: str) -> str:
    """
    Upload an image file to Azure Blob Storage
    
    Args:
        file_path (str): Path to the local image file
        product_name (str): Name of the product for naming the blob
        
    Returns:
        str: URL of the uploaded image in Azure Blob Storage
    """
    try:
        # Get blob service client
        blob_service_client = get_azure_blob_client()
        
        # Get container name from environment variable
        container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "product-images")
        
        # Generate unique blob name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        safe_product_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_product_name = safe_product_name.replace(' ', '_')
        
        blob_name = f"{safe_product_name}_{timestamp}_{unique_id}.png"
        
        # Get blob client
        blob_client = blob_service_client.get_blob_client(
            container=container_name, 
            blob=blob_name
        )
        
        # Upload the file
        with open(file_path, "rb") as data:
            content_settings = ContentSettings(content_type="image/png")
            blob_client.upload_blob(
                data, 
                overwrite=True,
                content_settings=content_settings
            )
        
        # Get the URL
        blob_url = blob_client.url
        
        logger.info(f"Successfully uploaded image to Azure Blob Storage: {blob_url}")
        return blob_url
        
    except Exception as e:
        logger.error(f"Failed to upload image to Azure Blob Storage: {e}", exc_info=True)
        raise

def delete_blob_from_azure(blob_url: str) -> bool:
    """
    Delete a blob from Azure Blob Storage
    
    Args:
        blob_url (str): URL of the blob to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        # Extract container name and blob name from URL
        # URL format: https://storageaccount.blob.core.windows.net/container/blobname
        parts = blob_url.split('/')
        container_name = parts[-2]
        blob_name = parts[-1]
        
        blob_service_client = get_azure_blob_client()
        blob_client = blob_service_client.get_blob_client(
            container=container_name, 
            blob=blob_name
        )
        
        blob_client.delete_blob()
        logger.info(f"Successfully deleted blob: {blob_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to delete blob: {e}", exc_info=True)
        return False
