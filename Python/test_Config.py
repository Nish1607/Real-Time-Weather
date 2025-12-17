import pyodbc # type: ignore
import requests
from config import API_KEY, BASE_URL_CURRENT, CITIES, CONN_STR

# Test API
r = requests.get(
    BASE_URL_CURRENT,
    params={"key": API_KEY, "q": CITIES[0], "aqi": "yes"},
    timeout=30
)
print("API status:", r.status_code)
print("City:", CITIES[0])

# Test SQL
conn = pyodbc.connect(CONN_STR)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM dbo.dim_city;")
print("Cities in DB:", cur.fetchone()[0])
conn.close()
