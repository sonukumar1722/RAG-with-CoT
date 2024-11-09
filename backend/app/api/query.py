from fastapi import APIRouter
from app.services import rag_service, cot_service

router = APIRouter()

@router.post("/process_query")
async def process_query(user_query: str):
    # Step 1: Generate a response using RAG model
    initial_response = rag_service.generate_response(user_query)
    
    # Step 2: Process response with Chain of Thought (CoT)
    final_response = cot_service.process_cot(initial_response, user_query)
    
    return {"response": final_response}