from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

# ⚠️ TODO: This API key is hardcoded on purpose for the demo.
# This is DANGEROUS in real projects — Talk 3 will fix this live.
GEMINI_API_KEY = "PUT_YOUR_GEMINI_API_KEY_HERE"

client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI()


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def health_check():
    return {"message": "API is alive"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    gemini_response = client.models.generate_content(
        model="gemini-2.5-flash",                                               # This is the model we are using
        contents=request.prompt,                                                # This is the prompt we are sending to the model
        config=genai.types.GenerateContentConfig(
            temperature=0.1,                                                    # 0.0 is the most deterministic, 2.0 is the most random
            system_instruction="Only answer the question directly.",            # This is the system instruction for the model
        )
    )
    print(gemini_response)                                                     # This is the response from the model
    api_response = gemini_response.text                                         # This is the response's text from the model
    
    return ChatResponse(response=api_response)
