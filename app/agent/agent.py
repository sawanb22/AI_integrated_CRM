from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional, List
# ✅ FIX: Import the 'get_llm' function from the correct file
from app.llm import get_llm
from datetime import date

# Get the LLM instance to use in this module
llm = get_llm()

# ✅ 1. Define a robust Pydantic model for extraction.
# This tells the LLM exactly what structure to use.
class Interaction(BaseModel):
    """Information about a sales rep's interaction with a healthcare professional."""
    hcp_name: str = Field(description="Name of the healthcare professional.")
    date_of_interaction: date = Field(description="Date of the meeting. Must be a valid YYYY-MM-DD date.")
    time: Optional[str] = Field(description="Time of the interaction (e.g., '04:45 PM').")
    interaction_type: Optional[str] = Field(description="Type of interaction (e.g., 'Email', 'Meeting', 'Call').")
    key_discussion_points: str = Field(description="A concise summary of the key points discussed.")
    products_discussed: Optional[List[str]] = Field(description="List of any product names that were discussed.")
    follow_up_needed: bool = Field(description="Whether a follow-up action is required.")
    outcome: Optional[str] = Field(description="Outcome of the interaction (e.g., 'Requested samples').")

# ✅ 2. Create a much more detailed system prompt, optimized for Gemma.
# This provides a role, rules, context, and a high-quality example.
SYSTEM_PROMPT_TEMPLATE = """
You are an expert AI assistant for a healthcare CRM. Your task is to extract key information from a sales representative's interaction notes and structure it into a JSON object that strictly conforms to the provided schema.

Today's date is July 27, 2025. Use this as a reference for relative dates like "today" or "yesterday".

Follow these rules carefully:
1. **hcp_name**: Extract the healthcare professional's name (e.g., "Dr. Sharma"). If no name is found, return "UNKNOWN".
2. **date_of_interaction**: Extract the date. It MUST be in YYYY-MM-DD format. If the note says "today", use the current date. If it says "July 27", assume the current year (2025).
3. **time**: Extract the time of the interaction (e.g., "04:45 PM"). If no time is found, return "UNKNOWN".
4. **interaction_type**: Extract the type of interaction (e.g., "Email", "Meeting", "Call"). If no type is explicitly mentioned, infer it from the context (e.g., "email" if the note says "got email").
5. **key_discussion_points**: Provide a CONCISE summary of the interaction. Do not just copy the original message.
6. **products_discussed**: Extract all product names into a list of strings. If no products are mentioned, return an empty list [].
7. **follow_up_needed**: Determine if a follow-up is mentioned. Return `true` if it is, otherwise `false`.
8. **outcome**: Extract the outcome of the interaction (e.g., "Requested samples", "Agreed to follow-up"). If no outcome is mentioned, return "UNKNOWN".

Example Interaction:
User Note: "Met with Dr. Evelyn Reed today at 3:00 PM about the new trial for Solara. She needs the phase III data sheet. I'll send it tomorrow."

Expected JSON Output:
```json
{
    "hcp_name": "Dr. Evelyn Reed",
    "date_of_interaction": "2025-07-27",
    "time": "3:00 PM",
    "interaction_type": "Meeting",
    "key_discussion_points": "Discussed new trial for Solara. Dr. Reed requested the phase III data sheet.",
    "products_discussed": ["Solara"],
    "follow_up_needed": true,
    "outcome": "Requested phase III data sheet"
}
```

Now, analyze the user's text and provide ONLY the JSON output. Do not add any extra commentary or markdown formatting.
"""

USER_PROMPT_TEMPLATE = """Text of the interaction:
---
{content}
---
"""

def get_interaction_graph():
    # This function should contain your graph logic
    # For now, we focus on the core extraction
    pass

# ✅ 3. This is the core function that will be called by your graph/endpoint.
def invoke_graph_agent_for_extraction(message: str) -> dict:
    """
    Invokes the LLM with structured output to extract interaction details.
    """
    try:
        # Use with_structured_output for reliable JSON and Pydantic parsing
        structured_llm = llm.with_structured_output(Interaction)
        
        # Construct the full prompt
        prompt_messages = [
            ("system", SYSTEM_PROMPT_TEMPLATE),
            ("user", USER_PROMPT_TEMPLATE.format(content=message))
        ]
        
        response_model = structured_llm.invoke(prompt_messages)
        return response_model.dict()
    except Exception as e:
        print(f"❌ Agent extraction failed: {e}")
        # Return a structured error to help with debugging on the frontend
        return {
            "hcp_name": "Extraction Error",
            "date_of_interaction": date.today(),
            "key_discussion_points": f"Failed to parse content. Error: {str(e)}",
            "products_discussed": [],
            "follow_up_needed": False,
        }
