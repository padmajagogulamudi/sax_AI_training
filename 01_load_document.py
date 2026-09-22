import fitz

pdf_path = r"c:\Users\Padmaja\Downloads\Saxon_Handbook.pdf"
#resource location
document = fitz.open(pdf_path)

print("Number of pages:", len(document))

for page_number, page in enumerate(document):
    text = page.get_text()

    print("\n==============================")
    print("PAGE:", page_number + 1)
    print("==============================")
    print(text)