import pandas as pd
import requests

# Load input Excel file
main_file = "Data Assignment.xlsx"
main_sheet = pd.read_excel(main_file, sheet_name=None)

constituents_df = main_sheet["Input Constituents"]
emails_df = main_sheet["Input Emails"]
donations_df = main_sheet["Input Donation History"]


# Standardize capitalization for names and company
constituents_df['First Name'] = constituents_df['First Name'].str.title()
constituents_df['Last Name'] = constituents_df['Last Name'].str.title()
constituents_df['Company'] = constituents_df['Company'].str.title()

# print(constituents_df['First Name'])
# print(constituents_df['Last Name'])


#1. This mapping is for CB Constituent ID to Patron ID (unique)
print(constituents_df["Patron ID"].is_unique) 
duplicate_ids = constituents_df[constituents_df.duplicated(subset="Patron ID", keep=False)]
print(duplicate_ids[["Patron ID", "First Name", "Last Name", "Company"]])
# Assumption1: Drop duplicates, keeping the first occurrence
constituents_df = constituents_df.drop_duplicates(subset="Patron ID", keep="first")
cb_df = pd.DataFrame()
cb_df["CB Constituent ID"]= constituents_df["Patron ID"]
# print(constituents_df["Patron ID"].is_unique) 


#2. This is to decide CB Constituent Type
def cb_type(row):
    if (pd.notna(row["First Name"])) or (pd.notna(row["Last Name"])):
        return "Person"
    else:
        return "Company"
cb_df["CB Constituent Type"] = constituents_df.apply(cb_type,axis=1)
cb_df["CB First Name"] = constituents_df["First Name"].where(cb_df["CB Constituent Type"]=="Person", "")
cb_df["CB Last Name"] = constituents_df["Last Name"].where(cb_df["CB Constituent Type"]=="Person", "")
cb_df["CB Company Name"] = constituents_df["Company"].where(cb_df["CB Constituent Type"]=="Company", "")
# print(cb_df["CB Constituent Type"])



#3. This is map created AT :: this has multiple date formats -- Assumption2: keeping "YYYY-MM-DD AND Empty string if invalid date "
cb_df['CB Created At'] = pd.to_datetime(
    constituents_df['Date Entered'], 
    errors='coerce').dt.strftime('%Y-%m-%d') 
cb_df['CB Created At'] = cb_df['CB Created At'].fillna('')



#4. Emails - Need to chceck valid emails first 
cb_df['Primary Email'] = constituents_df['Primary Email']
import re
def is_valid_email(email):
    if pd.isna(email) or email.strip() == '':
        return False
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return re.match(pattern, email.strip()) is not None


def map_emails(row):
    patron_id = row['CB Constituent ID']
    Email1 = ''
    Email2 = ''
    if is_valid_email(row['Primary Email']):
        Email1 = row['Primary Email'].strip().lower()  
        secondary_emails = emails_df[emails_df['Patron ID'] == patron_id]['Email'].tolist()
        for e in secondary_emails:
            e_std = e.strip().lower()
            if is_valid_email(e_std) and e_std != Email1:
                Email2 = e_std
                break
    return pd.Series([Email1, Email2])
cb_df[['CB Email 1', 'CB Email 2']] = cb_df.apply(map_emails, axis=1)




#5. Salutations - Assumptions: Mr.->Mr etc
valid_titles = {"Mr.", "Mrs.", "Ms.", "Dr."}
def standardize_title(title):
    if pd.isna(title) or title.strip() == "":
        return ""
    title = title.strip()
    if title in ["Mr", "Mr."]:
        return "Mr."
    elif title in ["Mrs", "Mrs."]:
        return "Mrs."
    elif title in ["Ms", "Ms."]:
        return "Ms."
    elif title == "Dr":
        return "Dr."
    else:
        return "" 
cb_df["CB Title"] = constituents_df["Salutation"].apply(standardize_title)


#6. CB Tags - REMOVED DUPLICATE TAGS, IGNORED ID FROM API
import requests
TAG_URL = "https://6719768f7fc4c5ff8f4d84f1.mockapi.io/api/v1/tags"
resp = requests.get(TAG_URL)
tags_data = resp.json()
tag_map = {
    t["name"].strip().lower(): t["mapped_name"].strip()
    for t in tags_data
}
def map_tags(raw_tags):
    if pd.isna(raw_tags) or raw_tags.strip() == "":
        return ""
    mapped = []
    for tag in raw_tags.split(","):
        key = tag.strip().lower()
        if key in tag_map:
            mapped.append(tag_map[key])
    mapped = list(dict.fromkeys(mapped))
    return ", ".join(mapped)
cb_df["CB Tags"] = constituents_df["Tags"].apply(map_tags)



#7. CB Background 
def build_background_info(row):
    job = row.get("Title")
    marital = row.get("Gender")
    parts = []
    if pd.notna(job) and str(job).strip() != "":
        parts.append(f"Job Title: {job.strip()}")
    if pd.notna(marital) and str(marital).strip() != "":
        parts.append(f"Marital Status: {marital.strip()}")
    return "; ".join(parts)
cb_df["CB Background Information"] = constituents_df.apply(build_background_info, axis=1)
print(cb_df["CB Background Information"])


#8. CB life time Donation
def get_lifetime_donation(row, donations_df):
    patron_id = row["Patron ID"]
    patron_donations = donations_df[donations_df["Patron ID"] == patron_id]
    patron_donations = patron_donations[patron_donations["Status"] == "Paid"]
    if patron_donations.empty:
        return ""
    total = patron_donations["Donation Amount"].replace('[\$,]', '', regex=True).astype(float).sum()
    return f"${total:,.2f}"
cb_df["CB Lifetime Donation Amount"] = constituents_df.apply(
    lambda row: get_lifetime_donation(row, donations_df), axis=1
)


#9 CB Most Recent Donation Date
def get_most_recent_donation_date(row, donations_df):
    patron_id = row["Patron ID"]
    patron_donations = donations_df[donations_df["Patron ID"] == patron_id]
    patron_donations = patron_donations[patron_donations["Status"] == "Paid"]
    if patron_donations.empty:
        return ""
    patron_donations["Donation Date"] = pd.to_datetime(patron_donations["Donation Date"])
    latest_date = patron_donations["Donation Date"].max()
    return latest_date.strftime("%Y-%m-%d")
cb_df["CB Most Recent Donation Date"] = constituents_df.apply(
    lambda row: get_most_recent_donation_date(row, donations_df), axis=1
)


#10 CB Most Recent Donation Amount
def get_most_recent_donation_amount(row, donations_df):
    patron_id = row["Patron ID"]
    patron_donations = donations_df[(donations_df["Patron ID"] == patron_id) & (donations_df["Status"] == "Paid")]
    if patron_donations.empty:
        return ""
    patron_donations = patron_donations.copy()
    patron_donations["Donation Date"] = pd.to_datetime(patron_donations["Donation Date"])
    latest_row = patron_donations.loc[patron_donations["Donation Date"].idxmax()]
    amount = float(str(latest_row["Donation Amount"]).replace('$','').replace(',',''))
    return f"${amount:,.2f}"
cb_df["CB Most Recent Donation Amount"] = constituents_df.apply(
    lambda row: get_most_recent_donation_amount(row, donations_df), axis=1
)


output_file = "CB_Output1_Constituents.xlsx"
cb_df.to_excel(output_file, index=False)
print(f"Output saved to {output_file}")
