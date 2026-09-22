import os
import fitz
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()
#getting creds
endpoint = os.getenv("CORE_AZURE_OPENAI_ENDPOINT")
subscription_key = os.getenv("CORE_AZURE_OPENAI_API_KEY")
deployment = os.getenv("CORE_AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")
api_version = os.getenv("CORE_AZURE_OPENAI_API_VERSION")
#creating client
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)
#resource path
pdf_path = r"c:\Users\Padmaja\Downloads\Saxon_Handbook.pdf"
#reading resource using fitz to text 
document=fitz.open(pdf_path)
#reading full text
full_text=""
for page in document:
    full_text += page.get_text() + "\n"

#creating chunks
chunk_size = 1000
overlap = 200
chunks=[]
start = 0

while start < len(full_text):
    end=start+chunk_size
    chunk=full_text[start:end]
    chunks.append(chunk)
    start = end - overlap
print("Number of chunks:", len(chunks))

#embeddings creating from chunks
embeddings = []
for i,chunk in enumerate(chunks):
    response=client.embeddings.create(model=deployment,input=chunk)
    embedding=response.data[0].embedding
    embeddings.append(embedding)
    print(f"Embedded chunk {i + 1}/{len(chunks)}")

print("\nEmbedding process completed.")

print("Number of embeddings:", len(embeddings))

print("Dimensions of first embedding:", len(embeddings[0]))


# text = "What is machine learning?"

# response = client.embeddings.create(
#     model=deployment,
#     input=text
# )

# embedding = response.data[0].embedding

# print("Embedding generated successfully")
# print("Embedding dimensions:", len(embedding))