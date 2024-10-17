import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# 1. Generating synthetic data
np.random.seed(42)
data_size = 500
acidity = np.random.uniform(0, 10, data_size)  # Acidity values from 0 to 10
sugar = np.random.uniform(0, 10, data_size)    # Sugar values from 0 to 10
ph = np.random.uniform(0, 14, data_size)       # pH values from 0 to 14
# Target (Wine Quality): Simple classification into 3 classes (poor, average, good)
wine_quality = (acidity + sugar + ph) / 3
wine_quality = np.digitize(wine_quality, [4, 7])  # 0: poor, 1: average, 2: good

# Combine features into one dataset
X = np.column_stack((acidity, sugar, ph))
y = wine_quality

# 2. Data Preprocessing
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 3. Build Neural Network Model
model = Sequential()
model.add(Dense(12, input_dim=3, activation='relu'))  # Input layer with 3 features
model.add(Dense(8, activation='relu'))               # Hidden layer with 8 neurons
model.add(Dense(3, activation='softmax'))            # Output layer with 3 classes (poor, average, good)

# 4. Compile the Model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 5. Train the Model
model.fit(X_train, y_train, epochs=150, batch_size=10, verbose=0)

# 6. Evaluate the Model
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# 7. Neural Network-Based Expert System for Prediction
def classify_wine(acidity_value, sugar_value, ph_value):
    input_data = np.array([[acidity_value, sugar_value, ph_value]])
    input_scaled = scaler.transform(input_data)  # Scale the input data
    prediction = model.predict(input_scaled)
    predicted_class = np.argmax(prediction, axis=1)
    
    if predicted_class == 0:
        return "Poor Quality"
    elif predicted_class == 1:
        return "Average Quality"
    else:
        return "Good Quality"

# 8. Testing the Expert System
test_acidity = 6.5
test_sugar = 8.0
test_ph = 7.2
result = classify_wine(test_acidity, test_sugar, test_ph)
print(f"Predicted wine quality: {result}")

