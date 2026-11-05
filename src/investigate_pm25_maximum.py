import duckdb

con = duckdb.connect()

input_file = "data/processed/delhi_2019_01.csv"

# Count readings exactly equal to 1,000
count_query = f"""
SELECT
    COUNT(*) AS readings_equal_to_1000,
    COUNT(DISTINCT station_id) AS stations_with_1000
FROM read_csv_auto('{input_file}')
WHERE parameter_name = 'PM2.5'
AND value = 1000;
"""

count_result = con.execute(count_query).df()

print("PM2.5 Readings Exactly Equal to 1000")
print(count_result.to_string(index=False))

# Inspect the 20 highest readings
top_query = f"""
SELECT
    station_id,
    station_name,
    collected_at,
    value
FROM read_csv_auto('{input_file}')
WHERE parameter_name = 'PM2.5'
ORDER BY value DESC
LIMIT 20;
"""

top_result = con.execute(top_query).df()

print("\nTop 20 PM2.5 Readings")
print(top_result.to_string(index=False))

con.close()