from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import database, model
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from app.agent.agent import invoke_graph_agent_for_extraction

app = FastAPI(
    title="Healthcare CRM API",
    description="AI-augmented API for logging HCP interactions"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only — allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ FIX: Define the missing AgentResponse model
class AgentResponse(BaseModel):
    response: str

class AgentRequest(BaseModel):
    message: str

# This is the Pydantic model for the data coming from the agent
class InteractionData(BaseModel):
    hcp_name: str
    date_of_interaction: date
    key_discussion_points: str
    products_discussed: Optional[List[str]] = None
    follow_up_needed: bool

# This is the model for the data being sent to the /save endpoint
class InteractionSaveRequest(InteractionData):
    original_message: str


@app.post("/agent/invoke", response_model=AgentResponse)
def invoke_agent(request: AgentRequest):
    try:
        llm = get_llm()
        ai_response = llm.invoke(request.message)
        return {"response": ai_response.content}
    except Exception as e:
        print(f"❌ Error in invoke_agent: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response from LLM")


@app.post("/agent/invoke/graph")
def invoke_graph_agent(request: AgentRequest):
    """
    This endpoint now directly calls the extraction function.
    """
    # ✅ Call the new function
    graph_data = invoke_graph_agent_for_extraction(request.message)
    return graph_data


@app.post("/interactions/save")
def save_interaction(log: InteractionSaveRequest, db: Session = Depends(database.get_db)):
    """
    This endpoint now correctly handles the list of products.
    """
    try:
        # Convert the Pydantic model to a dictionary
        log_data = log.dict()

        # ✅ Convert the list of products to a comma-separated string for DB storage
        if log_data.get("products_discussed"):
            log_data["products_discussed"] = ", ".join(log_data["products_discussed"])
        else:
            log_data["products_discussed"] = None # Ensure it's null if empty
        
        # The date is already a valid 'date' object from Pydantic
        
        db_obj = model.InteractionLog(**log_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return {"status": "success", "id": db_obj.id}
    except Exception as e:
        db.rollback()
        print(f"❌ Error saving interaction: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save to database: {e}")