from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import PyPDF2
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://fastapi-example-kw8k.onrender.com",
    "http://localhost:3000/dashboard/resume",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
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
    
    final_answer=""
    for line in text.split("\n"):
        if line:
            final_answer+=line+" "
    index = final_answer.find("Skills")
    if index == -1:
        raise HTTPException(status_code=400, detail="The keyword 'Skills' was not found.")
        
    start_index = index + len("Skills")
    end_index = final_answer.find("Projects")
        
    if end_index == -1:
            extracted_text = final_answer[start_index:].strip()
    else:
            extracted_text = final_answer[start_index:end_index].strip()
        
    if not extracted_text:
        raise HTTPException(status_code=400, detail="No text found between 'Skills' and 'Projects'.")
        
    return TextResponse(text=extracted_text)



@app.get("/extracted-text", response_model=TextResponse)
async def get_extracted_text():
    if not extracted_text_storage:
        raise HTTPException(status_code=404, detail="No extracted text found. Please upload a PDF first.")
    
    return TextResponse(text=extracted_text_storage)
