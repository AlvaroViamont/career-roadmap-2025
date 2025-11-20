import sys
import time
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def main():
    print("⏳ Esperando a que la base de datos arranque...")
    time.sleep(5) # Damos tiempo a Postgres para despertar

    print("🚀 Iniciando Simulación ETL...")

    # 1. Generar Datos (Simulación)
    data = {
        'sensor_id': np.random.randint(1, 10, 100),
        'temperatura': np.random.normal(25, 5, 100).round(2),
        'presion': np.random.normal(1013, 10, 100).round(2),
        'timestamp': pd.Timestamp.now()
    }
    df = pd.DataFrame(data)
    
    print(f"📊 Se generaron {len(df)} registros simulados.")

    # 2. Conexión a Base de Datos
    # NOTA: El host es 'db', que es el nombre del servicio en docker-compose
    connection_string = 'postgresql://usuario_datos:password_secreto@db:5432/base_integrador'
    
    try:
        engine = create_engine(connection_string)
        
        # 3. Cargar Datos (Load)
        print("💾 Guardando en base de datos...")
        df.to_sql('lecturas_sensores', engine, if_exists='append', index=False)
        
        print("✅ ¡Éxito! Datos guardados en la tabla 'lecturas_sensores'.")
        
    except Exception as e:
        print(f"❌ Error fatal conectando a la DB: {e}")

if __name__ == "__main__":
    main()