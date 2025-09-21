from fastapi import FastAPI, Request
from pydantic import BaseModel
from src.text_response_automation.crew import TextResponseAutomationCrew

app = FastAPI()

class PromptRequest(BaseModel):
    user_text: str

@app.get("/generate")
async def generate_response(prompt: PromptRequest):
    crew = TextResponseAutomationCrew().crew()
    result = crew.kickoff(inputs={"user_text": prompt.user_text})
    return {"response": result.raw}

@app.get("/")
async def root():
    return {"message": "api working"}