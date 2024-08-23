import unittest
from unittest.mock import patch, Mock
import os
from backend.src.fetch_reddit_discussion import generate_search_prompt
from backend.src.fetch_reddit_discussion import fetch_comments_for_topic


class TestGenerateSearchPrompt(unittest.TestCase):

    @patch('backend.src.fetch_reddit_discussion.requests.post')
    def test_missing_openrouter_api_key(self, mock_post):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(EnvironmentError) as context:
                generate_search_prompt('Test Topic')
            self.assertIn("Missing required environment variable: OPENROUTER_API_KEY", str(context.exception))

    @patch('backend.src.fetch_reddit_discussion.requests.post')
    def test_successful_api_call(self, mock_post):
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'dummy_key'}):
            # Mock the response from the API
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'choices': [
                    {'message': {'content': '{"query": "search query for Test Topic"}'}}
                ]
            }
            mock_post.return_value = mock_response

            query = generate_search_prompt('Test Topic')
            self.assertEqual(query, "search query for Test Topic")

    @patch('backend.src.fetch_reddit_discussion.requests.post')
    def test_invalid_json_response(self, mock_post):
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'dummy_key'}):
            # Mock a response with invalid JSON
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'choices': [
                    {'message': {'content': 'Invalid JSON'}}
                ]
            }
            mock_post.return_value = mock_response

            with self.assertRaises(RuntimeError) as context:
                generate_search_prompt('Test Topic')
            self.assertIn("Error processing the response: invalid JSON or missing 'query' field", str(context.exception))

    @patch('backend.src.fetch_reddit_discussion.requests.post')
    def test_api_call_failure(self, mock_post):
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'dummy_key'}):
            # Mock a failed API call
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            mock_post.return_value = mock_response

            with self.assertRaises(RuntimeError) as context:
                generate_search_prompt('Test Topic')
            self.assertIn("API call failed with status code 500", str(context.exception))



class TestFetchCommentsFromReddit(unittest.TestCase):

    # issue here, as mock is not able to loop saying not subscriptable

    # @patch('backend.src.fetch_reddit_discussion.configure_reddit_api')
    # def test_fetch_comments_from_reddit(self, mock_reddit_api):
    #     """Test fetching comments for a specific topic from a predefined subreddit ('all')."""
        
    #     # Mock the Reddit API
    #     mock_reddit = Mock()
    #     mock_subreddit = Mock(displayname='all')
    #     mock_reddit.subreddit.return_value = mock_subreddit
        
    #     # Predefined list of dictionaries for comments
    #     predefined_comments = [
    #         {
    #             "body": "Test Comment 0",
    #             "author": Mock(name="TestAuthor0"),
    #             "score": 10,
    #             "created_utc": (datetime.now() - timedelta(hours=10)).timestamp()
    #         },
    #         {
    #             "body": "Test Comment 1",
    #             "author": Mock(name="TestAuthor1"),
    #             "score": 11,
    #             "created_utc": (datetime.now() - timedelta(hours=9)).timestamp()
    #         },
    #         {
    #             "body": "Test Comment 2",
    #             "author": Mock(name="TestAuthor2"),
    #             "score": 12,
    #             "created_utc": (datetime.now() - timedelta(hours=8)).timestamp()
    #         },
    #         {
    #             "body": "Test Comment 3",
    #             "author": Mock(name="TestAuthor3"),
    #             "score": 13,
    #             "created_utc": (datetime.now() - timedelta(hours=7)).timestamp()
    #         },
    #         {
    #             "body": "Test Comment 4",
    #             "author": Mock(name="TestAuthor4"),
    #             "score": 14,
    #             "created_utc": (datetime.now() - timedelta(hours=6)).timestamp()
    #         }
    #     ]

    #     # Configure mock submission
    #     mock_submission = Mock()
    #     mock_submission.title = "Test Post Title"
    #     mock_submission.id = "abc123"
    #     mock_submission.created_utc = (datetime.now() - timedelta(days=1)).timestamp()
    #     mock_submission.subreddit = "all"
        
    #     # Ensure submission.comments.list() returns the predefined list of dictionaries
    #     mock_submission.comments.list.return_value = predefined_comments

    #     # Mock the search method to return our mock submission
    #     mock_subreddit.search.return_value = [mock_submission]

    #     # Set the mock Reddit API to return our mock subreddit
    #     mock_reddit_api.return_value = mock_reddit

    #     # Call the function
    #     topic = "Test Topic"
    #     city_name = "Test City"
    #     limit = 5
    #     max_age_days = 2

    #     # Fetch comments for the topic
    #     comments = fetch_comments_for_topic(topic, city_name, limit=limit, max_age_days=max_age_days)

    #     # Assertions
    #     self.assertEqual(len(comments), 5)
    #     self.assertEqual(comments[0]['CommentBody'], "Test Comment 0")
    #     self.assertEqual(comments[0]['Author'].name, "TestAuthor0")
    #     self.assertEqual(comments[0]['Score'], 10)
    #     self.assertEqual(comments[0]['Subreddit'], "r/all")


    @patch('backend.src.fetch_reddit_discussion.configure_reddit_api')
    def test_fetch_comments_with_no_results(self, mock_reddit_api):
        """Test that no comments are returned when there are no search results."""
        
        # Mock the Reddit API
        mock_reddit = Mock()
        mock_subreddit = Mock(displayname='all')
        mock_reddit.subreddit.return_value = mock_subreddit

        # No results for both relevance and hot
        mock_subreddit.search.side_effect = [[], []]

        # Set the mock Reddit API to return our mock subreddit
        mock_reddit_api.return_value = mock_reddit

        # Call the function
        topic = "Test Topic"
        city_name = "Test City"
        limit = 5
        max_age_days = 2

        # Fetch comments for the topic
        comments = fetch_comments_for_topic(topic, city_name, limit=limit, max_age_days=max_age_days)

        # Assertions
        self.assertEqual(len(comments), 0)  # Expecting no comments since no results were found


    @patch('backend.src.fetch_reddit_discussion.configure_reddit_api')
    def test_fetch_comments_with_api_failure(self, mock_reddit_api):
        """Test that an exception is handled gracefully when there is an API failure."""
        
        # Mock the Reddit API
        mock_reddit = Mock()
        mock_subreddit = Mock(displayname='all')
        mock_reddit.subreddit.return_value = mock_subreddit
        
        # Simulate an exception when trying to search
        mock_subreddit.search.side_effect = Exception("Reddit API failure")

        # Set the mock Reddit API to return our mock subreddit
        mock_reddit_api.return_value = mock_reddit

        # Call the function
        topic = "Test Topic"
        city_name = "Test City"
        limit = 5
        max_age_days = 2

        # Fetch comments for the topic and expect it to handle the failure gracefully
        try:
            comments = fetch_comments_for_topic(topic, city_name, limit=limit, max_age_days=max_age_days)
            self.assertEqual(len(comments), 0)  # Expecting no comments due to API failure
        except Exception as e:
            self.fail(f"fetch_comments_for_topic raised an exception: {e}")


