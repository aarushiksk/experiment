# from PyPDF2 import PdfReader

# reader = PdfReader("Aarushi_s_Resume_AIML (6).pdf")
# number_of_pages = len(reader.pages)
# page = reader.pages[0]
# text = page.extract_text()

# print(text)

from fastapi import FastAPI, File, UploadFile


app = FastAPI()


@app.get("/")
async def start():
    return {"message": "Hello World"}

@app.get("/pdf")
async def read_pdf():
    return {"message": "This is a PDF Reader"}
