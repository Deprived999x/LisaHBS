# Lisa_Validator_Engine.py - Core Validator Logic for HBS v005

import json
from typing import Dict, List

class TaxonomyLoader:
    def __init__(self, taxonomy_file: str):
        self.taxonomy = self.load_taxonomy(taxonomy_file)

    def load_taxonomy(self, path: str) -> Dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)  # assumes a converted JSON version of hbs-taxonomy-v005

class CharacterState:
    def __init__(self):
        self.traits = {}

    def set_trait(self, key: str, value: str):
        self.traits[key] = value

    def get_trait(self, key: str) -> str:
        return self.traits.get(key, None)

    def to_json(self):
        return json.dumps(self.traits, indent=2)

class Validator:
    def __init__(self, taxonomy: Dict):
        self.taxonomy = taxonomy

    def is_valid_option(self, trait_category: str, option: str) -> bool:
        options = self.taxonomy.get(trait_category, [])
        return any(opt["Option"] == option for opt in options)

    def get_valid_keys(self, trait_category: str) -> List[str]:
        return [opt["Key"] for opt in self.taxonomy.get(trait_category, [])]

    def enforce_mutual_exclusion(self, state: CharacterState, exclusion_rules: Dict[str, List[str]]) -> List[str]:
        violations = []
        for trait_a, excluded in exclusion_rules.items():
            selected = state.get_trait(trait_a)
            for trait_b in excluded:
                if state.get_trait(trait_b):
                    violations.append((trait_a, trait_b))
        return violations

    def validate_full_state(self, state: CharacterState) -> bool:
        for trait, value in state.traits.items():
            if not self.is_valid_option(trait, value):
                return False
        return True

# Example Usage
if __name__ == "__main__":
    loader = TaxonomyLoader("taxonomy.json")  # This must be a JSON version of hbs-taxonomy-v005
    validator = Validator(loader.taxonomy)
    state = CharacterState()

    # Simulate character creation
    state.set_trait("Gender", "Identify as female")
    state.set_trait("Visual Heritage", "East Asian Heritage")

    if validator.validate_full_state(state):
        print("Character state is valid.")
        print(state.to_json())
    else:
        print("Invalid trait(s) detected.")
