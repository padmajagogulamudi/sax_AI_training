import os
import fitz
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


# Read PDF

pdf_path = r"C:\Users\Padmaja\Downloads\Saxon_Handbook.pdf"

document = fitz.open(pdf_path)

full_text = ""

for page in document:
    full_text += page.get_text() + "\n"


# Create chunks

chunk_size = 1000
overlap = 200

chunks = []

start = 0

while start < len(full_text):

    end = start + chunk_size

    chunk = full_text[start:end]

    chunks.append(chunk)

    start = end - overlap


print("Number of chunks:", len(chunks))


# Generate embeddings

embeddings = []

for i, chunk in enumerate(chunks):

    response = client.embeddings.create(
        model=deployment,
        input=chunk
    )

    embedding = response.data[0].embedding

    embeddings.append(embedding)

    print(f"Embedded chunk {i + 1}/{len(chunks)}")


# Convert embeddings to NumPy array

embeddings_array = np.array(
    embeddings,
    dtype="float32"
)


print("\nEmbedding array shape:")
print(embeddings_array.shape)


# Create FAISS index

dimension = len(embeddings[0])

index = faiss.IndexFlatL2(dimension)

index.add(embeddings_array)


print("Number of vectors in FAISS:", index.ntotal)


# Create directory

os.makedirs("vector_store", exist_ok=True)


# Save FAISS index

faiss.write_index(
    index,
    "vector_store/handbook.index"
)


print("FAISS index saved successfully.")
import json

with open("vector_store/chunks.json", "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)

print("Chunks saved successfully.")