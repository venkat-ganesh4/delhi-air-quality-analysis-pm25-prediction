import duckdb

con = duckdb.connect()

query = """
WITH suspicious AS (
    SELECT
        station_id,
        collected_at
    FROM read_csv_auto(
        'data/processed/delhi_2019_01_wide.csv'
    )
    WHERE
        "PM2.5" IS NOT NULL
        AND "PM10" IS NOT NULL
        AND "PM2.5" > "PM10"
)

SELECT
    raw.station_id,
    raw.station_name,
    raw.collected_at,
    raw.parameter_name,
    raw.value,
    raw.unit,
    raw.source

FROM read_parquet('data/raw/2019_01.parquet') AS raw

INNER JOIN suspicious AS s
    ON raw.station_id = s.station_id
    AND raw.collected_at = s.collected_at

WHERE
    raw.state_name = 'Delhi'
    AND raw.parameter_name IN ('PM2.5', 'PM10')

ORDER BY
    raw.station_id,
    raw.collected_at,
    raw.parameter_name

LIMIT 60
"""

result = con.execute(query).df()

print("\nORIGINAL SOURCE RECORDS")
print(result.to_string(index=False))

con.close()