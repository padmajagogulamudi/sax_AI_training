import os
import math

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


text1 = "How many sick leaves can an employee take?"

text2 = "Permanent employees are eligible for 8 Sick Leaves per annum."

text3 = "india is a developping country"


def get_embedding(text):

    response = client.embeddings.create(
        model=deployment,
        input=text
    )

    return response.data[0].embedding


embedding1 = get_embedding(text1)
embedding2 = get_embedding(text2)
embedding3 = get_embedding(text3)


def cosine_similarity(vector_a, vector_b):

    dot_product = 0
    magnitude_a = 0
    magnitude_b = 0

    for i in range(len(vector_a)):

        dot_product += vector_a[i] * vector_b[i]

        magnitude_a += vector_a[i] ** 2

        magnitude_b += vector_b[i] ** 2

    magnitude_a = math.sqrt(magnitude_a)
    magnitude_b = math.sqrt(magnitude_b)

    return dot_product / (magnitude_a * magnitude_b)


similarity_1 = cosine_similarity(embedding1, embedding2)
similarity_2 = cosine_similarity(embedding1, embedding3)


print("Similarity between question and sick leave text:")
print(similarity_1)

print("\nSimilarity between question and travel text:")
print(similarity_2)