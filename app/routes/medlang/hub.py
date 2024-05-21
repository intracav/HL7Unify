"""
  Medlang.ai Hub - API routes to generate real world patient data
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Tuple
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import DirectoryLoader, JSONLoader
from pathlib import Path
from pprint import pprint


base_dir = Path(__file__).resolve().parent.parent.parent


router = APIRouter()


class Hub(BaseModel):
    # take optional parameters for what kind of data to be generated (e.g. demographics, vitals, etc.)
    sex: str
    age: int
    symptoms: List[str]
    vitals: List[str]
    medications: List[str]
    allergies: List[str]


@router.post("/generate_patient")
async def generate_patient(hub: Hub):
    # generate vector embeddings
    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )  # SentenceTransformer is a wrapper around transformers that generates embeddings for text
    # this embedding model is temporary until we have a trained model using custom patient data

    # TODO: format the data into object format to match the vector database's training data
    patient_data_query = f"{hub}"

    mock_vector_database_filepath = f"{base_dir}/sample_files/Google-ADT_A01 - 1.json"

    try:
        # load the vector database
        
        # generate embeddings for the requested data
        query_embeddings = model.encode(patient_data_query)

        # load the mock vector database using one JSON file
        # loader = DirectoryLoader(
        #     path=mock_vector_database_filepath,
        #     glob="**/*.json",
        #     loader_cls=JSONLoader,
        #     loader_kwargs={"jq_schema": ".", "text_content": "False"},
        # )
        loader = JSONLoader(
            file_path=mock_vector_database_filepath,
            jq_schema=".",
            text_content=False,
        )
        docs = loader.load()
        print(docs[0].page_content)

        # load the vector database using the FAISS vector store
        # db = FAISS.from_documents(docs, query_embeddings)

        # perform a similarity search on the vector database
        # similar_docs = db.similarity_search(query_embeddings)

        # return the similar embeddings - either as a whole object, or selected parts to make a new patient that matches the requested data
        return {"message": f"{query_embeddings}"}
    except Exception as e:
        return {"message": f"Data generation failed {e}"}
