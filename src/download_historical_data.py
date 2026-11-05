
import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# Project configuration
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw"

load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("XKDR_API_KEY")
BASE_URL = "https://airquality.xkdr.org"

if not API_KEY:
    raise ValueError("XKDR_API_KEY not found in .env file")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

DATA_DIR.mkdir(parents=True, exist_ok=True)

# Get available historical files
response = requests.get(
    f"{BASE_URL}/v1/files",
    headers=headers,
    timeout=30
)

response.raise_for_status()

files = response.json()["files"]

historical_files = [
    f for f in files
    if f.get("kind") == "measurements"
    and 2019 <= f.get("year", 0) <= 2025
    and 1 <= f.get("month", 0) <= 12
]

historical_files.sort(
    key=lambda f: (f["year"], f["month"])
)

print(f"Found {len(historical_files)} monthly files.")

downloaded = 0
skipped = 0
failed = []

# Download files one by one
for index, file_info in enumerate(historical_files, start=1):

    year = file_info["year"]
    month = file_info["month"]
    expected_size = file_info.get("bytes")

    filename = f"{year}_{month:02d}.parquet"
    output_path = DATA_DIR / filename
    temp_path = DATA_DIR / f"{filename}.part"

    # Skip files that already match the API file size
    if (
        output_path.exists()
        and output_path.stat().st_size > 0
        and (
            expected_size is None
            or output_path.stat().st_size == expected_size
        )
    ):
        print(f"[{index}/{len(historical_files)}] SKIPPED: {filename}")
        skipped += 1
        continue

    download_url = f"{BASE_URL}/v1/files/{file_info['key']}"

    print(f"[{index}/{len(historical_files)}] Downloading: {filename}")

    success = False

    for attempt in range(1, 4):
        try:
            with requests.get(
                download_url,
                headers=headers,
                stream=True,
                timeout=(15, 120)
            ) as download_response:

                download_response.raise_for_status()

                total_bytes = 0

                with open(temp_path, "wb") as output_file:
                    for chunk in download_response.iter_content(
                        chunk_size=1024 * 1024
                    ):
                        if chunk:
                            output_file.write(chunk)
                            total_bytes += len(chunk)

            # Verify downloaded size
            if expected_size is not None and total_bytes != expected_size:
                raise ValueError(
                    f"Size mismatch: expected {expected_size} bytes, "
                    f"received {total_bytes} bytes"
                )

            # Replace final file only after successful download
            temp_path.replace(output_path)

            size_mb = total_bytes / (1024 * 1024)

            print(f"    SUCCESS: {size_mb:.2f} MB")

            downloaded += 1
            success = True
            break

        except (requests.RequestException, OSError, ValueError) as error:
            print(f"    Attempt {attempt} failed: {error}")

            if temp_path.exists():
                temp_path.unlink()

            if attempt < 3:
                time.sleep(2)

    if not success:
        failed.append(filename)
        print(f"    FAILED: {filename}")

# Final summary
total_size_mb = sum(
    f.stat().st_size
    for f in DATA_DIR.glob("*.parquet")
) / (1024 * 1024)

print("\nDOWNLOAD SUMMARY")
print("-" * 40)
print("Downloaded:", downloaded)
print("Skipped:", skipped)
print("Failed:", len(failed))
print(f"Total Parquet storage: {total_size_mb:.2f} MB")

if failed:
    print("\nFiles that failed:")
    for filename in failed:
        print(filename)
else:
    print("\nAll available monthly files are downloaded.")
