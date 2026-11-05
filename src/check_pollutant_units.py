import duckdb

con = duckdb.connect()

input_file = "data/raw/2019_01.parquet"

query = f"""
SELECT
    parameter_name,
    unit,
    COUNT(*) AS total_records,
    COUNT(DISTINCT station_id) AS total_stations

FROM read_parquet('{input_file}')

WHERE state_name = 'Delhi'
AND parameter_name IN (
    'PM2.5',
    'PM10',
    'NO2',
    'SO2',
    'CO',
    'Ozone'
)

GROUP BY parameter_name, unit

ORDER BY parameter_name, unit;
"""

result = con.execute(query).df()

print("Pollutant Measurement Units")
print(result.to_string(index=False))

con.close()