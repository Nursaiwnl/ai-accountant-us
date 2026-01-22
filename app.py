import streamlit as st
from accountant.agent import run_accountant, explain_expense
from accountant.report import generate_pdf

st.set_page_config(page_title="AI Accountant US", layout="wide")
st.title("🧠💼 AI Accountant (US)")

uploaded_file = st.file_uploader("Upload transactions CSV", type=["csv"])

if uploaded_file:
    st.info("LLM will analyze descriptions first, then agent will calculate numbers.")

    # Запуск агента
    result = run_accountant(uploaded_file)

    st.subheader("Summary")
    st.metric("Income", f"${result['income']}")
    st.metric("Expenses", f"${result['expenses']}")
    st.metric("Net income", f"${result['net_income']}")

    st.subheader("Estimated taxes")
    st.json(result["taxes"])

    st.subheader("Transactions with LLM analysis")
    st.dataframe(result["table"])

    # Текстовое объяснение (первой транзакции для примера)
    st.subheader("💬 Explanation from AI")
    if st.button("Generate textual explanation for first expense"):
        explanation = explain_expense(result["table"].iloc[0])
        st.write(explanation)

    # PDF
    st.subheader("📄 Download PDF report")
    if st.button("Generate PDF report"):
        path = generate_pdf(result)
        with open(path, "rb") as f:
            st.download_button("Download report", f, file_name="report.pdf")
