# ⚡ Helix Analytics Co-Pilot: AI Data Analyst Agent

Helix Analytics Co-Pilot is a high-utility, autonomous **AI Data Analyst Agent** designed to safely ingest, clean, and cross-examine multi-format business files right on a user's system. Powered by **Google GenAI (Gemini 2.5 Flash)** and wrapped in a modern neon-dark Streamlit dashboard interface, this tool serves as an intelligent analytics workspace that writes and executes calculation scripts locally, completely bypassing cloud container timeout vulnerabilities.

---

## ✨ Key Technical Capabilities

- **Multi-Format Pipeline Ingestion**: Seamlessly registers and previews heterogeneous datasets including **Spreadsheets (.csv, .xlsx, .xls)**, nested data dumps **(.json)**, and relational databases **(.db, .sqlite)** simultaneously.
- **Local Code Interpreter Engine**: Leverages an internal execution loop (`exec()`) to compile and evaluate data transformations natively inside an isolated local project environment layout.
- **Automated Data Type Cleansing**: Implements strict system boundaries to ensure the AI automatically cleanses messy string rows (stripping currency symbols, spaces, and formatting commas) before computing critical statistics or aggregations.
- **Enterprise Security Compliance**: Built with a privacy-first layout. Because credentials live in an untracked local environment layer (`.env`), raw API endpoints and data frames are entirely safe from public Git leaks.
- **One-Click Executive Exporting**: Includes a dynamic Markdown compiler node allowing managers to download polished analytical synthesis report tables immediately.

---

## 🛠️ Architecture & System Workflow

[ Multi-Format File Uploads ]
(CSV, Excel, JSON, SQLite)
                              │
                              ▼
[ Streamlit File Ingest Layout ]──> Logs Live Matrix Meta-Previews
                              │
                              ▼
[ System Context-Mapping Prompt ] ──> Injects Layout Maps (Zero Hallucination)
                              │
                              ▼
[ Gemini 3.5 Flash Engine ] ──> Synthesizes Raw Code Blocks
                              │
                              ▼
[ Local Python Sandbox Environment ] ──> Executes Native Scripts Inside venv Container
                              │
                              ▼
[ Consolidated Markdown Reports ] ──> Render Viewports & Dynamic Download Button

---

## 🚀 Step-by-Step Installation Manual (Mac Desktop Deployment)

Follow these terminal instructions to spin up the separate environment sandbox container on your local system:

### 1. Clone and Navigate to the Repository
```bash
git clone https://github.com[Your-GitHub-Username]/private-ai-data-analyst.git
cd private-ai-data-analyst
```

### 2. Set Up the Isolated Python Virtual Environment

```bash
# Initialize a pristine separate environment structure
python3 -m venv venv

# Activate your folder container workspace space
source venv/bin/activate
```

### 3. Complete Dependency Ingestion
```bash
pip install --upgrade pip
pip install google-genai python-dotenv streamlit pandas openpyxl matplotlib seaborn tabulate SQLAlchemy
```
### 4. Configure Your Private Credentials
Create a private `.env` file in the folder root directory and add your Google Studio string layout value:
```text
GEMINI_API_KEY=AIzaSyYourActualSecretGeminiApiKeyGoesHere
```

### 5. Launch the Local Application Server
```bash
python -m streamlit run app.py
```

---

## 📊 Live Scenario Queries to Test Flaws & Bounds

Drop your business data sets into the control sidebar bay and test the agent's logic using these sample prompt sequences:

1. **The Cleaning Test**: *"Show me the maximum salary and the mathematical group average metrics sorted by country location."*
2. **The SQL / Spreadsheet Cross-Query Test**: *"Cross-reference our local inventory sheet `mock_products.csv` with the uploaded relational database `mock_sales.db`. Join them together on the `product_id` key fields and generate a revenue report."*
3. **The Schema Hallucination Boundary Test**: *"Filter out any employees who have been in their respective designative roles for less than two seasons."* (Tests if the agent strictly respects available columns or guesses fake data rows).

---

## 👨‍💻 Project Development Details
- **Frontend Layer**: Streamlit Framework Custom Dark-Theme Canvas Layout
- **Intelligence Orchestration Engine**: Google GenAI Library SDK
- **Data Structuring Layer**: Pandas, SQLAlchemy Core, Tabulate Formatter
- **Hosting Environment**: Streamlit Community Cloud Ecosystem

---
