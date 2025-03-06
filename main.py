import fitz  # PyMuPDF
import pandas as pd
import csv
import mysql.connector
import re

# Load the PDF file
pdf_path = "Water_Rights_Application.pdf"
doc = fitz.open(pdf_path)

# Extract text from PDF
text = ""
for page in doc:
    text += page.get_text("text")

doc.close()

# Function to extract key details using regex
def extract_detail(pattern, text, default="N/A"):
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else default

# Extract details dynamically
owner_name = extract_detail(r"Name and Address:\n\s*([\w\s.]+)\n", text)
owner_address = extract_detail(r"Name and Address:\n[\w\s.]+\n\s*(.+)\n", text)
priority_date = extract_detail(r"Priority Date:\s*(\d{2}/\d{2}/\d{4})", text)
status = extract_detail(r"Status:\s*(\w+)", text)
source = extract_detail(r"Source:\s*([\w\s]+)", text)
county = extract_detail(r"County:\s*([\w\s]+)", text)
diversion_rate = extract_detail(r"Total Diversion\s*(\d+.\d+) CFS", text)
acres = extract_detail(r"Total Acres:\s*(\d+)", text)
township = extract_detail(r"Township:\s*(\w+)", text)
range = extract_detail(r"Range:\s*(\w+)", text)
section = extract_detail(r"Section:\s*(\w+)", text)
quarter = extract_detail(r"Quarter:\s*(\w+)", text)

# Prepare data for CSV
csv_data = [
    ["Owner Name", "Address", "Priority Date", "Status", "Source", "County", "Diversion Rate (CFS)", "Acres", "Township", "Range", "Section", "Quarter"],
    [owner_name, owner_address, priority_date, status, source, county, diversion_rate, acres, township, range, section, quarter]
]

# Save to CSV
csv_path = "water_rights_parcel.csv"
with open(csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

print(f"CSV file created: {csv_path}")

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",  # Change if needed
    user="your_username",  # Update with your MySQL username
    password="your_password",  # Update with your MySQL password
    database="waterrightsdb"
)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS water_rights (
        id INT AUTO_INCREMENT PRIMARY KEY,
        owner_name VARCHAR(255),
        address VARCHAR(255),
        priority_date DATE,
        status VARCHAR(50),
        source VARCHAR(100),
        county VARCHAR(100),
        diversion_rate FLOAT,
        acres INT,
        township VARCHAR(10),
        range VARCHAR(10),
        section VARCHAR(10),
        quarter VARCHAR(10)
    )
''')

# Insert data into the database
cursor.execute('''
    INSERT INTO water_rights (owner_name, address, priority_date, status, source, county, diversion_rate, acres, township, range, section, quarter)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
''', (owner_name, owner_address, priority_date, status, source, county, diversion_rate, acres, township, range, section, quarter))

conn.commit()
cursor.close()
conn.close()

print("Data inserted into MySQL database successfully.")
