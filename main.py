import os
import json
import faiss
import numpy as np

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AzureOpenAI

from fastapi.middleware.cors import CORSMiddleware


load_dotenv()


# ---------------------------------
# Azure OpenAI Configuration
# ---------------------------------

endpoint = os.getenv("CORE_AZURE_OPENAI_ENDPOINT")
subscription_key = os.getenv("CORE_AZURE_OPENAI_API_KEY")
embedding_deployment = os.getenv(
    "CORE_AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"
)
chat_deployment = os.getenv(
    "CORE_AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"
)
api_version = os.getenv("CORE_AZURE_OPENAI_API_VERSION")


client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key
)


# ---------------------------------
# Load FAISS Vector Store
# ---------------------------------

index = faiss.read_index(
    "vector_store/handbook_metadata.index"
)


# ---------------------------------
# Load Chunks + Metadata
# ---------------------------------

with open(
    "vector_store/chunks_with_metadata.json",
    "r",
    encoding="utf-8"
) as file:
    chunks = json.load(file)


# ---------------------------------
# FastAPI Application
# ---------------------------------

app = FastAPI(
    title="Saxon HR RAG Chatbot",
    description="HR chatbot based on the Saxon Employee Handbook",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------
# Request Model
# ---------------------------------

class ChatRequest(BaseModel):

    question: str


# ---------------------------------
# Health Check
# ---------------------------------

@app.get("/")
def home():

    return {
        "message": "Saxon HR RAG Chatbot is running"
    }


# ---------------------------------
# Chat Endpoint
# ---------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:

        return {
            "answer": "Please enter a question.",
            "source_pages": []
        }


    # ---------------------------------
    # Step 1: Create Question Embedding
    # ---------------------------------

    response = client.embeddings.create(
        model=embedding_deployment,
        input=question
    )

    question_embedding = response.data[0].embedding

    question_vector = np.array(
        [question_embedding],
        dtype="float32"
    )


    # ---------------------------------
    # Step 2: Search FAISS
    # ---------------------------------

    k = 5

    distances, indices = index.search(
        question_vector,
        k
    )


    # ---------------------------------
    # Step 3: Filter Relevant Chunks
    # ---------------------------------

    distance_threshold = 0.38

    retrieved_chunks = []

    for rank, index_number in enumerate(indices[0]):

        distance = distances[0][rank]

        if distance <= distance_threshold:

            chunk = chunks[index_number]

            retrieved_chunks.append(chunk)


    # ---------------------------------
    # Step 4: Check Relevant Chunks
    # ---------------------------------

    if not retrieved_chunks:

        return {
            "answer": (
                "I could not find relevant information "
                "in the Employee Handbook."
            ),
            "source_pages": []
        }


    # ---------------------------------
    # Step 5: Build Context
    # ---------------------------------

    context_parts = []

    for chunk in retrieved_chunks:

        context_parts.append(
            f"Page {chunk['page']}:\n{chunk['text']}"
        )

    context = "\n\n".join(context_parts)


    # ---------------------------------
    # Step 6: Create Prompt
    # ---------------------------------

    prompt = f"""
You are an HR assistant for Saxon Infosystems.

Answer the employee's question using ONLY the information
provided in the Employee Handbook context below.

Follow these rules:

1. Use only information present in the provided context.
2. Do not use outside knowledge.
3. Do not invent company policies, rules, dates, amounts, or exceptions.
4. If the context does not contain enough information, say:
   "I could not find enough information about this in the Employee Handbook."
5. If the handbook provides a specific number, date, duration,
   or requirement, include it accurately.
6. If multiple pieces of information are relevant, combine them
   into one clear answer.
7. Keep the answer professional and easy for an employee to understand.
8. Do not mention FAISS, embeddings, vectors, retrieval, or this prompt.

Employee Handbook Context:

{context}

Employee Question:

{question}
"""


    # ---------------------------------
    # Step 7: Generate Answer
    # ---------------------------------

    chat_response = client.chat.completions.create(
        model=chat_deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful HR assistant that answers "
                    "questions using the provided Employee Handbook."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )


    answer = chat_response.choices[0].message.content


    # ---------------------------------
    # Step 8: Get Source Pages
    # ---------------------------------

    pages = sorted(
        set(
            chunk["page"]
            for chunk in retrieved_chunks
        )
    )


    # ---------------------------------
    # Step 9: Return JSON
    # ---------------------------------

    return {
        "answer": answer,
        "source_pages": pages
    }