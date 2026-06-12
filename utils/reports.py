from reportlab.pdfgen import canvas
import pandas as pd


def generate_pdf_report(filename="report.pdf"):

    c = canvas.Canvas(filename)

    c.drawString(
        100,
        750,
        "Sales Forecast Report"
    )

    c.save()

    return filename


def generate_excel_report(df, filename="report.xlsx"):

    df.to_excel(
        filename,
        index=False
    )

    return filename


def generate_csv_report(df, filename="report.csv"):

    df.to_csv(
        filename,
        index=False
    )

    return filename