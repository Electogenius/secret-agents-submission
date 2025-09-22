from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.text_response_automation.crew import TextResponseAutomationCrew

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    user_text: str

@app.post("/generate")
async def generate_response(prompt: PromptRequest):
    crew = TextResponseAutomationCrew().crew()
    result = crew.kickoff(inputs={"user_text": prompt.user_text})
    return {"response": result.raw}

@app.get("/")
async def root():
    return {"message": "api working"}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}

@app.get("/healthz", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}