import os
import json
import faiss
import numpy as np
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

endpoint = os.getenv("CORE_AZURE_OPENAI_ENDPOINT")
subscription_key = os.getenv("CORE_AZURE_OPENAI_API_KEY")
deployment = os.getenv("CORE_AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")
api_version = os.getenv("CORE_AZURE_OPENAI_API_VERSION")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key
)

index = faiss.read_index(
    "vector_store/handbook_metadata.index"
)

with open(
    "vector_store/chunks_with_metadata.json",
    "r",
    encoding="utf-8"
) as file:
    chunks = json.load(file)

questions = [
    "How many sick leaves can an employee take?",
    "What is the notice period?",
    "What is the company's policy on cryptocurrency?"
]

for question in questions:

    response = client.embeddings.create(
        model=deployment,
        input=question
    )

    question_embedding = response.data[0].embedding

    question_vector = np.array(
        [question_embedding],
        dtype="float32"
    )

    k = 5

    distances, indices = index.search(
        question_vector,
        k
    )

    print("\n===================================")
    print("QUESTION:")
    print(question)
    print("===================================")

    for rank, index_number in enumerate(indices[0]):

        chunk = chunks[index_number]

        print("\nResult:", rank + 1)
        print("Distance:", distances[0][rank])
        print("Page:", chunk["page"])