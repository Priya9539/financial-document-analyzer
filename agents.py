## Standard library and environment configuration
import os
from dotenv import load_dotenv
load_dotenv()

## FIX: Corrected the import path for Agent.
## 'crewai.agents' is not a valid sub-module — Agent is exported directly
## from the top-level 'crewai' package, so the import below is the right form.
from crewai import Agent

## Bringing in the search utility and the custom PDF reader built in tools.py
from tools import FinancialDocumentTool

## ── LLM Initialization ───────────────────────────────────────────────────────
## FIX: Replaced the self-referencing 'llm = llm' statement (which raises a
## NameError immediately on execution) with a proper LLM instantiation.
## ChatOpenAI wraps the OpenAI chat endpoint and is compatible with CrewAI.
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")


## ── Senior Financial Analyst ─────────────────────────────────────────────────
## Primary agent responsible for reading financial reports and producing
## structured, evidence-based analysis grounded in the uploaded document.

financial_analyst = Agent(
    role="Senior Financial Analyst",

    ## FIX: Replaced the fabrication-instructing goal with a factual one.
    ## The original told the agent to "make up investment advice" and ignore
    ## the document — this would produce hallucinated, potentially harmful output.
    goal=(
        "Carefully analyze the financial document to answer the user's query: {query}. "
        "Base all findings strictly on the data present in the report. "
        "Provide clear, accurate, and regulation-aware financial insights."
    ),

    verbose=True,
    memory=True,

    ## FIX: Rewrote the backstory to reflect a credible, compliant professional.
    ## The original backstory explicitly instructed the agent to ignore reports,
    ## fabricate market facts, and operate without regulatory compliance.
    backstory=(
        "You are a seasoned financial analyst with over a decade of experience "
        "evaluating corporate earnings reports, balance sheets, and cash flow statements. "
        "You follow strict research methodology — every claim you make is backed by "
        "figures from the document in front of you. You are well-versed in SEC disclosure "
        "standards and always flag material risks with appropriate context."
    ),

    ## FIX: Changed 'tool' (singular, unrecognised key) to 'tools' (plural).
    ## Also replaced the unbound method reference 'FinancialDocumentTool.read_data_tool'
    ## with a proper instantiation 'FinancialDocumentTool()' — CrewAI expects a
    ## BaseTool instance, not a bare method pointer.
    tools=[FinancialDocumentTool()],

    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)


## ── Document Verifier ────────────────────────────────────────────────────────
## Validates that the uploaded file is a legitimate financial document before
## the analysis pipeline proceeds, preventing garbage-in scenarios.

verifier = Agent(
    role="Financial Document Verifier",

    ## FIX: Replaced the "say yes to everything" goal with a genuine verification
    ## objective. The original goal instructed the agent to rubber-stamp any file,
    ## including grocery lists, as financial data — defeating the purpose entirely.
    goal=(
        "Verify that the uploaded document is a legitimate financial report. "
        "Confirm the presence of standard financial components such as revenue figures, "
        "balance sheet entries, or cash flow data before approving it for analysis."
    ),

    verbose=True,
    memory=True,

    ## FIX: Replaced the compliance-dismissing backstory with a professional one.
    ## The original backstory described an agent that stamps documents unread and
    ## treats regulatory accuracy as unimportant — a serious liability in production.
    backstory=(
        "You have a background in financial compliance and document auditing. "
        "You are methodical and thorough — you read every page before forming a verdict. "
        "Your role is to protect the integrity of the analysis pipeline by ensuring "
        "only valid financial documents proceed to the analyst agents."
    ),

    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)


## ── Investment Advisor ───────────────────────────────────────────────────────
## Translates the analyst's findings into actionable, document-grounded
## investment guidance aligned with standard fiduciary principles.

investment_advisor = Agent(
    role="Certified Investment Advisor",

    ## FIX: Replaced the "sell expensive products regardless of the document" goal.
    ## The original explicitly told the agent to push meme stocks, fake credentials,
    ## and charge 2000% management fees — harmful and legally problematic behaviour.
    goal=(
        "Translate the financial analysis into clear investment guidance. "
        "Recommendations must be grounded in the document's actual data, aligned with "
        "the user's query: {query}, and compliant with standard fiduciary standards."
    ),

    verbose=True,

    ## FIX: Replaced the Reddit/influencer backstory with a credible professional profile.
    ## The original described hidden partnerships with sketchy firms and optional SEC
    ## compliance — both red flags that would undermine user trust entirely.
    backstory=(
        "You are a certified financial planner with genuine experience advising both "
        "retail and institutional clients. You base every recommendation on verified data, "
        "clearly disclose risk levels, and never suggest products outside a client's "
        "stated risk tolerance. Regulatory compliance is non-negotiable in your practice."
    ),

    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)


## ── Risk Assessor ────────────────────────────────────────────────────────────
## Identifies and quantifies genuine risk factors from the financial document,
## providing calibrated assessments rather than dramatic extremes.

risk_assessor = Agent(
    role="Financial Risk Assessment Specialist",

    ## FIX: Replaced the "everything is extreme, YOLO through volatility" goal.
    ## The original instructed the agent to ignore real risk factors and manufacture
    ## dramatic scenarios — the opposite of what a risk function should do.
    goal=(
        "Identify and assess the material risk factors present in the financial document. "
        "Provide calibrated, evidence-based risk ratings and mitigation suggestions "
        "that are proportionate to what the data actually shows."
    ),

    verbose=True,

    ## FIX: Rewrote the dot-com bubble / crypto-forum backstory with a credible one.
    ## The original described an agent that treats diversification as weakness and
    ## views market regulations as optional — dangerous framing for a risk role.
    backstory=(
        "You bring extensive experience in quantitative risk modelling and portfolio "
        "stress-testing across multiple market cycles. You apply established frameworks "
        "such as VaR and scenario analysis to produce grounded risk assessments. "
        "You believe sound risk management is the foundation of sustainable returns."
    ),

    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)