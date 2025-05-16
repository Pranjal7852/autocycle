# -*- coding: utf-8 -*-
from openai import OpenAI
import base64

client = OpenAI(api_key="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")

# Define brand variables
brand1 = "Marlboro"
brand2 = "Nike"

prompt = f"""
Create a square-format digital promotional image showcasing a fictional collaboration between [{brand1}] and [{brand2}]. The featured product should be a core or iconic item from {brand2}, reimagined with the design aesthetics, technology, or identity of {brand1}. Style the product to reflect premium branding, and place it in the center of the frame on a soft, design-conscious background. Use a color palette inspired by modern commercial aesthetics—such as muted pastels (beige, mustard yellow, olive green, soft blue) or bold neutrals (charcoal gray, metallic silver, deep navy). Apply gentle lighting and subtle shadows for a refined, editorial look. Include the text " [{brand1}] × [{brand2}] " at the top in a modern, sans-serif font, and a short, thematic tagline beneath it. Do not use real logos; instead, rely on abstract branding cues like shape language, materials, or color schemes. The final image should feel balanced, modern, and aligned with product advertisement styles.
"""

result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    n=2
)

# Save each image with sequential names
for i, image_data in enumerate(result.data, start=1):
    image_base64 = image_data.b64_json
    image_bytes = base64.b64decode(image_base64)
    
    filename = f"image_{i}.png"
    with open(filename, "wb") as f:
        f.write(image_bytes)
    
    print(f"Saved: {filename}")