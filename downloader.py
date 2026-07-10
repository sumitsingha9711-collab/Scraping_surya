import json
import os
from urllib.parse import urlparse

import requests

# Create images directory if it doesn't exist
os.makedirs("images", exist_ok=True)

# Load scraped pages
with open("data/pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

downloaded = set()
download_count = 0

for page in pages:
    for image_url in page.get("images", []):

        # Skip duplicate images
        if image_url in downloaded:
            continue

        downloaded.add(image_url)

        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()

            # Get filename from URL
            filename = os.path.basename(urlparse(image_url).path)

            # Handle URLs ending with /
            if not filename:
                filename = f"image_{download_count + 1}.jpg"

            filepath = os.path.join("images", filename)

            # Avoid overwriting existing files
            if os.path.exists(filepath):
                name, ext = os.path.splitext(filename)
                counter = 1

                while os.path.exists(filepath):
                    filepath = os.path.join(
                        "images",
                        f"{name}_{counter}{ext}"
                    )
                    counter += 1

            with open(filepath, "wb") as img_file:
                img_file.write(response.content)

            download_count += 1
            print(f"Downloaded: {os.path.basename(filepath)}")

        except Exception as e:
            print(f"Failed to download {image_url}")
            print(e)

print(f"\nDownloaded {download_count} images.")