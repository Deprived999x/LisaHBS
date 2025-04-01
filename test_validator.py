# test_validator.py - Unit Tests for Lisa Validator Engine

import unittest
from lisa_validator_engine import Validator, CharacterState, TaxonomyLoader

class TestValidator(unittest.TestCase):

    def setUp(self):
        # Setup a simple taxonomy for testing
        self.taxonomy = {
            "Gender": [
                {"Key": "A", "Option": "Male", "Visual Description": "Short description", "As Seen In": "Example"},
                {"Key": "B", "Option": "Female", "Visual Description": "Short description", "As Seen In": "Example"}
            ],
            "Visual Heritage": [
                {"Key": "A", "Option": "West African", "Visual Description": "Short description", "As Seen In": "Example"},
                {"Key": "B", "Option": "East Asian", "Visual Description": "Short description", "As Seen In": "Example"}
            ]
        }
        self.loader = TaxonomyLoader(self.taxonomy)
        self.validator = Validator(self.loader.taxonomy)
        self.state = CharacterState()

    def test_valid_option(self):
        # Test for valid options
        self.state.set_trait("Gender", "Male")
        self.assertTrue(self.validator.is_valid_option("Gender", "Male"))
        self.assertFalse(self.validator.is_valid_option("Gender", "Non-binary"))

    def test_invalid_option(self):
        # Test for invalid options
        self.state.set_trait("Visual Heritage", "West African")
        self.assertTrue(self.validator.is_valid_option("Visual Heritage", "West African"))
        self.assertFalse(self.validator.is_valid_option("Visual Heritage", "Native American"))

    def test_mutual_exclusion(self):
        # Test mutual exclusion rule
        exclusion_rules = {
            "Gender": ["Female"],
            "Visual Heritage": ["East Asian"]
        }
        self.state.set_trait("Gender", "Female")
        self.state.set_trait("Visual Heritage", "East Asian")
        violations = self.validator.enforce_mutual_exclusion(self.state, exclusion_rules)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0], ("Gender", "Visual Heritage"))

    def test_valid_full_state(self):
        # Test for full state validation
        self.state.set_trait("Gender", "Female")
        self.state.set_trait("Visual Heritage", "East Asian")
        self.assertTrue(self.validator.validate_full_state(self.state))

    def test_invalid_full_state(self):
        # Test for invalid full state
        self.state.set_trait("Gender", "Unknown")
        self.state.set_trait("Visual Heritage", "East Asian")
        self.assertFalse(self.validator.validate_full_state(self.state))

if __name__ == "__main__":
    unittest.main()
