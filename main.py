from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

app = FastAPI(title="Data Analyzer API")

@app.get("/")
def home():
    return {"message": "Data Analyzer API is running", "docs": "/docs"}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

    summary = {
        "rows": len(df),
        "columns": list(df.columns),
        "head": df.head().to_dict()
    }
    return summary

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)