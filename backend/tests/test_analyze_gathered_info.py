import unittest
from unittest.mock import patch
import os

# Adjust the import path based on your file structure
from backend.src.analyze_gathered_info import getAnalyzedReport

class TestGetAnalyzedReport(unittest.TestCase):

    @patch('backend.src.analyze_gathered_info.summarize_discussion')
    @patch('backend.src.analyze_gathered_info.analyze_sentiment')
    @patch('backend.src.analyze_gathered_info.identify_actionable_needs')
    def test_successful_analysis(self, mock_identify_actionable_needs, mock_analyze_sentiment, mock_summarize_discussion):
        # Mock return values for each function
        mock_summarize_discussion.return_value = "This is a summary of the discussion."
        mock_analyze_sentiment.return_value = "The sentiment is positive."
        mock_identify_actionable_needs.return_value = "Need more resources and better planning."

        # Sample discussions input
        discussions = [
            "This is a great initiative!",
            "However, we need more resources.",
            "Overall, good job!",
            "Can we get better planning next time?"
        ]

        # Call the function
        summary, sentiment, actionable_needs = getAnalyzedReport(discussions)

        # Assert the expected outputs
        self.assertEqual(summary, "This is a summary of the discussion.")
        self.assertEqual(sentiment, "The sentiment is positive.")
        self.assertEqual(actionable_needs, "Need more resources and better planning.")

        # Ensure the functions are called with the correct arguments
        mock_summarize_discussion.assert_called_once_with(discussions)
        mock_analyze_sentiment.assert_called_once_with(discussions)
        mock_identify_actionable_needs.assert_called_once_with(discussions)

    @patch('backend.src.analyze_gathered_info.summarize_discussion', side_effect=Exception("Failed to summarize discussion"))
    @patch('backend.src.analyze_gathered_info.analyze_sentiment', side_effect=Exception("Failed to analyze sentiment"))
    @patch('backend.src.analyze_gathered_info.identify_actionable_needs', side_effect=Exception("Failed to identify actionable needs"))
    def test_failure_case(self, mock_identify_actionable_needs, mock_analyze_sentiment, mock_summarize_discussion):
        # Sample discussions input
        discussions = [
            "This is a great initiative!",
            "However, we need more resources.",
            "Overall, good job!",
            "Can we get better planning next time?"
        ]

        # Assert that an exception is raised for each function
        with self.assertRaises(Exception) as context:
            getAnalyzedReport(discussions)
        
        self.assertTrue("Failed to summarize discussion" in str(context.exception))
