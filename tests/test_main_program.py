"""Tests for CLI input helpers."""

import unittest

from src.main_program import _validate_city_name


class ValidateCityNameTest(unittest.TestCase):
    def test_accepts_letters_spaces_and_configured_extra_characters(self):
        extra_chars = "-'. "

        self.assertTrue(_validate_city_name("new york", extra_chars))
        self.assertTrue(_validate_city_name("saint-jean", extra_chars))
        self.assertTrue(_validate_city_name("o'fallon", extra_chars))

    def test_rejects_empty_or_unconfigured_characters(self):
        extra_chars = "-'. "

        self.assertFalse(_validate_city_name("", extra_chars))
        self.assertFalse(_validate_city_name("paris!", extra_chars))
        self.assertFalse(_validate_city_name("tokyo2", extra_chars))


if __name__ == "__main__":
    unittest.main()
