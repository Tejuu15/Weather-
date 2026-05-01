# Weather & Air Quality Dashboard – FastAPI
# Uses OpenWeatherMap API (Weather + AQI)
# Run: python main.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

API_KEY = "YOUR_OPENWEATHER_API_KEY"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ---------- Helpers ----------
def get_weather(city: str):
    w = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}").json()
    lat, lon = w['coord']['lat'], w['coord']['lon']
    aqi = requests.get(
        f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}").json()

    return {
        "city": w['name'],
        "temp": w['main']['temp'],
        "humidity": w['main']['humidity'],
        "condition": w['weather'][0]['description'].title(),
        "aqi": aqi['list'][0]['main']['aqi']
    }

# ---------- Routes ----------
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/weather", response_class=HTMLResponse)
def weather(request: Request, city: str = Form(...)):
    data = get_weather(city)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": data
    })

# ---------- Run ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


# -----------------------------
# Create folder: templates/
# Create file: templates/index.html
# -----------------------------

"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Weather & Air Quality</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
<style>
body {
  font-family: Inter, sans-serif;
  background: linear-gradient(135deg, #020617, #020617);
  color: #e5e7eb;
  margin: 0;
  padding: 40px;
}
.container { max-width: 800px; margin: auto; }
h1 { font-size: 2.4rem; margin-bottom: 16px; }
.card {
  background: rgba(2,6,23,.9);
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 25px 50px rgba(0,0,0,.7);
  margin-bottom: 24px;
}
form {
  display: flex;
  gap: 12px;
}
input, button {
  padding: 14px;
  border-radius: 12px;
  border: none;
  font-size: 15px;
}
input {
  flex: 1;
  background: #020617;
  border: 1px solid #1e293b;
  color: white;
}
button {
  background: #60a5fa;
  color: #020617;
  font-weight: 700;
  cursor: pointer;
}
button:hover { background: #3b82f6; }
.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}
.metric {
  background: #020617;
  padding: 20px;
  border-radius: 16px;
  text-align: center;
}
.metric span { font-size: 1.8rem; display: block; }
.aqi-good { color: #4ade80; }
.aqi-moderate { color: #fde047; }
.aqi-bad { color: #f87171; }
</style>
</head>
<body>
<div class="container">
<h1>☁️ Weather & Air Quality</h1>

<div class="card">
<form method="post" action="/weather">
  <input name="city" placeholder="Enter city (e.g. London)" required>
  <button>Check</button>
</form>
</div>

{% if data %}
<div class="card">
<h2>{{ data.city }}</h2>
<p>{{ data.condition }}</p>
<div class="grid">
  <div class="metric"><span>{{ data.temp }}°C</span>Temperature</div>
  <div class="metric"><span>{{ data.humidity }}%</span>Humidity</div>
  <div class="metric">
    <span class="{% if data.aqi <= 2 %}aqi-good{% elif data.aqi == 3 %}aqi-moderate{% else %}aqi-bad{% endif %}">
      AQI {{ data.aqi }}
    </span>Air Quality
  </div>
</div>
</div>
{% endif %}
</div>
</body>
</html>
"""
