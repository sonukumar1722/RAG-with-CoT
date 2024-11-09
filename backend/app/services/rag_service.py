from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration
from embedding_service import query_index, generate_embeddings
from typing import List, Tuple
import torch
import os
import numpy as np

DIMENSION = 768

# Set the cache directory for transformers (for caching models and tokenizers)
os.environ['TRANSFORMERS_CACHE'] = 'backend/cache/models'

# Initialize the RAG model, retriever, and tokenizer
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
retriever = RagRetriever.from_pretrained(
    "facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True, trust_remote_code=True)
model = RagTokenForGeneration.from_pretrained(
    "facebook/rag-token-nq", retriever=retriever)


def calculate_doc_scores(query: str, retrieved_docs: list) -> torch.Tensor:
    """
    Calculate document scores (doc_scores) based on cosine similarity between query 
    and retrieved documents.

    Parameters:
    - query (str): The user query
    - retrieved_docs (list): List of retrieved documents (text)

    Returns:
    - torch.Tensor: Document scores for each retrieved document
    """
    # Generate embeddings for the query
    # Assuming output shape: (embedding_dim,)
    query_embedding = generate_embeddings(query)
    query_embedding = torch.tensor(query_embedding)  # Shape: (1, embedding_dim)

    # Generate embeddings for each retrieved document
    doc_embeddings = torch.tensor([generate_embeddings(doc_text) for doc_text in retrieved_docs]).squeeze(1)  # Shape: (num_docs, embedding_dim)

    # For debugging --------------------------------------------------------------------------------

    print(query_embedding.shape)
    print(doc_embeddings.shape)

    # ----------------------------------------------------------------------------------------------

    # Calculate cosine similarity scores as document scores
    query_norm = torch.nn.functional.normalize(query_embedding, p=2, dim=1)
    doc_norms = torch.nn.functional.normalize(doc_embeddings, p=2, dim=1)
    doc_scores = torch.matmul(query_norm, doc_norms.T).squeeze(
        0).unsqueeze(0)  # Shape: (num_docs,)
    return doc_scores


def generate_response_with_cot(query: str, top_k: int = 5) -> str:
    """
    Generates a response to a query using Retrieval-Augmented Generation (RAG) 
    with a Chain of Thought approach.

    Parameters:
    - query (str): The user query
    - top_k (int): Number of top documents to retrieve for context

    Returns:
    - str: The generated response
    """
    # Step 1: Retrieve relevant documents
    retrieved_docs = query_index(query, top_k)

    print(query) # for debugging
    print(retrieved_docs) # for debugging

    # Step 2: Prepare context from retrieved documents
    context_docs = [doc for doc, _ in retrieved_docs]

    # context_texts = " ".join(context_docs)

    # Calculate document scores for relevance
    doc_scores = calculate_doc_scores(query, context_docs)

    # Step 3: Apply Chain of Thought
    # cot_prompts = apply_chain_of_thought(context_docs)

    context_tokens = tokenizer(context_docs, return_tensors="pt",
                               padding=True, truncation=True, max_length=DIMENSION)

    # Step 4: Tokenize and generate response with CoT prompt
    inputs = tokenizer(query, return_tensors="pt",
                       padding=True, truncation=True, max_length=DIMENSION)
    
    print("context_tokens", context_tokens)
    print("inputs embeddings", inputs)


    # Generate output with tokenized context
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        context_input_ids=context_tokens["input_ids"],
        attention_mask=inputs["attention_mask"],
        context_attention_mask=context_tokens["attention_mask"],
        doc_scores=doc_scores,
        max_new_tokens=100,
        temperature=0.7,
        top_k= top_k,
        top_p=0.9,
        do_sample=True,
        n_docs = len(context_docs)
    )
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return response


def apply_chain_of_thought(context: str) -> str:
    """
    Applies a Chain of Thought reasoning strategy to create a coherent prompt 
    for the model generation.

    Parameters:
    - query (str): The user query
    - context (str): Relevant document context

    Returns:
    - str: Formatted prompt for RAG model input
    """
    # Create a detailed prompt with structured reasoning
    return "".join(
        f"Context: {context}\n\n"
        "Let's think step-by-step to answer this query based on the information provided.\nIdentify relevant points from the context and build a coherent response."
    )
