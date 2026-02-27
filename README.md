# Financial Document Analyzer - Debug Assignment

## Project Overview

This project is an AI-powered financial document analysis system built using CrewAI.  
It processes corporate reports, financial statements, and investment documents to generate structured insights, investment recommendations, and risk assessments.

The application is built with FastAPI and supports PDF uploads via an API endpoint.  
Analysis results are stored using SQLite for persistent storage.

---

## Bugs Identified and Fixed

- Fixed incorrect task variable reference in `main.py`
- Resolved missing imports and improper LLM initialization in `agents.py`
- Corrected CrewAI tool binding configuration
- Rewrote inefficient prompts to produce structured and consistent outputs
- Added proper exception handling in file upload logic
- Integrated SQLite database for storing analysis results
- Resolved dependency and environment configuration issues
- Ensured secure handling of environment variables using `.env`

---

## Tech Stack

- Python 3.12
- FastAPI
- CrewAI
- LangChain
- OpenAI API
- SQLite
- SQLAlchemy

---

## Project Structure

```
financial-document-analyzer/
│
├── agents.py
├── task.py
├── tools.py
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
```

---

## Getting Started

### 1. Create Virtual Environment

```sh
python -m venv venv
venv\Scripts\activate   # Windows
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```

Make sure `.env` is added to `.gitignore` to prevent exposing API keys.

---

## Running the Application

Start the FastAPI server:

```sh
uvicorn main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000/docs
```

This opens the interactive Swagger UI for testing endpoints.

---

## API Endpoints

### `GET /`
Health check endpoint.

### `POST /analyze`
Upload a financial PDF file and receive AI-generated financial analysis.

### `GET /results`
Retrieve historical analysis results stored in the SQLite database.

---

## Sample Document Testing

The system can analyze documents such as Tesla’s Q2 2025 financial update.

To test:

1. Download the Tesla Q2 2025 update:
   https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf
2. Save it as:
   ```
   data/sample.pdf
   ```
3. Or upload any financial PDF through the `/analyze` endpoint.

Note: Replace placeholder files with real financial documents for accurate testing.

---

## Expected Features

- Upload financial documents (PDF format)
- AI-powered financial performance analysis
- Investment recommendation insights
- Risk assessment reporting
- Structured output through improved prompt engineering
- Persistent storage of results using SQLite

---

## Bonus Improvements Implemented

- SQLite database integration using SQLAlchemy
- `/results` endpoint to fetch stored analysis records
- Improved prompt engineering for structured financial summaries
- Better exception handling and validation
- Clean modular architecture (agents, tasks, tools separation)

---

## Database Integration

The system stores:

- Uploaded file name
- User query
- Generated analysis result
- Timestamp

Database file:
```
analysis.db
```

Automatically created when the application starts.

---

## Security Notes

- `.env` file is excluded via `.gitignore`
- API keys are never committed to version control
- Uploaded files are deleted after processing

---

## Submission Summary

This repository includes:

- Fully debugged and working code
- Improved prompts and structured outputs
- Database integration for result persistence
- Complete setup instructions
- API documentation
- Clean project organization

The system is ready for evaluation and testing.