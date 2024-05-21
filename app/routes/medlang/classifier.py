"""
  Medlang.ai Classifier - API routes to classify patient HL7 messages + objects for human review
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


router = APIRouter()


class Classifier(BaseModel):
    hl7_data: str


@router.post("/classify_hl7")
async def classify_hl7(data: Classifier):
    tokenizer = AutoTokenizer.from_pretrained("bvanaken/CORe-clinical-diagnosis-prediction")
    model = AutoModelForSequenceClassification.from_pretrained("bvanaken/CORe-clinical-diagnosis-prediction")
    # TODO: format the data into object format for the classification model
    hl7_data = data.hl7_data

    try:
        # process the data into the model
        tokenized_input = tokenizer(hl7_data, return_tensors="pt")
        output = model(**tokenized_input)
        # get the classification
        print(output.logits)
        predictions = torch.sigmoid(output.logits)
        predicted_labels = [model.config.id2label[_id] for _id in (predictions > 0.3).nonzero()[:, 1].tolist()]
        
        print(predicted_labels)
        # return the classification to the user
        return {"classification": predicted_labels}
    except:
        return {"message": f"Data generation failed"}
      
      # sigmoids squash large matrices into a range of 0 to 1 for probability classification
