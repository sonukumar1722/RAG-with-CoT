import unittest
from unittest.mock import patch
import numpy as np
from embedding_service import fetch_wordpress_content, generate_embeddings, update_embeddings_with_wordpress_content, query_index

class TestEmbeddingService(unittest.TestCase):
    
    def setUp(self):
        """
        Setup necessary environment before each test
        """
        self.test_url = "https://time.com"  # Use a placeholder URL for testing
        self.test_query = "test query"
        
    @patch('embedding_service.requests.get')
    def test_fetch_wordpress_content(self, mock_get):
        """
        Test fetching WordPress content via the REST API
        """
        mock_data = [
            {"id": 1, "title": {"rendered": "Test Title 1"}, "content": {"rendered": "Test content 1"}},
            {"id": 2, "title": {"rendered": "Test Title 2"}, "content": {"rendered": "Test content 2"}},
            {"id": 3, "title": {"rendered": "Test Title 3"}, "content": {"rendered": "Test content 3"}},
            {"id": 4, "title": {"rendered": "Test Title 4"}, "content": {"rendered": "Test content 4"}}
        ]
        
        # Mock the GET request to return the test data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_data
        
        result = fetch_wordpress_content(self.test_url)
        
        # Assertions
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['title'], "Test Title 1")
        self.assertEqual(result[0]['content'], "Test content 1")
        
    def test_generate_embeddings(self):
        """
        Test embedding generation from text using Sentence-BERT
        """
        text = "Hello, world!"
        embeddings = generate_embeddings(text)
        
        # Check if embeddings are a numpy array and have the expected shape
        self.assertIsInstance(embeddings, np.ndarray)
        self.assertEqual(embeddings.shape[0], 1)  # One sentence should result in one embedding
        # self.assertEqual(embeddings.shape[1], 768)  # Should match Sentence-BERT's dimensionality
    
    @patch('embedding_service.fetch_wordpress_content')
    @patch('embedding_service.generate_embeddings')
    def test_update_embeddings_with_wordpress_content(self, mock_generate_embeddings, mock_fetch_content):
        """
        Test updating embeddings with WordPress content and storing in Faiss index
        """
        mock_content_data = [
            {"id": 1, "title": "Test Title 1", "content": "Test content 1"},
            {"id": 2, "title": "Test Title 2", "content": "Test content 2"},
            {"id": 3, "title": "Test Title 3", "content": "Test content 3"},
            {"id": 4, "title": "Test Title 4", "content": "Test content 4"}
        ]
        
        mock_generate_embeddings.return_value = np.random.rand(1, 768)  # Mock embeddings
        mock_fetch_content.return_value = mock_content_data
        
        # Update embeddings with the mock content data
        update_embeddings_with_wordpress_content(self.test_url)
        
        # Assertions
        mock_generate_embeddings.assert_called()
        self.assertEqual(len(mock_content_data), 4)  # Check if two content entries were processed
        self.assertEqual(mock_generate_embeddings.call_count, 4)  # Ensure embeddings were generated for both entries
    
    @patch('embedding_service.index.search')
    def test_query_index(self, mock_search):
        """
        Test querying the FAISS index and retrieving results
        """
        # Mock the search result
        mock_search.return_value = (np.array([[0.1, 0.2, 0.3, 0.4]]), np.array([[1, 2, 3, 4]]))  # Mock distance and index
        
        # Sample query
        query = "Test query"
        results = query_index(query, top_k=2)
        
        # Assertions
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0][0], "Test Title 1 Test content 1")  # Ensure the correct content is returned
        self.assertAlmostEqual(results[0][1], 0.1, places=2)  # Ensure the correct similarity score is returned

if __name__ == "__main__":
    unittest.main()