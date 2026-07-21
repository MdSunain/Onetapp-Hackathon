import streamlit as st
from utils.chart import render_chart
from utils.helpers import ask_business_assistant
from utils.planner import plan_analysis
from utils.renderer import render_layout

st.set_page_config(
    page_title="Business Analytics AI",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Business Analytics AI")
st.caption(
    "Ask natural language questions about promotions, sales, inventory and regional performance."
)

st.divider()

question = st.chat_input("Ask a business question...")

# st.write("### Quick Questions")

# cols = st.columns(5)

# examples = [
#     "Promotion Effectiveness",
#     "Regional Sales",
#     "Inventory Reduction",
#     "Beverage Performance",
#     "Weekly Sales"
# ]

# clicked = None

# for col, text in zip(cols, examples):
#     if col.button(text, use_container_width=True):
#         clicked = text

# if clicked:
#     question = clicked
with st.sidebar:

    st.header("⚙️ AI Workflow")

    st.markdown("""
1. 🧠 Planner Agent
2. 🗄️ SQL Generator
3. 📊 Analytics Engine
4. 💡 Insight Generator
5. 🎨 Dashboard Renderer
6. 📄 Report Generator
""")
    st.divider()


USE_MOCK = False

if question:
    if question:

        with st.status("Analyzing..."):

            if USE_MOCK:
                from utils.sample_response import PLAN, RESPONSE
                plan = PLAN
                response = RESPONSE

            else:
                plan = plan_analysis(question)
                response = ask_business_assistant(question)

        if not response["success"]:
            st.error(response["error"])
            st.stop()

        render_layout(
            plan,
            response,
            question
        )
    