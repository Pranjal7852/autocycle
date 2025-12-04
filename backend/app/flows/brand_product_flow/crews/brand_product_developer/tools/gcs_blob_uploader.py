import os
import uuid
import json
from datetime import datetime
from google.cloud import storage
from google.oauth2 import service_account
import logging

logger = logging.getLogger(__name__)


def get_gcs_client():
    """
    Returns an authenticated Google Cloud Storage client.
    Uses service-account JSON if provided.
    Falls back to ADC (Application Default Credentials) in production.
    """
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if cred_path and os.path.exists(cred_path):
        logger.info("Using service account JSON for GCS auth")
        credentials = service_account.Credentials.from_service_account_file(cred_path)
        return storage.Client(credentials=credentials)

    # Fallback → For Cloud Run / GKE / Compute Engine
    logger.info("Using default Google Cloud credentials (ADC)")
    return storage.Client()


def upload_image_to_gcs(file_path: str, product_name: str) -> str:
    try:
        client = get_gcs_client()

        bucket_name = os.getenv("GCS_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("GCS_BUCKET_NAME environment variable not set")

        bucket = client.bucket(bucket_name)

        # Clean product name
        safe_name = "".join(
            c for c in product_name if c.isalnum() or c in (" ", "-", "_")
        ).strip().replace(" ", "_")

        # Build blob name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        blob_name = f"{safe_name}_{timestamp}_{unique_id}.png"

        blob = bucket.blob(blob_name)
        blob.content_type = "image/png"

        # Upload
        blob.upload_from_filename(file_path)

        return blob.public_url

    except Exception as e:
        logger.error(f"GCS Upload failed: {e}", exc_info=True)
        raise
