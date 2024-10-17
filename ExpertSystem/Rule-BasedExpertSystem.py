class RuleBasedExpertSystem:
    def __init__(self):
        # Knowledge base containing rules
        self.rules = [
            ("fever", "flu"),
            ("cough", "flu"),
            ("sore throat", "flu"),
            ("shortness_of_breath", "asthma"),
            ("headache", "migraine"),
            ("nausea", "migraine"),
            ("fatigue", "flu"),
            ("muscle_pain", "flu"),
        ]
        # Facts about the patient
        self.facts = set()

    def add_symptom(self, symptom):
        """Add a symptom to the set of facts."""
        self.facts.add(symptom)

    def diagnose(self):
        """Diagnose based on the facts and rules."""
        diagnoses = set()
        for symptom, diagnosis in self.rules:
            if symptom in self.facts:
                diagnoses.add(diagnosis)
        return diagnoses

# Example usage
expert_system = RuleBasedExpertSystem()
expert_system.add_symptom("fever")
expert_system.add_symptom("cough")

diagnosis = expert_system.diagnose()
print("Possible diagnoses:", diagnosis)
