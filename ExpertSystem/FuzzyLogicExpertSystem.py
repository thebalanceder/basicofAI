import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define the input variables
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')  # Room temperature
desired_temp = ctrl.Antecedent(np.arange(0, 41, 1), 'desired_temp')  # Desired temperature

# Define the output variable
action = ctrl.Consequent(np.arange(0, 101, 1), 'action')  # Action (Cooling/Heating)

# Define membership functions for temperature
temperature['cold'] = fuzz.trimf(temperature.universe, [0, 0, 20])
temperature['comfortable'] = fuzz.trimf(temperature.universe, [15, 25, 35])
temperature['hot'] = fuzz.trimf(temperature.universe, [30, 40, 40])

# Define membership functions for desired temperature
desired_temp['cold'] = fuzz.trimf(desired_temp.universe, [0, 0, 20])
desired_temp['comfortable'] = fuzz.trimf(desired_temp.universe, [15, 25, 35])
desired_temp['hot'] = fuzz.trimf(desired_temp.universe, [30, 40, 40])

# Define membership functions for action
action['cool'] = fuzz.trimf(action.universe, [0, 0, 50])
action['maintain'] = fuzz.trimf(action.universe, [25, 50, 75])
action['heat'] = fuzz.trimf(action.universe, [50, 100, 100])

# Define rules
rule1 = ctrl.Rule(temperature['cold'] & desired_temp['hot'], action['heat'])
rule2 = ctrl.Rule(temperature['comfortable'] & desired_temp['hot'], action['cool'])
rule3 = ctrl.Rule(temperature['hot'] & desired_temp['cold'], action['cool'])
rule4 = ctrl.Rule(temperature['comfortable'] & desired_temp['comfortable'], action['maintain'])
rule5 = ctrl.Rule(temperature['hot'] & desired_temp['comfortable'], action['cool'])

# Create a control system
action_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
action_simulation = ctrl.ControlSystemSimulation(action_ctrl)

# Input values for simulation
current_temperature = 30   # Current room temperature
target_temperature = 22     # Desired temperature

# Fuzzification of inputs
action_simulation.input['temperature'] = current_temperature
action_simulation.input['desired_temp'] = target_temperature

# Compute the output
action_simulation.compute()

# Output result
print(f"Action to take: {action_simulation.output['action']}%")
