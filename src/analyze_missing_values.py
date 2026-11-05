import duckdb

con = duckdb.connect()

input_file = "data/processed/delhi_2019_01_wide.csv"

query = f"""
SELECT
    COUNT(*) AS total_rows,

    COUNT("PM2.5") AS PM25_available,
    COUNT("PM10") AS PM10_available,
    COUNT("NO2") AS NO2_available,
    COUNT("SO2") AS SO2_available,
    COUNT("CO") AS CO_available,
    COUNT("Ozone") AS Ozone_available

FROM read_csv_auto('{input_file}');
"""

result = con.execute(query).df()

print("Missing Value Analysis")
print(result.to_string(index=False))

con.close()