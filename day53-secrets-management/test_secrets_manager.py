import os
import unittest
from unittest.mock import patch

from secrets_manager import get_secret, secret_is_configured


class TestSecretsManager(unittest.TestCase):
    @patch.dict(os.environ, {"DATABASE_PASSWORD": "example-only"}, clear=True)
    def test_reads_environment_variable(self):
        self.assertEqual(get_secret("DATABASE_PASSWORD"), "example-only")

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_secret_returns_none(self):
        self.assertIsNone(get_secret("DATABASE_PASSWORD"))

    @patch.dict(os.environ, {"API_KEY": "example-only"}, clear=True)
    def test_configured_secret_check(self):
        self.assertTrue(secret_is_configured("API_KEY"))

    @patch.dict(os.environ, {}, clear=True)
    def test_unconfigured_secret_check(self):
        self.assertFalse(secret_is_configured("API_KEY"))

    def test_invalid_secret_name_is_rejected(self):
        with self.assertRaises(ValueError):
            get_secret("DATABASE-PASSWORD")


if __name__ == "__main__":
    unittest.main()
