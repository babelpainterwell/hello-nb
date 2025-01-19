from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI


app = FastAPI()
client = OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class CommentRequest(BaseModel):
    comment: str
    contex: str | None = None

@app.post("/interpret")
def interpret_comment(request: CommentRequest):
    """
    This endpoint accepts Chinese text and optional context,
    then uses the OpenAI API to interpret slang and nuances
    in English.
    """
    comment = request.comment
    context = request.context or ""

    # You can add/change prompt engineering here to instruct the model

    prompt = f"""
            You are an English assistant helping a user understand Chinese social media comments.
            Explain the comment below in English, including any nuances, slang, or cultural references.

            Comment in Chinese: {comment}

            Context (if any): {context}

            If the comment input is in Chinese, please provide the English translation first before explaining the nuances.

            Please provide a clear, thorough explanation and try to be concise.
            """
    

    DEVLOPER_MESSAGE = f"""
                        You are an English assistant helping a user understand Chinese social media comments.
                        Explain the comment in English, including any nuances, slang, or cultural references.
                        
                        If the comment input is in Chinese, please provide the English translation first before explaining the nuances.

                        Please provide a clear, thorough explanation and try to be concise.
                        """

    try: 
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "developer", "content": DEVLOPER_MESSAGE},
                {
                    "role": "user",
                    "content": f"Comment: {comment}\nContext: {context}\n"
                }
            ]
        )
        ans = completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
