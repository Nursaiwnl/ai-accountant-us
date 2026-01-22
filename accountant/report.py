from fpdf import FPDF

def generate_pdf(result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "AI Accountant US - Summary Report", ln=True)

    pdf.cell(200, 10, f"Income: ${result['income']}", ln=True)
    pdf.cell(200, 10, f"Expenses: ${result['expenses']}", ln=True)
    pdf.cell(200, 10, f"Net income: ${result['net_income']}", ln=True)

    pdf.cell(200, 10, "Estimated taxes:", ln=True)
    for k, v in result["taxes"].items():
        pdf.cell(200, 10, f"{k}: ${v}", ln=True)

    path = "report.pdf"
    pdf.output(path)
    return path
