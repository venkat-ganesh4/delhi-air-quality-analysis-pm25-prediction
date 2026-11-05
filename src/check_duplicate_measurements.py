import duckdb

con = duckdb.connect()

file_path = "data/processed/delhi_2019_01.csv"

# Find duplicate station, timestamp and pollutant combinations
query = f"""
SELECT
    COUNT(*) AS duplicate_groups,
    COALESCE(SUM(record_count - 1), 0) AS extra_rows
FROM (
    SELECT
        station_id,
        collected_at,
        parameter_name,
        COUNT(*) AS record_count
    FROM read_csv_auto('{file_path}')
    GROUP BY
        station_id,
        collected_at,
        parameter_name
    HAVING COUNT(*) > 1
)
"""

result = con.execute(query).fetchone()

print("Duplicate Analysis")
print("------------------")
print("Duplicate groups:", result[0])
print("Extra duplicate rows:", result[1])

# Display a few examples if duplicates exist
if result[0] > 0:
    sample_query = f"""
    SELECT
        station_id,
        collected_at,
        parameter_name,
        COUNT(*) AS record_count
    FROM read_csv_auto('{file_path}')
    GROUP BY
        station_id,
        collected_at,
        parameter_name
    HAVING COUNT(*) > 1
    LIMIT 10
    """

    print("\nSample duplicate records:")
    print(con.execute(sample_query).df())
else:
    print("\nNo duplicate measurement combinations found.")

con.close()