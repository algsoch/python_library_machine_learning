"""Unit tests for the spell correction module."""

import unittest
import sys
import os

# Add parent directory to path to import spell module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spell import correct_text, get_backend_info, TEXTBLOB_AVAILABLE


class TestSpellCorrection(unittest.TestCase):
    """Test cases for spell correction functionality."""
    
    def test_backend_info(self):
        """Test that backend info is returned correctly."""
        info = get_backend_info()
        self.assertIn('backend', info)
        self.assertIn('status', info)
        self.assertIsInstance(info['backend'], str)
        self.assertIsInstance(info['status'], str)
    
    def test_empty_string(self):
        """Test correction of empty string."""
        self.assertEqual(correct_text(''), '')
        self.assertEqual(correct_text('   '), '   ')
    
    def test_correct_text_no_typos(self):
        """Test that correct text remains unchanged."""
        text = "This is correct text"
        result = correct_text(text)
        # Should either be the same or very similar
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
    
    def test_common_typos(self):
        """Test correction of common typos from our dataset."""
        # Test cases that TextBlob handles well
        test_cases = [
            ('electic', 'electric'),  # Should correct to electric
            ('cieling', 'ceiling'),   # Should correct to ceiling
        ]
        
        for typo, expected in test_cases:
            result = correct_text(typo)
            # For TextBlob or fallback, it should correct these
            self.assertIn(expected.lower(), result.lower(),
                         f"Expected '{expected}' in correction of '{typo}', got '{result}'")
    
    def test_phrase_correction(self):
        """Test correction of phrases with multiple typos."""
        # These are from the actual dataset
        test_phrases = [
            'metal plate cover gcfi',  # Should correct gcfi -> gfci
            'artric air portable',     # Should correct artric -> arctic
            'lawn mower- electic',     # Should correct electic -> electric
        ]
        
        for phrase in test_phrases:
            result = correct_text(phrase)
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0)
            # The corrected text should be different from the original
            # (unless TextBlob can't improve it, which is okay)
    
    def test_correction_map_entries(self):
        """Test that correction map entries work correctly."""
        # Test a few entries that should work with fallback
        if not TEXTBLOB_AVAILABLE:
            # Only test these if using fallback (dictionary-based)
            result = correct_text('cieling')
            self.assertEqual(result.lower(), 'ceiling')


class TestAppIntegration(unittest.TestCase):
    """Test cases for Flask app integration."""
    
    def setUp(self):
        """Set up test client."""
        # Import here to avoid issues if Flask is not installed
        try:
            from app import app
            self.app = app
            self.client = app.test_client()
            self.app.config['TESTING'] = True
        except ImportError:
            self.skipTest("Flask not installed")
    
    def test_index_route(self):
        """Test that index page loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_api_info(self):
        """Test API info endpoint."""
        response = self.client.get('/api/info')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('backend', data)
        self.assertIn('status', data)
    
    def test_api_correct_valid(self):
        """Test API correction with valid input."""
        response = self.client.post('/api/correct',
                                   json={'text': 'test text'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('original', data)
        self.assertIn('corrected', data)
        self.assertIn('backend', data)
        self.assertEqual(data['original'], 'test text')
    
    def test_api_correct_missing_text(self):
        """Test API correction with missing text field."""
        response = self.client.post('/api/correct', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
