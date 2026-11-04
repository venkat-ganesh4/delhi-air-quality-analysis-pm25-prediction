
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("XKDR_API_KEY")
BASE_URL = "https://airquality.xkdr.org"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Get the list of historical files
response = requests.get(
    f"{BASE_URL}/v1/files",
    headers=headers,
    timeout=30
)

response.raise_for_status()

files = response.json()["files"]

# Find January 2019
file_info = next(
    (
        f for f in files
        if f.get("year") == 2019 and f.get("month") == 1
    ),
    None
)

if file_info is None:
    print("January 2019 file not found.")
    raise SystemExit

# Download the file
download_url = f"{BASE_URL}/v1/files/{file_info['key']}"

download_response = requests.get(
    download_url,
    headers=headers,
    timeout=120
)

download_response.raise_for_status()

# Save the file
output_path = Path("data/raw/2019_01.parquet")
output_path.parent.mkdir(parents=True, exist_ok=True)

output_path.write_bytes(download_response.content)

print("Download successful!")
print("Saved to:", output_path)
print("File size:", round(output_path.stat().st_size / (1024 * 1024), 2), "MB")
