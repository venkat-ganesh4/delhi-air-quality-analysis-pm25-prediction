import duckdb

con = duckdb.connect()

input_file = "data/processed/delhi_2019_01_wide.csv"

query = f"""
SELECT
    station_id,
    station_name,

    COUNT(*) FILTER (
        WHERE "PM2.5" IS NOT NULL
        AND "PM10" IS NOT NULL
        AND "NO2" IS NOT NULL
        AND "SO2" IS NOT NULL
        AND "CO" IS NOT NULL
        AND "Ozone" IS NOT NULL
    ) AS complete_rows

FROM read_csv_auto('{input_file}')

GROUP BY station_id, station_name

HAVING complete_rows > 0

ORDER BY complete_rows DESC;
"""

result = con.execute(query).df()

print("Complete Model Rows by Station")
print(result.to_string(index=False))

con.close()