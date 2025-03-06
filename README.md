Water Rights Parser & Importer

Overview

This script extracts key details from a water rights application PDF, generates a CSV file for GIS import, and inserts the extracted data into a MySQL database.

Features

Automatically extracts owner details, priority date, water source, and parcel info.

Generates a structured CSV that can be imported into ArcGIS Online.

Inserts extracted data into a MySQL database for storage and querying.

Requirements

Python 3.x

Required libraries:

pymupdf (for PDF parsing)

pandas (for data handling)

mysql-connector-python (for MySQL interaction)

Install dependencies using:

pip install pymupdf pandas mysql-connector-python

Usage

Update MySQL Credentials

Open the script and modify the host, user, password, and database fields to match your MySQL setup.

Run the Script

python extract_water_rights.py

Check Outputs

A water_rights_parcel.csv file will be created.

Data will be inserted into the water_rights table in MySQL.

Database Schema

The MySQL table water_rights is structured as follows:

Column

Type

id

INT (Primary Key, Auto Increment)

owner_name

VARCHAR(255)

address

VARCHAR(255)

priority_date

DATE

status

VARCHAR(50)

source

VARCHAR(100)

county

VARCHAR(100)

diversion_rate

FLOAT

acres

INT

township

VARCHAR(10)

range

VARCHAR(10)

section

VARCHAR(10)

quarter

VARCHAR(10)

Notes

Ensure the PDF format remains consistent for accurate extraction.

Future improvements can include shapefile creation for direct GIS compatibility.

License

MIT License
