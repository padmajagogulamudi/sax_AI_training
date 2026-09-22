import fitz

pdf_path = r"c:\Users\Padmaja\Downloads\Saxon_Handbook.pdf"
#resource location
document = fitz.open(pdf_path)
full_text=""
for page in document:
    full_text+=page.get_text()+"\n"

print("Total characters:", len(full_text))



#======chunking
chunks=[]
chunk_size=500
for start in range(0,len(full_text),chunk_size):
    chunk=full_text[start:start+chunk_size]
    chunks.append(chunk)
print("Total chunks:", len(chunks))

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

print("\n================ FIRST CHUNK ================\n")
print(chunks[0])