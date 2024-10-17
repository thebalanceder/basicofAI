import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 1. Fuzzy Logic System
# Define fuzzy variables (Antecedents and Consequents)
acidity = ctrl.Antecedent(np.arange(0, 11, 1), 'acidity')
sugar = ctrl.Antecedent(np.arange(0, 11, 1), 'sugar')
ph = ctrl.Antecedent(np.arange(0, 14, 1), 'ph')
quality = ctrl.Consequent(np.arange(0, 11, 1), 'quality')

# Define membership functions for fuzzy variables
acidity['low'] = fuzz.trimf(acidity.universe, [0, 0, 5])
acidity['medium'] = fuzz.trimf(acidity.universe, [3, 5, 7])
acidity['high'] = fuzz.trimf(acidity.universe, [5, 10, 10])

sugar['low'] = fuzz.trimf(sugar.universe, [0, 0, 5])
sugar['medium'] = fuzz.trimf(sugar.universe, [3, 5, 7])
sugar['high'] = fuzz.trimf(sugar.universe, [5, 10, 10])

ph['low'] = fuzz.trimf(ph.universe, [0, 0, 7])
ph['medium'] = fuzz.trimf(ph.universe, [5, 7, 9])
ph['high'] = fuzz.trimf(ph.universe, [7, 14, 14])

quality['poor'] = fuzz.trimf(quality.universe, [0, 0, 5])
quality['average'] = fuzz.trimf(quality.universe, [4, 5, 6])
quality['good'] = fuzz.trimf(quality.universe, [5, 10, 10])

# Define fuzzy rules
rule1 = ctrl.Rule(acidity['low'] & sugar['high'] & ph['low'], quality['good'])
rule2 = ctrl.Rule(acidity['medium'] & sugar['medium'] & ph['medium'], quality['average'])
rule3 = ctrl.Rule(acidity['high'] & sugar['low'] & ph['high'], quality['poor'])

# Create control system and simulation
quality_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
quality_simulation = ctrl.ControlSystemSimulation(quality_ctrl)

# 2. Neural Network for Learning
# Create some synthetic data for training
np.random.seed(0)
X_train = np.random.rand(100, 3) * 10  # Random values for acidity, sugar, and ph
y_train = (X_train[:, 0] + X_train[:, 1] + X_train[:, 2]) / 3  # Simple average as target

# Build a neural network model
model = Sequential()
model.add(Dense(8, input_dim=3, activation='relu'))  # Input is 3 features
model.add(Dense(4, activation='relu'))
model.add(Dense(1))  # Output layer

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=150, verbose=0)

# 3. Combine Neural Network and Fuzzy Logic
# Evaluate on some test data
X_test = np.array([[6.0, 8.0, 7.5], [3.0, 3.0, 5.5], [9.0, 2.0, 9.0]])

for i in range(len(X_test)):
    acidity_input = np.clip(X_test[i][0], 0, 10)
    sugar_input = np.clip(X_test[i][1], 0, 10)
    ph_input = np.clip(X_test[i][2], 0, 14)
    
    # Neural network prediction
    nn_prediction = model.predict(X_test[i].reshape(1, -1))
    
    # Fuzzification of inputs
    quality_simulation.input['acidity'] = acidity_input
    quality_simulation.input['sugar'] = sugar_input
    quality_simulation.input['ph'] = ph_input

    # Compute fuzzy output
    quality_simulation.compute()

    # Check if fuzzy output is available
    if 'quality' in quality_simulation.output:
        fuzzy_quality = quality_simulation.output['quality']
        print(f"Test case {i + 1}:")
        print(f"  Inputs -> Acidity: {acidity_input}, Sugar: {sugar_input}, pH: {ph_input}")
        print(f"  Neural Network Prediction: {nn_prediction[0][0]}")
        print(f"  Fuzzy Logic Prediction: {fuzzy_quality}")
    else:
        print(f"Test case {i + 1}: No fuzzy output for the given inputs.")
    print("-" * 50)

