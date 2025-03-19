import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 🔹 1️⃣ Generar datos sintéticos
def generate_dummy_data(n=10000):
    np.random.seed(42)
    
    # Generar montos aleatorios entre 100 y 10000
    amounts = np.random.uniform(100, 10000, n)
    
    # Definir fraude: Si el monto es mayor a 5000, es fraude (1), si no, no (0)
    frauds = (amounts > 5000).astype(int)
    
    # Crear DataFrame
    df = pd.DataFrame({"monto": amounts, "fraudulento": frauds})
    
    return df

# 🔹 2️⃣ Crear los datos de entrenamiento
df = generate_dummy_data()

# Separar características (X) y etiquetas (y)
X = df[['monto']].values
y = df['fraudulento'].values

# Normalizar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir en datos de entrenamiento y prueba (80%-20%)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = keras.Sequential([
    keras.layers.Dense(16, activation='relu', input_shape=(1,)),  # Capa oculta 1
    keras.layers.Dense(8, activation='relu'),  # Capa oculta 2
    keras.layers.Dense(1, activation='sigmoid')  # Capa de salida (0 o 1)
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

loss, accuracy = model.evaluate(X_test, y_test)
print(f"🔍 Precisión del modelo: {accuracy:.2f}")

model.save("fraud_detection_model.h5")
print("✅ Modelo guardado como 'fraud_detection_model.h5'")
