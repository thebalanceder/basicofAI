class Frame:
    def __init__(self, name):
        self.name = name
        self.slots = {}
    
    def add_slot(self, slot_name, value):
        self.slots[slot_name] = value
    
    def get_slot(self, slot_name):
        return self.slots.get(slot_name, None)

class VehicleIssueFrame(Frame):
    def __init__(self, name):
        super().__init__(name)
        self.add_slot("symptoms", [])
        self.add_slot("solution", "")

    def add_symptom(self, symptom):
        symptoms = self.get_slot("symptoms")
        symptoms.append(symptom)
        self.add_slot("symptoms", symptoms)

class VehicleDiagnosisExpertSystem:
    def __init__(self):
        self.issues = {}
    
    def add_issue(self, issue_frame):
        self.issues[issue_frame.name] = issue_frame
    
    def diagnose(self, observed_symptoms):
        possible_issues = []
        for issue in self.issues.values():
            if all(symptom in issue.get_slot("symptoms") for symptom in observed_symptoms):
                possible_issues.append(issue.name)
                print(f"Suggested solution for {issue.name}: {issue.get_slot('solution')}")
        return possible_issues

# Example usage
expert_system = VehicleDiagnosisExpertSystem()

# Creating vehicle issue frames
issue1 = VehicleIssueFrame("Dead Battery")
issue1.add_symptom("engine won't start")
issue1.add_symptom("clicking sound")
issue1.add_slot("solution", "Check battery connections and replace if necessary.")

issue2 = VehicleIssueFrame("Flat Tire")
issue2.add_symptom("tire pressure warning light")
issue2.add_symptom("visible damage on tire")
issue2.add_slot("solution", "Inspect tire and replace if damaged.")

# Adding issues to the expert system
expert_system.add_issue(issue1)
expert_system.add_issue(issue2)

# Diagnosing based on observed symptoms
observed_symptoms = ["engine won't start", "clicking sound"]
diagnosis = expert_system.diagnose(observed_symptoms)

print("Possible issues diagnosed:", diagnosis)
