import csv
from fpdf import FPDF
from collections import defaultdict

# Step 1: Read and process data
def read_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['Score'] = int(row['Score'])
            data.append(row)
    return data

# Step 2: Analyze data
def analyze_data(data):
    summary = {
        "Total Students": len(data),
        "Average Score": round(sum(d['Score'] for d in data) / len(data), 2),
        "Highest Scorer": max(data, key=lambda x: x['Score'])['Name']
    }

    by_department = defaultdict(list)
    for row in data:
        by_department[row['Department']].append(row['Score'])

    summary['Average Score by Department'] = {
        dept: round(sum(scores)/len(scores), 2)
        for dept, scores in by_department.items()
    }

    return summary

# Step 3: Create PDF report
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "CodTech Internship - Automated Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_summary(self, summary):
        self.set_font("Arial", "", 12)
        for key, value in summary.items():
            if isinstance(value, dict):
                self.cell(0, 10, f"{key}:", ln=True)
                for sub_key, sub_value in value.items():
                    self.cell(0, 10, f"  {sub_key}: {sub_value}", ln=True)
            else:
                self.cell(0, 10, f"{key}: {value}", ln=True)

# Step 4: Generate report
def generate_pdf(summary, output_path="report_sample.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_summary(summary)
    pdf.output(output_path)

# Run all steps
if __name__ == "__main__":
    data = read_data("data.csv")
    summary = analyze_data(data)
    generate_pdf(summary)
    print("PDF report generated successfully!")
