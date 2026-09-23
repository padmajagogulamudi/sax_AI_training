import os
import json
import faiss
import numpy as np
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

endpoint = os.getenv("CORE_AZURE_OPENAI_ENDPOINT")
subscription_key = os.getenv("CORE_AZURE_OPENAI_API_KEY")
embedding_deployment = os.getenv("CORE_AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")
chat_deployment = os.getenv("CORE_AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
api_version = os.getenv("CORE_AZURE_OPENAI_API_VERSION")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key
)

index = faiss.read_index("vector_store/handbook.index")

with open("vector_store/chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

print("===================================")
print("     SAXON HR HANDBOOK CHATBOT")
print("===================================")
print("Ask questions about the Employee Handbook.")
print("Type 'exit' to stop the chatbot.")
print()

while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    if not question.strip():
        print("Chatbot: Please enter a question.")
        continue

    # Step 1: Convert question into embedding

    response = client.embeddings.create(
        model=embedding_deployment,
        input=question
    )

    question_embedding = response.data[0].embedding

    question_vector = np.array(
        [question_embedding],
        dtype="float32"
    )

    # Step 2: Search FAISS

    k = 3

    distances, indices = index.search(
        question_vector,
        k
    )

    # Step 3: Get relevant chunks

    retrieved_chunks = []

    for index_number in indices[0]:
        retrieved_chunks.append(chunks[index_number])

    # Step 4: Combine chunks into context

    context = "\n\n".join(retrieved_chunks)

    # Step 5: Create prompt

    prompt = f"""
You are an HR assistant for Saxon Infosystems.

Answer the employee's question using ONLY the information
provided in the Employee Handbook context below.

Do not use outside knowledge.
Do not make up or assume any company policy.

If the answer cannot be found in the provided context, say:

"I could not find this information in the Employee Handbook."

Employee Handbook Context:
{context}

Employee Question:
{question}
"""

    # Step 6: Send context + question to GPT-4o

    chat_response = client.chat.completions.create(
        model=chat_deployment,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful HR assistant that answers questions using the provided Employee Handbook context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    # Step 7: Get answer

    answer = chat_response.choices[0].message.content

    print("\nChatbot:", answer)
    print()