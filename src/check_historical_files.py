
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("XKDR_API_KEY")
BASE_URL = "https://airquality.xkdr.org"

if not API_KEY:
    raise ValueError("XKDR_API_KEY not found in .env file")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Get historical file information
response = requests.get(
    f"{BASE_URL}/v1/files",
    headers=headers,
    timeout=30
)

response.raise_for_status()

files = response.json()["files"]

# Keep monthly measurement files from 2019 to 2025
historical_files = [
    f for f in files
    if f.get("kind") == "measurements"
    and 2019 <= f.get("year", 0) <= 2025
    and 1 <= f.get("month", 0) <= 12
]

# Sort by year and month
historical_files.sort(
    key=lambda f: (f["year"], f["month"])
)

print("\nAVAILABLE HISTORICAL FILES (2019-2025)")
print("-" * 60)

for file in historical_files:
    year = file["year"]
    month = file["month"]
    size_mb = file.get("bytes", 0) / (1024 * 1024)

    print(
        f"{year}-{month:02d} | "
        f"Rows: {file.get('rows', 'Unknown'):,} | "
        f"Size: {size_mb:.2f} MB"
    )

# Check missing months
available_months = {
    (f["year"], f["month"])
    for f in historical_files
}

expected_months = {
    (year, month)
    for year in range(2019, 2026)
    for month in range(1, 13)
}

missing_months = sorted(expected_months - available_months)

print("\nSUMMARY")
print("-" * 60)
print("Available monthly files:", len(available_months))
print("Expected monthly files:", len(expected_months))
print("Missing monthly files:", len(missing_months))

if missing_months:
    print("\nMissing months:")
    for year, month in missing_months:
        print(f"{year}-{month:02d}")
else:
    print("\nAll 84 monthly files are available.")
