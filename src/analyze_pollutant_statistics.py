import duckdb

con = duckdb.connect()

input_file = "data/raw/2019_01.parquet"

query = f"""
SELECT
    parameter_name,
    unit,

    COUNT(*) AS total_records,

    ROUND(MIN(value), 2) AS minimum,
    ROUND(quantile_cont(value, 0.25), 2) AS q1,
    ROUND(quantile_cont(value, 0.50), 2) AS median,
    ROUND(AVG(value), 2) AS average,
    ROUND(quantile_cont(value, 0.75), 2) AS q3,
    ROUND(MAX(value), 2) AS maximum,

    COUNT(*) FILTER (WHERE value = 0) AS zero_values

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

ORDER BY parameter_name;
"""

result = con.execute(query).df()

print("Pollutant Statistical Analysis")
print(result.to_string(index=False))

con.close()