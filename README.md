# Data Engineer Assignment

## Overview
This repository contains my submission for the Data Engineer assignment. The project processes constituent and donation data to generate summarized output CSV files.

---

## Repository Explanation:
- load_excel.py – Helper code for reading Excel files
- process_cb.py  – Main script for processing constituent and donation data
- process_tags.py – Script for processing CB Tags data
- CB_Output1_Constituents.xlsx – Output file with processed constituent data
- CB_Output2_Tags.xlsx – Output file summarizing tags
- requirements.txt – Python dependencies

---

## How to Run

Steps (Please follow in the same order)
   
1. Clone this repo using command =>  git clone https://github.com/FnuPratichi/Data-Engineer-Assignment.git
   
2. Go to this directory => cd Data-Engineer-Assignment
   
3. Create a virtual environment using below commands in the order :
- python3 -m venv venv             => This command will create a venv named virtual env folder 
- source venv/bin/activate         => This command will activate your venv
   
4. Install dependenies using command  =>    pip install -r requirements.txt
   
5. Run these two file to get the output sheet
   -  python process_cb.py
   -  python process_tags.py



## Assumptions

1. Duplicate Patron IDs:  Found 2 duplicate IDs and assumed and kept only the first occurrence to maintain unique records.
2. First Name and Last Name: I assumed these names should be in "First Name" and "Last Name" form , so i cleaned it and kept first letter as capital.
3. Constituent Type (Person vs Company): For this, I observed 2 cases:  <a>. If first and last name → Person   <b>. If only company name → Company. But we had few rows where first name, last name and company name all are given, so in that case I assumed constituent type as Person
4. Date Formatting: I assumpted valid dates are in "YYYY-MM-DD" format and invalid or missing dates are left as empty strings.
5. Background information: For this I assumed if title and/or gender were empty fields ==> skipped.
6. Lifetime donation: I calculated it as sum of all paid donations


## Clarifying Questions for Client
1. If first and last name are given and If only company name is also given, in that case , if we assume constituent type as"Person" then should we generate company name for this patron id? Please check row 6 (Patron id: 5034)


## QA / Verification Process
1. In the python code, i have used print() to validate if my data frame had correct and expected answer. I have commented it out in my code, but if you want to validate , just uncomment it. Also I have checked few things manually since the dataset is not too large (Like duplicate ids, name formatting)


## AI  vs Me

I explored the input data on my own. Understood what needs to be done, explored all sheets and visualize the columns and how they can be mapped. After reading the instructions, i understood how to handle patron IDs (we wanted only unique one), how to clean email format, how to decide what could be the CB Constituent Type based on first/last names and what could be all possible assumptions.

I took the help of AI to revisite the regex patten structure that was need for email formatting, date formatting, processing excel sheets, troubleshooting, correcting the syntax errors.

