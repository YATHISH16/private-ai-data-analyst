import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ==========================================
# 1. ENHANCED BRANDING & PAGE STYLING
# ==========================================
st.set_page_config(
    page_title="Helix Analytics Co-Pilot", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise CSS Inject Layer
st.markdown("""
    <style>
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    [data-testid="stMetricContainer"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
    }
    [data-testid="stSidebar"] {
        background-color: #0E1117;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    .status-badge {
        padding: 4px 10px;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        background: rgba(0, 200, 83, 0.15);
        color: #00C853;
        border: 1px solid rgba(0, 200, 83, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Main Title Framework Layout
col_header, col_status = st.columns([4, 1])
with col_header:
    st.markdown("<h1 style='margin-bottom:0;'>⚡ Helix Analytics Co-Pilot</h1>", unsafe_allow_html=True)
    st.caption("Enterprise-Grade Autonomous Data Intelligence Engine Powered by Gemini GenAI")
with col_status:
    st.markdown("<br><span class='status-badge'>🟢 AGENT STATUS: ONLINE</span>", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 2. PRIVACY & BACKEND CONFIGURATION
# ==========================================
load_dotenv()
UPLOAD_DIR = "uploaded_data_workspace"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if not os.environ.get("GEMINI_API_KEY"):
    st.error("❌ Key Error: Missing 'GEMINI_API_KEY' entry inside your hidden local `.env` file.")
    st.stop()

client = genai.Client()

# ==========================================
# 3. SIDEBAR DIRECTORY & DATA VIEWER
# ==========================================
st.sidebar.markdown("### 🏢 SYSTEM CONTROL")
st.sidebar.caption("Secure Local Sandbox Active")

uploaded_files = st.sidebar.file_uploader(
    "Upload business tables (CSV, Excel)", 
    type=["csv", "xlsx", "xls"], 
    accept_multiple_files=True,
    help="Files remain locally containerized inside your private Mac directory space."
)

schema_context = "=== DOCK DIRECTORY PATHS AND SCHEMAS ===\n"

st.sidebar.markdown("---")
st.sidebar.markdown("### 📦 ENVIRONMENT FILES")

if not uploaded_files:
    st.sidebar.info("No documents uploaded yet.")
    st.info("👋 **Welcome to your private agent!** Drop data files (CSVs or Excel sheets) into the left sidebar panel to begin your custom analytics session.")
else:
    for file in uploaded_files:
        file_ext = file.name.split(".")[-1].lower()
        saved_path = os.path.join(UPLOAD_DIR, file.name)
        
        with open(saved_path, "wb") as f:
            f.write(file.getbuffer())
            
        with st.sidebar.expander(f"📄 {file.name}", expanded=False):
            try:
                df = pd.read_csv(saved_path, nrows=3) if file_ext == "csv" else pd.read_excel(saved_path, nrows=3)
                schema_context += f"- File Name: '{file.name}' | Local Path: '{saved_path}' | Columns: {', '.join(df.columns.tolist())}\n"
                
                st.metric(label="Detected Columns", value=len(df.columns))
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Mapping failure: {str(e)}")

# ==========================================
# 4. CHAT DASHBOARD INTERFACE
# ==========================================
if uploaded_files:
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="Active Data Streams", value=f"{len(uploaded_files)} Sources")
    with m_col2:
        st.metric(label="Core AI Model", value="Gemini 3.5 Flash") 
    with m_col3:
        st.metric(label="Execution Context Limit", value="1.0M Tokens")
        
    st.markdown("### 💬 Analytical Workspace Console")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Ask Helix to process metrics, find nulls, or filter trees..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            status_placeholder = st.empty()
            with status_placeholder.container():
                st.markdown("⏳ *Helix running local Python code loop...*")
                
            system_instruction = f"""
            You are an expert Data Scientist. Generate clean Python code to answer the user query.

            DATA WORKSPACE MAP:
            {schema_context}

            USER QUERY: {user_input}

            CODING RULES:
            1. Use pandas to read the files from their explicit 'Local Path' provided above.
            2. IMPORTANT DATA CLEANING RULE: If the user asks for mathematical summaries, aggregations, averages, or sums on financial/numeric columns that might be formatted as strings (e.g. containing commas, currency signs like '₹', '$', 'INR', or empty characters), you MUST write string-clearing transformations first.
            3. CRITICAL SCHEMA BOUNDARY RULE: Look closely at the exact column headers provided in the 'DATA WORKSPACE MAP' above. Do NOT guess, hallucinate, or assume any other column names (like assuming 'Role', 'Name', or 'Designation' exist). ONLY filter, group, or display columns that are explicitly listed in the map. If you need to print general rows, output the entire matching dataframe slice or use the columns that are actually available.
            4. Calculate the answer and save your final textual response summary string into a local variable named `final_insight`. Use `.to_markdown()` to format dataframes.
            5. Do not include markdown code block formats in your execution string. Respond ONLY with raw executable python code.
            """

            # Code blocks are nested cleanly within Streamlit's input state container
            try:
                response = client.models.generate_content(
                    model='gemini-3.5-flash', 
                    contents=[
                        {"role": "user", "parts": [{"text": f"{system_instruction}\n\nUser Question: {user_input}"}]}
                    ]
                )
                
                raw_code = response.text.strip()
                
                # Dynamic edge case splitting logic to normalize LLM outputs
                if "```python" in raw_code:
                    raw_code = raw_code.split("```python")[-1].split("```")[0].strip()
                elif "```" in raw_code:
                    raw_code = raw_code.split("```")[1].split("```")[0].strip()

                # Local isolated execution memory scope definition
                execution_context = {
                    "pd": pd,
                    "os": os,
                    "final_insight": "Code ran but didn't assign response text to 'final_insight' variable."
                }
                
                # Execute script logic natively on your Mac device
                exec(raw_code, execution_context, execution_context)
                final_report = str(execution_context.get("final_insight"))
                
                status_placeholder.empty()
                st.markdown(final_report)
                
                st.download_button(
                    label="📥 Export Report to Markdown (.md)",
                    data=final_report,
                    file_name="helix_analytics_report.md",
                    mime="text/markdown"
                )
                
                st.session_state.chat_history.append({"role": "assistant", "content": final_report})

            except Exception as e:
                status_placeholder.empty()
                st.error(f"Local Execution Pipeline Error: {str(e)}")
