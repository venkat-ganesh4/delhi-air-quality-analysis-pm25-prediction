
import duckdb
from pathlib import Path

input_file = "data/raw/2019_01.parquet"
output_file = "data/processed/delhi_2019_01.csv"

# Create output directory
Path("data/processed").mkdir(parents=True, exist_ok=True)

# Connect to DuckDB
con = duckdb.connect()

# Extract Delhi and our six required pollutants
query = """
    SELECT
        station_id,
        station_name,
        collected_at,
        parameter_name,
        value
    FROM read_parquet(?)
    WHERE state_name = 'Delhi'
      AND parameter_name IN (
          'PM2.5',
          'PM10',
          'NO2',
          'SO2',
          'CO',
          'Ozone'
      )
    ORDER BY station_id, collected_at
"""

df = con.execute(query, [input_file]).fetchdf()

# Save the extracted data
df.to_csv(output_file, index=False)

print("Delhi data extraction successful!")
print("Total records:", len(df))
print("Saved to:", output_file)

con.close()
