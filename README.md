# 🧠 LangGraph Agent Design – AI-first HCP CRM Module

## 🎯 Objective
Enable field reps to log and edit HCP interactions using conversational AI with LangGraph + LLMs.

## 🤖 Role of LangGraph Agent
- Acts as the orchestrator between user input and LLM tools.
- Determines user intent (log/edit) and invokes appropriate tool.
- Coordinates memory, context, and API responses for CRM functions.

## 🧰 Tools Used by LangGraph Agent

### 1. LogInteraction Tool
Captures HCP data from user messages. Extracts:
- HCP name
- Interaction summary
- Date/time
- Sentiment
*Uses Groq Gemma 2 to extract JSON-formatted entities.*

### 2. EditInteraction Tool
Modifies previously logged interactions.
- Uses interaction ID
- Accepts field updates
- Supports correction prompts like: “Update Dr. Sharma’s follow-up status to true.”

### 3. HCPProfileFetcher Tool
Fetches HCP profiles from DB using name or ID.

### 4. SuggestMaterials Tool
Recommends PDFs or studies to share, based on product discussed.

### 5. FollowUpScheduler Tool
Auto-generates follow-up actions with time/date using GPT logic.

## 🔗 AI Stack
- LangGraph
- Groq Gemma 2 9B-IT
- FastAPI
- PostgreSQL
