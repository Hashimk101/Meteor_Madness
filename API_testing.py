import requests
import sqlite3
import datetime

#db setup
conn = sqlite3.connect("asteroids.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS asteroids (
    id TEXT PRIMARY KEY,
    name TEXT,
    magnitude REAL,
    diameter_min REAL,
    diameter_max REAL,
    close_approach_date TEXT,
    velocity_km_s REAL
)
""")

# api call
API_KEY = "nOToMg7eUhiEMT3BemUq5dsEkDdXprbIpqKEl7sb"
today = datetime.date.today()
url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={today}&api_key={API_KEY}"

response = requests.get(url)
data = response.json()

# extract and store data
near_earth_objects = data["near_earth_objects"][str(today)]

for obj in near_earth_objects:
    asteroid_id = obj["id"]
    name = obj["name"]
    magnitude = obj["absolute_magnitude_h"]
    diameter_min = obj["estimated_diameter"]["meters"]["estimated_diameter_min"]
    diameter_max = obj["estimated_diameter"]["meters"]["estimated_diameter_max"]

    approach = obj["close_approach_data"][0]
    close_date = approach["close_approach_date"]
    velocity = float(approach["relative_velocity"]["kilometers_per_second"])

    cur.execute("""
    INSERT OR REPLACE INTO asteroids VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (asteroid_id, name, magnitude, diameter_min, diameter_max, close_date, velocity))

conn.commit()
conn.close()

print("Asteroid data saved into asteroids.db ✅")
