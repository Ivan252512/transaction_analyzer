import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def generate_dummy_data(n=10000):
    np.random.seed(42)
    
    # Generar montos aleatorios entre 100 y 10000
    amounts = np.random.uniform(100, 10000, n)
    amounts_binary = (amounts > 5000).astype(int)
    
    # Generar datos aleatorios de existencia de origen y destino
    origen_existente = np.random.randint(0, 2, n)
    destino_existente = np.random.randint(0, 2, n)
    
    # Generar cantidad aleatoria de transferencias en un minuto
    cantidad_transferencias = np.random.randint(1, 10, n)
    transacciones_mayor_dos = (cantidad_transferencias > 2).astype(int)
    
    # Simular monto acumulado para dos transferencias
    monto_acumulado = [np.sum(np.random.uniform(100, 10000, 2)) for _ in range(n)]
    monto_acumulado_binary = (np.array(monto_acumulado) > 6000).astype(int)
    
    # Calcular si es fraudulento basado en las reglas dadas
    frauds = (0.2 * amounts_binary + 0.2 * (1 - origen_existente) + 
              0.2 * (1 - destino_existente) + 0.2 * transacciones_mayor_dos + 
              0.2 * monto_acumulado_binary >= 0.6).astype(int)
    
    # Crear DataFrame
    df = pd.DataFrame({
        "monto_binario": amounts_binary,
        "origen_existente": origen_existente,
        "destino_existente": destino_existente,
        "transacciones_mayor_dos": transacciones_mayor_dos,
        "monto_acumulado_binario": monto_acumulado_binary,
        "fraudulento": frauds
    })
    
    df.to_csv("datos_entrenamiento.csv", index=False)
    return df

# Crear los datos de entrenamiento
df = generate_dummy_data()

# Separar características (X) y etiquetas (y)
X = df[['monto_binario', 'origen_existente', 'destino_existente', 'transacciones_mayor_dos', 'monto_acumulado_binario']].values
y = df['fraudulento'].values

# No necesitamos escalar los datos ya que son binarios
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Configurar el modelo
model = keras.Sequential([
    keras.layers.Dense(16, activation='relu', input_shape=(5,)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Evaluar el modelo
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Precisión del modelo: {accuracy:.2f}")

# Guardar el modelo
model.save("fraud_detection_model.h5")
print("Modelo guardado como 'fraud_detection_model.h5'")
