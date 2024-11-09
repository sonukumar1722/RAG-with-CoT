import unittest
from unittest.mock import patch, MagicMock
from embedding_service import update_embeddings_with_wordpress_content
from rag_service import generate_response_with_cot, apply_chain_of_thought


class TestRAGService(unittest.TestCase):
    @patch('rag_service.query_index')
    def test_generate_response_with_cot(self, mock_query_index):
        # Mock the FAISS retrieval function to return example documents
        mock_query_index.return_value = [
            ("the Earth is around ball of approximately 3,959 miles (6,371 kilometers) in diameter", 0.8),
            ("The Earth's equatorial diameter is approximately 24,901 miles (40,075 kilometers).", 0.7),
            ("The Earth's polar diameter is approximately 24,901 miles (40,075 kilometers).", 0.6),
            ("The Earth's circumference at the equator is approximately 40,075 miles (63,710 kilometers).", 0.5),
            ("The Earth's atmosphere is composed primarily of nitrogen, oxygen, and trace amounts of other gases.", 0.4)
        ]

        # Define a sample query and run the RAG model
        query = "What is the radius of earth?"

        # Manually adding contexts in the faiss DB
        context_texts = [
            {"id": 100, "title": "Test Title 1",
                "content": "the Earth is around ball of approximately 3,959 miles (6,371 kilometers) in diameter"},
            {"id": 200, "title": "Test Title 2",
                "content": "The Earth's equatorial diameter is approximately 24,901 miles (40,075 kilometers)."},
            {"id": 300, "title": "Test Title 3",
                "content": "The Earth's polar diameter is approximately 24,901 miles (40,075 kilometers)."},
            {"id": 400, "title": "Test Title 4",
                "content": "The Earth's circumference at the equator is approximately 40,075 miles (63,710 kilometers)."},
            {"id": 500, "title": "Test Title 5",
                "content": "The Earth's atmosphere is composed primarily of nitrogen, oxygen, and trace amounts of other gases."}
        ]
        update_embeddings_with_wordpress_content(context_texts=context_texts)

        # Run the response generation
        response = generate_response_with_cot(query)

        # Assertions to ensure response is not empty and includes context
        print(f"Generated Response: {response}")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_apply_chain_of_thought(self):
        # Test the Chain of Thought prompt formatting
        context = "This is a detailed explanation of the process and its steps."

        # Generate the CoT prompt
        cot_prompt = apply_chain_of_thought(context)

        # Assertions to check the prompt structure
        self.assertIn("Context:", cot_prompt)
        self.assertIn("Let's think step-by-step", cot_prompt)
        # print(f"Chain of Thought Prompt: {cot_prompt}")

    def test_model_generation_integration(self):
        # Define a sample query and run the RAG model
        query = "What is the color of sun?"
        # Manually adding contexts in the faiss DB
        context_texts = [
            {"id": 10, "title": "Test Title 1",
                "content": "The sun is a yellow, hot, glowing ball of plasma that gives off light."},
            {"id": 20, "title": "Test Title 2",
                "content": "The sun's color depends on its temperature and composition."},
            {"id": 30, "title": "Test Title 3",
                "content": "The sun emits a broad spectrum of light, including ultraviolet, visible light, and infrared light."},
            {"id": 40, "title": "Test Title 4",
                "content": "The sun's temperature varies throughout its day and night."},
            {"id": 50, "title": "Test Title 5",
                "content": "The sun's light also provides heat and energy for life on Earth."}
        ]

        update_embeddings_with_wordpress_content(context_texts=context_texts)

        response = generate_response_with_cot(query)

        # Check the response format
        print(f"Model Integration Response: {response}")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)


if __name__ == "__main__":
    unittest.main()
