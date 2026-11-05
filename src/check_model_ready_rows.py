import duckdb

con = duckdb.connect()

input_file = "data/processed/delhi_2019_01_wide.csv"

query = f"""
SELECT
    COUNT(*) AS total_rows,

    COUNT(*) FILTER (
        WHERE "PM2.5" IS NOT NULL
    ) AS rows_with_target,

    COUNT(*) FILTER (
        WHERE "PM2.5" IS NOT NULL
        AND "PM10" IS NOT NULL
        AND "NO2" IS NOT NULL
        AND "SO2" IS NOT NULL
        AND "CO" IS NOT NULL
        AND "Ozone" IS NOT NULL
    ) AS complete_rows_for_model

FROM read_csv_auto('{input_file}');
"""

result = con.execute(query).df()

print("Model Data Availability")
print(result.to_string(index=False))

con.close()