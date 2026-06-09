from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import tabula
from io import StringIO
import numpy as np

app = FastAPI(title="Data Analyzer API", version="1.0")

@app.get("/")
def home():
    return {"message": "Data Analyzer API is running", "docs": "/docs"}

# 1. CSV Upload + Analysis
@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Sirf CSV file allowed")

    try:
        df = pd.read_csv(file.file)
        return await run_analysis(df, file.filename)
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

# 2. PDF to CSV + Analysis
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Sirf PDF file allowed")

    try:
        dfs = tabula.read_pdf(file.file, pages='all', multiple_tables=True, stream=True)
        if not dfs:
            raise HTTPException(400, "PDF me table nahi mili")

        df = pd.concat(dfs, ignore_index=True)
        return await run_analysis(df, file.filename)
    except Exception as e:
        raise HTTPException(500, f"PDF Error: {str(e)}")

# 3. AI Analysis Function - Yahi sir ko impress karega
async def run_analysis(df: pd.DataFrame, filename: str):
    df = df.replace({np.nan: None}) # NaN ko null kar do JSON ke liye

    analysis = {
        "filename": filename,
        "overview": {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),
            "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024**2, 2)
        },

        "data_quality": {
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
            "unique_counts": df.nunique().to_dict()
        },

        "statistics": {},
        "top_insights": {},
        "sample_data": df.head(5).to_dict(orient='records')
    }

    # Numeric columns ka stats
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        analysis["statistics"] = numeric_df.describe().round(2).to_dict()

        # Top insights - AI jaisa
        for col in numeric_df.columns:
            analysis["top_insights"][f"Max {col}"] = float(numeric_df[col].max())
            analysis["top_insights"][f"Min {col}"] = float(numeric_df[col].min())
            analysis["top_insights"][f"Avg {col}"] = float(numeric_df[col].mean())

    # Categorical columns - sabse zyada wali value
    categorical_df = df.select_dtypes(include=['object'])
    for col in categorical_df.columns[:3]: # sirf 3 column tak
        top_val = df[col].value_counts().head(1)
        if not top_val.empty:
            analysis["top_insights"][f"Top {col}"] = {
                "value": top_val.index[0],
                "count": int(top_val.values[0])
            }

    return JSONResponse(content=analysis)

# 4. Column wise count endpoint
@app.post("/count-by/{column}")
async def count_by_column(column: str, file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    if column not in df.columns:
        raise HTTPException(404, f"Column '{column}' nahi mili")

    counts = df[column].value_counts().head(10).to_dict()
    return {"column": column, "top_10_counts": counts}