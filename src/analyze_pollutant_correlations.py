import duckdb

con = duckdb.connect()

input_file = "data/processed/delhi_2019_01_wide.csv"

query = f"""
WITH complete_data AS (
    SELECT
        "PM2.5" AS pm25,
        "PM10" AS pm10,
        "NO2" AS no2,
        "SO2" AS so2,
        "CO" AS co,
        "Ozone" AS ozone

    FROM read_csv_auto('{input_file}')

    WHERE "PM2.5" IS NOT NULL
    AND "PM10" IS NOT NULL
    AND "NO2" IS NOT NULL
    AND "SO2" IS NOT NULL
    AND "CO" IS NOT NULL
    AND "Ozone" IS NOT NULL
)

SELECT
    COUNT(*) AS complete_rows,

    CORR(pm25, pm10) AS PM25_PM10,
    CORR(pm25, no2) AS PM25_NO2,
    CORR(pm25, so2) AS PM25_SO2,
    CORR(pm25, co) AS PM25_CO,
    CORR(pm25, ozone) AS PM25_Ozone

FROM complete_data;
"""

result = con.execute(query).df()

print("PM2.5 Correlation Analysis")
print(result.to_string(index=False))

con.close()