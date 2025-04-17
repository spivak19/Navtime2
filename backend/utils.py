# backend/utils.py
import os
from datetime import datetime
import getpass
from docx import Document
import csv
from pyluach import dates, hebrewcal

# Define directories relative to this file
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
OUTPUT_DIR = os.path.join(os.getcwd(), 'files')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def create_document(template_name, additional_keywords="", new_filename=None):
    """
    Opens a DOCX template, replaces the placeholder [date] with the current date,
    then saves the new document using the provided new_filename (if given).
    """
    template_path = os.path.join(TEMPLATE_DIR, template_name)
    doc = Document(template_path)
    # Format the current date as yyyy-mm-dd (display in the document)
    current_date_display = datetime.now().strftime('%Y-%m-%d')
    
    csv_path = os.path.join(os.path.dirname(__file__), 'user_abbreviations.csv')
    username = getpass.getuser()

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Compare usernames case-insensitively.
            if row and row[0].strip().lower() == username.lower():
                HebrewName = row[3].strip() + " " + row[4].strip()
                rank = row[6].strip()
                title = row[7].strip()
    
    for para in doc.paragraphs:
        if '[date]' in para.text:
            para.text = para.text.replace('[date]', current_date_display)
        if '[simuchin]' in para.text:
            para.text = para.text.replace('[simuchin]', new_filename)
        if '[doctitle]' in para.text:
            para.text = para.text.replace('[doctitle]', additional_keywords)
        if '[Hebrew date]' in para.text:
            todayHebrew = dates.HebrewDate.today()
            Hdate = str(todayHebrew.hebrew_date_string())
            para.text = para.text.replace('[Hebrew date]', Hdate)

        if '[Hebrew name]' in para.text:
            para.text = para.text.replace('[Hebrew name]', HebrewName)
            
        if '[rank]' in para.text:
            para.text = para.text.replace('[rank]', rank)
        if '[title]' in para.text:
            para.text = para.text.replace('[title]', title)


    # If new_filename is provided, use it (append .docx); otherwise, fall back to default naming.
    
    if new_filename:
        file_name = new_filename + ".docx"
    else:
        # Fallback default naming if needed
        file_name = "NV-" + datetime.now().strftime('%Y%m%d%H%M%S') + ".docx"
    output_path = os.path.join(OUTPUT_DIR, file_name)
    
    doc.save(output_path)
    
    return {
        "file_name": file_name,
        "file_path": output_path,
        "created_at": current_date_display,
        "user": getpass.getuser(),
        "keywords": additional_keywords
    }
