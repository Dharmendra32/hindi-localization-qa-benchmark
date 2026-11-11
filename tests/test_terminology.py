
import unittest

from check_terminology import (
    source_contains_term,
    translation_contains_term
)


class TestTerminologyChecker(unittest.TestCase):

    def test_english_term_found(self):
        self.assertTrue(
            source_contains_term(
                "Sign in to your account.",
                "account"
            )
        )

    def test_english_term_is_case_insensitive(self):
        self.assertTrue(
            source_contains_term(
                "Open the SETTINGS page.",
                "settings"
            )
        )

    def test_english_substring_not_accepted(self):
        self.assertFalse(
            source_contains_term(
                "Change your accountsettings.",
                "settings"
            )
        )

    def test_approved_hindi_term_accepted(self):
        self.assertTrue(
            translation_contains_term(
                "अपने खाते में साइन इन करें।",
                ["खाता", "खाते"]
            )
        )

    def test_unapproved_hindi_term_rejected(self):
        self.assertFalse(
            translation_contains_term(
                "हम आपका अकाउंट नहीं खोज सके।",
                ["खाता", "खाते"]
            )
        )


if __name__ == "__main__":
    unittest.main()
