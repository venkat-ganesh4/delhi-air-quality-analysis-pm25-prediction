
import duckdb

file_path = "data/raw/2019_01.parquet"

# Connect to DuckDB
con = duckdb.connect()

# Inspect the dataset columns and data types
result = con.execute(
    f"DESCRIBE SELECT * FROM read_parquet('{file_path}')"
)

print("DATASET COLUMNS:")
print(result.fetchdf().to_string(index=False))

# Display the first 5 records
print("\nFIRST 5 RECORDS:")

result = con.execute(
    f"SELECT * FROM read_parquet('{file_path}') LIMIT 5"
)

print(result.fetchdf().to_string(index=False))

# Count records belonging to Delhi
result = con.execute("""
    SELECT COUNT(*) AS total_records
    FROM read_parquet('data/raw/2019_01.parquet')
    WHERE state_name = 'Delhi'
""")

print("\nTOTAL DELHI RECORDS:")
print(result.fetchdf().to_string(index=False))

# Count unique Delhi stations
result = con.execute("""
    SELECT COUNT(DISTINCT station_id) AS total_stations
    FROM read_parquet('data/raw/2019_01.parquet')
    WHERE state_name = 'Delhi'
""")

print("\nTOTAL DELHI STATIONS:")
print(result.fetchdf().to_string(index=False))


# Find available pollutants in Delhi
result = con.execute("""
    SELECT
        parameter_name,
        COUNT(*) AS total_records,
        COUNT(DISTINCT station_id) AS total_stations
    FROM read_parquet('data/raw/2019_01.parquet')
    WHERE state_name = 'Delhi'
    GROUP BY parameter_name
    ORDER BY parameter_name
""")

print("\nDELHI POLLUTANT SUMMARY:")
print(result.fetchdf().to_string(index=False))


con.close()
