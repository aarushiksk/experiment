# from PyPDF2 import PdfReader

# reader = PdfReader("Aarushi_s_Resume_AIML (6).pdf")
# number_of_pages = len(reader.pages)
# page = reader.pages[0]
# text = page.extract_text()

# print(text)

# from fastapi import FastAPI, File, UploadFile


# app = FastAPI()


# @app.get("/")
# async def start():
#     return {"message": "Hello World"}

# @app.post("/pdf")
# async def read_pdf():
#     return {"message": "This is a PDF Reader"}


from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import PyPDF2
from io import BytesIO

app = FastAPI()

# Global variable to store extracted text
extracted_text_storage = ""

class TextResponse(BaseModel):
    text: str

@app.post("/", response_model=TextResponse)
async def extract_text(file: UploadFile = File(...)):
    global extracted_text_storage

    # Read the uploaded file
    file_content = await file.read()
    pdf_file = BytesIO(file_content)
    
    # Extract text from the PDF
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    
    # Store the extracted text
    extracted_text_storage = text

    return TextResponse(text=text)

@app.get("/extracted-text", response_model=TextResponse)
async def get_extracted_text():
    if not extracted_text_storage:
        raise HTTPException(status_code=404, detail="No extracted text found. Please upload a PDF first.")
    
    return TextResponse(text=extracted_text_storage)
