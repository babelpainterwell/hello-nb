from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, model_validator
import os
import google.generativeai as genai 
from dotenv import load_dotenv
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  
        logging.StreamHandler()          
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Add CORS middleware to allow requests from the same origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Configure Generative AI
def configure_genai():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    
    genai.configure(api_key=api_key)
    
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    system_instruction = (
        "You are an English assistant helping a user understand Chinese social media comments. "
        "Focus on only important nuances, slang, or cultural references. "
        "If the comment input is in Chinese, please provide the English translation first. "
        "Please provide a clear explanation and try to be brief and concise."
        "It's ok if there is no slang or cultural nuances in the comment, then just provide the English translation."
    )
    
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        system_instruction=system_instruction,
        generation_config=generation_config,
    )
    return model

model = configure_genai()

def get_model():
    return model


class CommentRequest(BaseModel):
    comment: str
    context: str | None = None

    @model_validator(mode="before")
    def validate_inputs(cls, values):
        comment = values.get("comment", "").strip()
        context = values.get("context", "")

        # Check if comment is empty
        if not comment:
            raise ValueError("Comment cannot be empty.")

        # Check if comment is too long
        if len(comment) > 2000:
            raise ValueError("Comment is too long. Please keep it under 2000 characters.")

        # Check if context is too long
        if context and len(context) > 2000:
            raise ValueError("Context is too long. Please keep it under 2000 characters.")

        return values

# Serve the index.html for the root URL
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("app/static/index.html") as f:
        return f.read()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/interpret")
def interpret_comment(request: CommentRequest, model=Depends(get_model)):
    try:
        content = f"comment input: {request.comment}\ncontext: {request.context or ''}"
        response = model.generate_content(content)
        logger.info(f"Generated response for comment: {request.comment}\nResponse: {response.text}\n")
        return {"response": response.text}
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")