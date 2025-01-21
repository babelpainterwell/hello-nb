from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
import google.generativeai as genai 
from dotenv import load_dotenv
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Logs will be written to `app.log`
        logging.StreamHandler()          # Logs will also appear in the console
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI()

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

    @classmethod
    def validate(cls, values):

        # Check if comment is empty
        if not values["comment"].strip():
            raise ValueError("Comment cannot be empty.")

        # check if comment is too long
        if len(values["comment"]) > 2000:
            raise ValueError("Comment is too long. Please keep it under 2000 characters.")

        # check if context is too long
        if values["context"] and len(values["context"]) > 2000:
            raise ValueError("Context is too long. Please keep it under 2000 characters.")

        return values

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