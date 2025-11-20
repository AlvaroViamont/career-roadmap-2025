import os
import time
import requests
import pandas as pd
from sqlalchemy import create_engine

# Configuración
LOCATIONS = {
    "Londres": {"lat": 51.5074, "lon": -0.1278},
    "Nueva York": {"lat": 40.7128, "lon": -74.0060},
    "Tokio": {"lat": 35.6762, "lon": 139.6503}
}
INTERVALO_SEGUNDOS = 60  # Ejecutar cada minuto (Para ver resultados rápido)

def get_weather_data(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None

def run_etl_process(api_key, engine):
    """Esta función contiene la lógica de UNA ejecución"""
    print(f"\n⏰ Ejecutando ciclo ETL: {pd.Timestamp.now()}")
    weather_records = []

    for city, coords in LOCATIONS.items():
        data = get_weather_data(coords["lat"], coords["lon"], api_key)
        if data:
            record = {
                "ciudad": city,
                "temperatura": data["main"]["temp"],
                "humedad": data["main"]["humidity"],
                "descripcion": data["weather"][0]["description"],
                "timestamp": pd.Timestamp.now()
            }
            weather_records.append(record)
            print(f"   -> {city}: {record['temperatura']}°C")
        time.sleep(0.5) # Pequeña pausa para no saturar la API

    if weather_records:
        try:
            df = pd.DataFrame(weather_records)
            df.to_sql('clima_real', engine, if_exists='append', index=False)
            print("   ✅ Datos guardados.")
        except Exception as e:
            print(f"   ❌ Error DB: {e}")

def main():
    print("⏳ Iniciando servicio de monitoreo continuo...")
    time.sleep(5) # Esperar a la DB inicial

    api_key = os.getenv("OPENWEATHER_API_KEY")
    connection_string = 'postgresql://usuario_datos:password_secreto@db:5432/base_integrador'
    engine = create_engine(connection_string)

    # --- BUCLE INFINITO ---
    while True:
        run_etl_process(api_key, engine)
        
        print(f"💤 Durmiendo por {INTERVALO_SEGUNDOS} segundos...")
        time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    main()