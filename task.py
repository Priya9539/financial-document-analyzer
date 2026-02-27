## Standard library and environment configuration
from crewai import Task

## FIX: Imported all four specialist agents instead of just two.
## Previously only 'financial_analyst' and 'verifier' were imported,
## meaning 'investment_advisor' and 'risk_assessor' were unavailable
## when their respective tasks tried to reference them below.
from agents import financial_analyst, verifier, investment_advisor, risk_assessor

## Bringing in the search utility and the custom PDF reader built in tools.py
from tools import FinancialDocumentTool


## ── Primary Financial Analysis Task ─────────────────────────────────────────
## FIX 1: Renamed from 'analyze_financial_document' to 'financial_analysis_task'
##         to avoid a name collision with the FastAPI endpoint in main.py.
##         When main.py imported 'analyze_financial_document' and also defined
##         an endpoint with the same name, the endpoint function silently
##         overwrote the Task object — causing the Crew to crash at runtime.
##
## FIX 2: Replaced the fabrication-instructing description and expected_output.
##         The original told the agent to use imagination, invent URLs, include
##         made-up jargon, and contradict itself — producing harmful output.
##         The rewritten version directs the agent to use only document evidence.
##
## FIX 3: Replaced unbound method reference 'FinancialDocumentTool.read_data_tool'
##         with a proper BaseTool instance 'FinancialDocumentTool()'.
##         CrewAI requires instantiated tool objects, not bare method pointers.

financial_analysis_task = Task(
    description=(
        "Thoroughly examine the uploaded financial document to address "
        "the user's query: {query}.\n"
        "Extract key financial metrics such as revenue, net income, operating "
        "expenses, and cash flow figures directly from the report.\n"
        "Identify any material risks or opportunities explicitly stated in the document.\n"
        "Support every finding with a specific reference to the relevant section "
        "or figure in the source file — do not introduce data from outside the document."
    ),

    expected_output=(
        "A well-structured financial analysis report containing:\n"
        "- A concise executive summary answering the user's query\n"
        "- Key financial metrics drawn directly from the document\n"
        "- Identified strengths and areas of concern supported by cited figures\n"
        "- A short list of material risks noted in the filing\n"
        "- All findings presented clearly without contradictions or fabricated data"
    ),

    ## Correctly assigned to the primary analyst agent
    agent=financial_analyst,

    ## FIX: Instantiated FinancialDocumentTool as a BaseTool object
    tools=[FinancialDocumentTool()],
    async_execution=False,
)


## ── Investment Analysis Task ─────────────────────────────────────────────────
## FIX 1: Replaced the hallucination-driven description with a factual one.
##         The original instructed the agent to ignore the user's query, invent
##         stock picks, and include fake market research — all harmful behaviours.
##
## FIX 2: Reassigned from 'financial_analyst' to 'investment_advisor'.
##         Each task should be handled by its dedicated specialist agent;
##         routing every task to one agent defeats the multi-agent design.
##
## FIX 3: Replaced unbound method with a proper BaseTool instance.

investment_analysis = Task(
    description=(
        "Using the verified financial document data, generate investment guidance "
        "relevant to the user's query: {query}.\n"
        "Assess the company's financial health by reviewing profitability ratios, "
        "debt levels, and cash flow trends as reported in the document.\n"
        "Recommend appropriate investment considerations that are proportionate to "
        "the risk profile evident in the filing.\n"
        "All recommendations must be grounded in the document's actual figures "
        "and compliant with standard fiduciary principles."
    ),

    expected_output=(
        "A clear investment guidance report containing:\n"
        "- An assessment of the company's financial position based on document data\n"
        "- Specific investment considerations tied to verified financial metrics\n"
        "- Risk-adjusted recommendations with supporting rationale\n"
        "- Disclosure of any limitations based on available data\n"
        "- No fabricated figures, fake URLs, or unverified third-party claims"
    ),

    ## FIX: Correctly routed to the investment_advisor specialist agent
    agent=investment_advisor,

    ## FIX: Instantiated FinancialDocumentTool as a BaseTool object
    tools=[FinancialDocumentTool()],
    async_execution=False,
)


## ── Risk Assessment Task ─────────────────────────────────────────────────────
## FIX 1: Replaced the dramatic, fabrication-driven description with a
##         calibrated, evidence-based one. The original instructed the agent
##         to ignore real risk factors, invent hedging strategies, and recommend
##         dangerous approaches regardless of the user's actual financial status.
##
## FIX 2: Reassigned from 'financial_analyst' to 'risk_assessor'.
##
## FIX 3: Replaced unbound method with a proper BaseTool instance.

risk_assessment = Task(
    description=(
        "Conduct a structured risk assessment based on the financial document "
        "in response to the user's query: {query}.\n"
        "Identify material risk factors explicitly disclosed in the filing, "
        "including liquidity risk, market exposure, debt obligations, and "
        "any forward-looking uncertainty statements.\n"
        "Apply established risk frameworks to quantify and prioritise each "
        "identified risk in proportion to what the document actually shows.\n"
        "Do not introduce risk scenarios that are unsupported by the source data."
    ),

    expected_output=(
        "A calibrated risk assessment report containing:\n"
        "- A prioritised list of risk factors sourced directly from the document\n"
        "- A brief explanation of each risk and its potential financial impact\n"
        "- Suggested mitigation strategies appropriate to the identified risks\n"
        "- An overall risk rating with clear justification\n"
        "- No fabricated risk models, invented institutions, or unrealistic timelines"
    ),

    ## FIX: Correctly routed to the risk_assessor specialist agent
    agent=risk_assessor,

    ## FIX: Instantiated FinancialDocumentTool as a BaseTool object
    tools=[FinancialDocumentTool()],
    async_execution=False,
)


## ── Document Verification Task ───────────────────────────────────────────────
## FIX 1: Replaced the "just guess and approve everything" description with a
##         genuine verification objective. The original told the agent to
##         hallucinate financial terms, skip careful reading, and call any file
##         a financial document — completely undermining pipeline integrity.
##
## FIX 2: Reassigned from 'financial_analyst' to 'verifier'.
##
## FIX 3: Replaced unbound method with a proper BaseTool instance.

verification = Task(
    description=(
        "Inspect the uploaded file to confirm it is a legitimate financial document "
        "before it proceeds to the analysis pipeline.\n"
        "Check for the presence of standard financial report components such as "
        "income statement data, balance sheet entries, cash flow figures, or "
        "official regulatory disclosures.\n"
        "If the document does not contain recognisable financial content, "
        "flag it clearly and halt further processing with a descriptive reason.\n"
        "Base the verification decision solely on what is present in the file — "
        "do not assume or infer financial content that is not there."
    ),

    expected_output=(
        "A verification summary containing:\n"
        "- A clear pass or fail verdict on whether the file is a financial document\n"
        "- The specific financial components identified that support the verdict\n"
        "- The document type inferred (e.g. annual report, earnings release, 10-K)\n"
        "- Any anomalies or missing sections noted during review\n"
        "- A concise confidence statement based strictly on observed document content"
    ),

    ## FIX: Correctly routed to the verifier specialist agent
    agent=verifier,

    ## FIX: Instantiated FinancialDocumentTool as a BaseTool object
    tools=[FinancialDocumentTool()],
    async_execution=False,
)