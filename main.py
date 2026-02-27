from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
import os
import uuid

# Database imports
from database import engine, SessionLocal, Base
from models import AnalysisResult

# CrewAI imports
from crewai import Crew, Process
from agents import financial_analyst
from task import financial_analysis_task

# Create DB tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Document Analyzer")


# ─────────────────────────────────────────────────────────────
# Run CrewAI workflow
# ─────────────────────────────────────────────────────────────
def run_crew(query: str, file_path: str = "data/sample.pdf"):
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[financial_analysis_task],
        process=Process.sequential,
    )

    result = financial_crew.kickoff({
        "query": query,
        "file_path": file_path
    })

    return result


# ─────────────────────────────────────────────────────────────
# Health Check Endpoint
# ─────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


# ─────────────────────────────────────────────────────────────
# Analyze Financial Document
# ─────────────────────────────────────────────────────────────
@app.post("/analyze")
async def analyze_financial_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):

    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        # Ensure folder exists
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        if not query:
            query = "Analyze this financial document for investment insights"

        # Run CrewAI
        response = run_crew(query=query.strip(), file_path=file_path)

        # Save result to SQLite database
        db: Session = SessionLocal()

        db_record = AnalysisResult(
            filename=file.filename,
            query=query,
            analysis=str(response)
        )

        db.add(db_record)
        db.commit()
        db.close()

        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing financial document: {str(e)}"
        )

    finally:
        # Cleanup uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass


# ─────────────────────────────────────────────────────────────
# Fetch Stored Results
# ─────────────────────────────────────────────────────────────
@app.get("/results")
def get_results():
    db: Session = SessionLocal()
    results = db.query(AnalysisResult).all()
    db.close()

    return [
        {
            "id": r.id,
            "filename": r.filename,
            "query": r.query,
            "analysis": r.analysis,
            "created_at": r.created_at
        }
        for r in results
    ]


# ─────────────────────────────────────────────────────────────
# Run Server
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)