import unittest
from unittest.mock import patch, Mock
from regular import PhoneNumberExtractor


class TestPhoneNumberExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = PhoneNumberExtractor()

    # --- extract_phone_numbers ---
    def test_extract_phone_numbers_basic(self):
        text = "Позвоните +7 (999) 123-45-67 или 8 (999) 1234567."
        result = self.extractor.extract_phone_numbers(text)

        self.assertIn("+7 (999) 123-45-67", result)
        # альтернативный формат должен быть найден как есть
        self.assertIn("8 (999) 1234567", result)

    def test_extract_multiple_formats(self):
        text = "Телефоны: 9991234567, +7(999)1234567, 8-999-123-45-67"
        result = self.extractor.extract_phone_numbers(text)

        self.assertTrue(any("+7 (999) 123-45-67" in p for p in result))
        self.assertIn("9991234567", result)
        self.assertIn("+7(999)1234567", result)

    # --- validate_phone_number ---
    def test_validate_phone_number(self):
        self.assertTrue(self.extractor.validate_phone_number("+7 (999) 123-45-67"))
        self.assertTrue(self.extractor.validate_phone_number("8 (999) 1234567"))
        self.assertTrue(self.extractor.validate_phone_number("79991234567"))
        self.assertTrue(self.extractor.validate_phone_number("9991234567"))

        self.assertFalse(self.extractor.validate_phone_number("+7999123"))
        self.assertFalse(self.extractor.validate_phone_number("12345"))
        self.assertFalse(self.extractor.validate_phone_number("+1 999 1234567"))

    # --- normalize_phone ---
    def test_normalize_phone(self):
        self.assertEqual(
            self.extractor.normalize_phone("+7 (999) 123-45-67"),
            "+79991234567"
        )
        self.assertEqual(
            self.extractor.normalize_phone("8 (999) 123-45-67"),
            "+79991234567"
        )
        self.assertEqual(
            self.extractor.normalize_phone("9991234567"),
            "+79991234567"
        )

        # неверный формат — вернуть как есть
        self.assertEqual(
            self.extractor.normalize_phone("+1 23 45"),
            "+1 23 45"
        )

    # --- get_phones_from_url ---
    @patch("regular.requests.get")
    def test_get_phones_from_url(self, mock_get):
        mock_response = Mock()
        mock_response.text = "Наш телефон: +7 (999) 111-22-33"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = self.extractor.get_phones_from_url("http://example.com")

        self.assertEqual(result, ["+7 (999) 111-22-33"])
        mock_get.assert_called_once_with("http://example.com", timeout=10)

    @patch("regular.requests.get")
    def test_get_phones_from_url_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")

        result = self.extractor.get_phones_from_url("http://badurl")

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
