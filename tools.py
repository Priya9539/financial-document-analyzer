## Standard library and environment setup
import os
from dotenv import load_dotenv
load_dotenv()

## Third-party PDF loader
from langchain_community.document_loaders import PyPDFLoader

## CrewAI base tool class
from crewai.tools import BaseTool   

from pydantic import Field


# ── Financial Document Reader ────────────────────────────────────────────────

class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "Reads and extracts text from a PDF financial document."

    def _run(self, path: str = 'data/sample.pdf'):
        """
        Loads a PDF file page by page and returns the cleaned full text.
        """

        # Load PDF pages properly into a variable
        docs = PyPDFLoader(path).load()

        full_report = ""
        for data in docs:
            content = data.page_content

            # Remove excessive blank lines
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")

            full_report += content + "\n"

        return full_report


# ── Investment Analysis Tool ─────────────────────────────────────────────────

class InvestmentTool(BaseTool):
    name: str = "Investment Analyzer"
    description: str = "Analyzes financial document data for investment insights."

    def _run(self, financial_document_data: str):

        processed_data = financial_document_data

        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1

        return "Investment analysis functionality to be implemented"


# ── Risk Assessment Tool ─────────────────────────────────────────────────────

class RiskTool(BaseTool):
    name: str = "Risk Assessor"
    description: str = "Performs risk assessment on financial document data."

    def _run(self, financial_document_data: str):
        return "Risk assessment functionality to be implemented"