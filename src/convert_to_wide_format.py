import duckdb

con = duckdb.connect()

input_file = "data/processed/delhi_2019_01.csv"
output_file = "data/processed/delhi_2019_01_wide.csv"

query = f"""
COPY (
    PIVOT (
        SELECT
            station_id,
            station_name,
            collected_at,
            parameter_name,
            value
        FROM read_csv_auto('{input_file}')
    )
    ON parameter_name IN ('PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'Ozone')
    USING first(value)
    GROUP BY station_id, station_name, collected_at
)
TO '{output_file}'
(HEADER, DELIMITER ',');
"""

con.execute(query)

# Check the output
result = con.execute(
    f"SELECT COUNT(*) FROM read_csv_auto('{output_file}')"
).fetchone()

print("Wide-format conversion successful!")
print("Total rows:", result[0])
print("Saved to:", output_file)

print("\nOutput columns:")
print(
    con.execute(
        f"DESCRIBE SELECT * FROM read_csv_auto('{output_file}')"
    ).df()["column_name"].tolist()
)

con.close()