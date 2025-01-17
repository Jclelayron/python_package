import os

import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdfs_path, image_path, product_id, product_name,
             amount_purchased, price_per_unit, total_price):
    """
    This function converts invoice Excel files into PDF invoices.
    """
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")
    print(filepaths)

    for filepath in filepaths:
        filename = Path(filepath).stem
        invoice_num, date= str(filename).split("-")
        
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt= f"Invoice nr.{invoice_num}",ln=1)
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt= f"Date: {date}", ln=1)
        pdf.ln(10)

        df = pd.read_excel(filepath, sheet_name="Sheet 1") 
        raw_columns = list(df.columns)
        columns = [item.replace("_"," ").title() for item in raw_columns]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=str(columns[0]), border=1)
        pdf.cell(w=70, h=8, txt=str(columns[1]), border=1)
        pdf.cell(w=30, h=8, txt=str(columns[2]), border=1)
        pdf.cell(w=30, h=8, txt=str(columns[3]), border=1)
        pdf.cell(w=30, h=8, txt=str(columns[4]), border=1)
        pdf.ln(8)
        for index,row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1)
            pdf.ln(8)

        total_sum = df[total_price].sum()
        pdf.set_font(family="Times", size=10, style="B") 
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=70, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1)
        pdf.ln(20)

        #Add total sum sentence
        pdf.set_font(family="Times",size=10, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}", ln=1)

        #Add company name and logo
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=25, h=8, txt=f"PythonHow")
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")
