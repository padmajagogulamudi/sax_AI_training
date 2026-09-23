import fitz
import json
import os

pdf_path = r"C:\Users\Padmaja\Downloads\Saxon_Handbook.pdf"

document = fitz.open(pdf_path)

chunk_size = 1000
overlap = 200

chunks = []

for page_number, page in enumerate(document, start=1):

    page_text = page.get_text()

    start = 0

    while start < len(page_text):

        end = start + chunk_size

        chunk_text = page_text[start:end]

        if chunk_text.strip():
            chunks.append({
                "text": chunk_text,
                "page": page_number
            })

        start = end - overlap

os.makedirs("vector_store", exist_ok=True)

with open(
    "vector_store/chunks_with_metadata.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        chunks,
        file,
        ensure_ascii=False,
        indent=2
    )

print("Chunks created successfully.")
print("Number of chunks:", len(chunks))

print("\nFirst chunk:")
print(chunks[0])