import requests
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
import os
from typing import List, Dict

# Load pre-trained Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Set the cache directory for transformers (for caching models and tokenizers)
os.environ['TRANSFORMERS_CACHE'] = 'backend/cache/models'

# Initialize Faiss index
DIMENSION = 768  # DIMENSIONality of the Sentence-BERT embeddings for 'all-MiniLM-L6-v2'
index = faiss.IndexFlatL2(DIMENSION)  # Using L2 distance for similarity

# Path for storing id_to_text dictionary
ID_TO_TEXT_PATH = 'id_to_text.pkl'

# Load id_to_text from disk if it exists
if os.path.exists(ID_TO_TEXT_PATH):
    with open(ID_TO_TEXT_PATH, 'rb') as f:
        id_to_text = pickle.load(f)
else:
    id_to_text = {}


def save_id_to_text():
    """Save the id_to_text dictionary to a file for persistence."""
    with open(ID_TO_TEXT_PATH, 'wb') as f:
        pickle.dump(id_to_text, f)


def fetch_wordpress_content(base_url: str) -> List[Dict]:
    """
    Fetches content (posts) from a WordPress site's REST API.

    Parameters:
    - base_url (str): The base URL of the WordPress site

    Returns:
    - List[Dict]: A list of posts with ID, title, and content
    """
    posts_endpoint = f"{base_url}/wp-json/wp/v2/posts"
    response = requests.get(posts_endpoint)
    if response.status_code == 200:
        posts = response.json()
        content_data = []
        for post in posts:
            content_data.append({
                "id": post["id"],
                "title": post["title"]["rendered"],
                "content": post["content"]["rendered"]
            })
        return content_data
    else:
        print(
            f"Failed to fetch posts from {base_url}. Status code: {response.status_code}")
        return []

# Check and pad the embedding if needed
def pad_embedding(embedding):
    if embedding.shape[1] < DIMENSION:
        padding = np.zeros(
            (1, DIMENSION - embedding.shape[1]), dtype=np.float32)
        embedding = np.hstack((embedding, padding))
    return embedding

def generate_embeddings(text: str):
    """
    Generates embeddings for a given text using Sentence-BERT model.

    Parameters:
    - text (str): The input text to be embedded

    Returns:
    - np.ndarray: The embedding as a numpy array
    """
    embedding = model.encode([text])
    # Check and pad the embedding if needed
    embedding = pad_embedding(embedding)

    return embedding


def update_embeddings_with_wordpress_content(base_url: str = None, context_texts: list = None):
    """
    Updates the embeddings for WordPress content, adding to the FAISS index.

    Parameters:
    - base_url (str): The base URL of the WordPress site to fetch content from
    """
    if context_texts:
        content_data = context_texts
    else:
        # Fetch WordPress content
        content_data = fetch_wordpress_content(base_url)

    if content_data:
        for item in content_data:
            # Combine title and content for embedding
            content_text = item["title"] + " " + item["content"]
            # Generate embedding
            embedding = generate_embeddings(content_text)

            # FOR DEBUGGING --------------------------------------

            # print(embedding.shape)

            # ----------------------------------------------------

            # Convert to numpy for Faiss storage
            # FAISS requires float32 dtype
            embedding_np = embedding.astype(np.float32)

            # Store in Faiss with the item's ID as a reference
            index.add(embedding_np)

            # Map the ID to its text (title and content)
            id_to_text[item["id"]] = content_text

            print(
                f"Added embedding for content ID {item['id']} - Title: {item['title']}")

        # Save the updated id_to_text dictionary for persistence
        # save_id_to_text()
    else:
        print("No content fetched to update embeddings.")


def query_index(query: str, top_k: int = 5):
    """
    Queries the FAISS index to find the top-k most similar documents to the input query.

    Parameters:
    - query (str): The user query to be embedded and searched in the index
    - top_k (int): The number of top results to return

    Returns:
    - List[Tuple[str, float]]: A list of tuples with document text and similarity score
    """
    # Generate the embedding for the query
    query_embedding = generate_embeddings(query).astype(
        np.float32)  # FAISS requires float32 dtype
    
    # Check and pad the embedding if needed
    query_embedding = pad_embedding(query_embedding)
    
    # Perform the search in the FAISS index
    distances, indices = index.search(query_embedding, top_k)
    # Collect the results, using the indices to retrieve the document content
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx != -1:  # Ensure the index is valid
            # Retrieve document text from id_to_text with the index
            results.append((id_to_text.get(idx, "Content not found"), dist))

    return results
