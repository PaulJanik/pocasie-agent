import requests
from datetime import datetime

LAT = 48.9853
LON = 20.3497
NTFY_TOPIC = "palo-pocasie-stiavnik-7f3k"  # váš vlastný topic

# 1. Získanie predpovede z Open-Meteo
url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode"
    f"&timezone=Europe/Bratislava"
)
data = requests.get(url).json()

daily = data["daily"]
tmax = daily["temperature_2m_max"][0]
tmin = daily["temperature_2m_min"][0]
zrazky = daily["precipitation_probability_max"][0]
kod = daily["weathercode"][0]

# Jednoduchý preklad weathercode na text
popis = {
    0: "jasno", 1: "prevažne jasno", 2: "polooblačno", 3: "zamračené",
    45: "hmla", 51: "slabé mrholenie", 61: "slabý dážď", 63: "dážď",
    65: "silný dážď", 71: "sneženie", 73: "sneženie", 75: "silné sneženie",
    80: "prehánky", 95: "búrky"
}.get(kod, "neznáme")

sprava = (
    f"Spišský Štiavnik – dnes: {popis}\n"
    f"Teplota: {tmin:.0f}°C až {tmax:.0f}°C\n"
    f"Pravdepodobnosť zrážok: {zrazky}%"
)

# 2. Odoslanie notifikácie cez ntfy.sh
requests.post(
    f"https://ntfy.sh/{NTFY_TOPIC}",
    data=sprava.encode("utf-8"),
    headers={"Title": "Ranné počasie"}
)

print(sprava)
