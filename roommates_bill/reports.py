import webbrowser
import os

from filestack import Client
from fpdf import FPDF


class PdfReport:
    """
    Creates a Pdf file that contains data about
    the roommates such as their names, their due amounts
    and the period of the bill.
    """

    def __init__(self, filename):
        self.filename = filename

    def generate(self, roommate1, roommate2, bill):

        roommate1_pay = str(round(roommate1.pays(bill, roommate2), 2))
        roommate2_pay = str(round(roommate2.pays(bill, roommate1), 2))

        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        # Add icon
        pdf.image("files/house.png", w=30, h=30)

        # Insert title
        pdf.set_font(family='Times', size=24, style='B')
        pdf.cell(w=0, h=80, txt="Flatmates Bill", border=0, align="C", ln=1)

        # Insert Period label and value
        pdf.set_font(family="Times", size=14, style='B')
        pdf.cell(w=100, h=40, txt="Period:", border=0)
        pdf.cell(w=150, h=40, txt=bill.period, border=0, ln=1)

        # Insert name and due amount of the first flatmate
        pdf.set_font(family="Times", size=12)
        pdf.cell(w=100, h=25, txt=roommate1.name, border=0)
        pdf.cell(w=150, h=25, txt=roommate1_pay, border=0, ln=1)

        # Insert name and due amount of the first flatmate
        pdf.cell(w=100, h=25, txt=roommate2.name, border=0)
        pdf.cell(w=150, h=25, txt=roommate2_pay, border=0, ln=1)

        # Change directory to files, generate and open the PDF
        os.chdir("files")
        pdf.output(self.filename)
        webbrowser.open(self.filename)


class FileSharer:

    def __init__(self, filepath, api_key="AViVqp7suSQWWEdrl6hf9z"):
        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        client = Client(self.api_key)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url