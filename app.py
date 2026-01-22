import streamlit as st
from accountant.agent import run_accountant, explain_expense
from accountant.report import generate_pdf

st.set_page_config(page_title="AI Accountant US", layout="wide")
st.title("🧠💼 AI Accountant (US)")

uploaded_file = st.file_uploader("Upload transactions CSV", type=["csv"])

if uploaded_file:
    result = run_accountant(uploaded_file)

    st.subheader("Summary")
    st.metric("Income", f"${result['income']}")
    st.metric("Expenses", f"${result['expenses']}")
    st.metric("Net income", f"${result['net_income']}")

    st.subheader("Estimated taxes")
    st.json(result["taxes"])

    st.subheader("Transactions")
    st.dataframe(result["table"])

    st.subheader("💬 Ask accountant")
    question = st.text_input("Ask about an expense or tax logic")

    if question:
        answer = explain_expense(result["table"].iloc[0])
        st.write(answer)

    if st.button("📄 Generate PDF report"):
        path = generate_pdf(result)
        with open(path, "rb") as f:
            st.download_button("Download report", f, file_name="report.pdf")
