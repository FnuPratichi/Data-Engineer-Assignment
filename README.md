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
  
