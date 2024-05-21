"""
  This route will accept one or many HL7 messages and format them into one or many JSON objects.
  
  Once an HL7 message is received, the message will be sent to a fine-tuned text2textgeneration transformer model to be standardized. Then create embeddings for the message and store it in the vector database. Finally, return the standardized message to the user.
  
  I don't currently have a fine-tuned model, so I'm using a pre-trained model from HuggingFace or GPT-3.5-turbo with strategic prompting.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
# from transformers import pipeline
from openai import Embedding
import openai
from secret import OPENAI_API_KEY

router = APIRouter()

openai.api_key = OPENAI_API_KEY

class HL7Data(BaseModel):
    hl7_data: str

@router.post("/format_hl7")
async def format_hl7(data: HL7Data):
    hl7_data = data.hl7_data
    system_prompt = f"You are a medical coding specialist. Your job is to receive HL7 messages from a variety of sources and standardize them in a common JSON-based format. You receive the following HL7 message:\n\n{hl7_data}\n\nYou standardize the message into the following JSON format:\n\n"

    # openai chat completion
    chat_request = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            { "role": "system", "content": system_prompt },
        ]
    )

    standardized_message = chat_request["choices"][0]["message"]["content"]

    response = []

    # create the response object
    response.append(
        {"original_message": hl7_data, "standardized_message": standardized_message}
    )

    # return the response
    return response


# embed the original HL7 message to use for training
@router.post("/embed_hl7")
async def embed_hl7(hl7_messages: List[str]):
    # embed the message
    embedding = Embedding("vector-database")
    embedding.embed(hl7_messages)

    # return the response
    return {"message": "Embedding successful"}
