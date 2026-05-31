import os
import logging
from google.cloud import storage
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

def get_gcs_client():
    """Get Google Cloud Storage Client"""
    try:
        # If GOOGLE_APPLICATION_CREDENTIALS is set, it will use that file.
        # Otherwise, if deployed on Cloud Run, it automatically uses the default service account.
        return storage.Client()
    except Exception as e:
        logger.error(f"Failed to create GCS Client: {e}")
        raise

def upload_image_to_gcs(file_path: str, product_name: str) -> str:
    """
    Upload an image file to Google Cloud Storage
    
    Args:
        file_path (str): Path to the local image file
        product_name (str): Name of the product for naming the blob
        
    Returns:
        str: Public URL of the uploaded image in Google Cloud Storage
    """
    try:
        # Get storage client
        storage_client = get_gcs_client()
        
        # Get bucket name from environment variable
        bucket_name = os.getenv("GCS_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("GCS_BUCKET_NAME environment variable not set")
            
        bucket = storage_client.bucket(bucket_name)
        
        # Generate unique blob name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        safe_product_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_product_name = safe_product_name.replace(' ', '_')
        
        blob_name = f"{safe_product_name}_{timestamp}_{unique_id}.png"
        
        # Get blob (object) reference
        blob = bucket.blob(blob_name)
        
        # Upload the file
        blob.upload_from_filename(file_path, content_type="image/png")
        
        # Make the blob publicly viewable (Requires bucket to have fine-grained access control or uniform bucket level access configured for public read)
        # However, a cleaner way is just returning the standard URL
        # For public buckets: https://storage.googleapis.com/bucket_name/blob_name
        
        blob_url = f"https://storage.googleapis.com/{bucket_name}/{blob_name}"
        
        logger.info(f"Successfully uploaded image to Google Cloud Storage: {blob_url}")
        return blob_url
        
    except Exception as e:
        logger.error(f"Failed to upload image to Google Cloud Storage: {e}", exc_info=True)
        raise

def delete_blob_from_gcs(blob_url: str) -> bool:
    """
    Delete a blob from Google Cloud Storage
    
    Args:
        blob_url (str): URL of the blob to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        # Extract container name and blob name from URL
        # URL format: https://storage.googleapis.com/bucket_name/blob_name
        parts = blob_url.split('/')
        bucket_name = parts[-2]
        blob_name = parts[-1]
        
        storage_client = get_gcs_client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        blob.delete()
        logger.info(f"Successfully deleted blob: {blob_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to delete blob: {e}", exc_info=True)
        return False
