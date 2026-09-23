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

with open(
    "vector_store/chunks_with_metadata.json",
    "r",
    encoding="utf-8"
) as file:
    chunks = json.load(file)

print("Number of chunks:", len(chunks))

embeddings = []

for i, chunk in enumerate(chunks):

    text = chunk["text"]

    response = client.embeddings.create(
        model=deployment,
        input=text
    )

    embedding = response.data[0].embedding

    embeddings.append(embedding)

    print(f"Embedded chunk {i + 1}/{len(chunks)}")

embeddings_array = np.array(
    embeddings,
    dtype="float32"
)

print("\nEmbedding array shape:")
print(embeddings_array.shape)

dimension = len(embeddings[0])

index = faiss.IndexFlatL2(dimension)

index.add(embeddings_array)

print("Number of vectors in FAISS:", index.ntotal)

os.makedirs("vector_store", exist_ok=True)

faiss.write_index(
    index,
    "vector_store/handbook_metadata.index"
)

print("FAISS index saved successfully.")

print("\nVector store creation completed.")