from fastapi import FastAPI, UploadFile, File
from util import process_file
from db import save_to_db, create_tables

app = FastAPI()

@app.on_event("startup")
def startup():
    create_tables()

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    data = process_file(contents, file.filename)
    save_to_db(data)
    return {"status": "success", "parsed_data": data}
