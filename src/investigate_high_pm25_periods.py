import duckdb

con = duckdb.connect()

input_file = "data/processed/delhi_2019_01.csv"

query = f"""
SELECT
    station_id,
    station_name,
    collected_at,
    value AS PM25

FROM read_csv_auto('{input_file}')

WHERE parameter_name = 'PM2.5'
AND value >= 800

ORDER BY station_id, collected_at;
"""

result = con.execute(query).df()

print("PM2.5 Readings >= 800 µg/m³")
print("Total high readings:", len(result))
print(result.to_string(index=False))

con.close()