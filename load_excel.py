import pandas as pd

main_file= "Data Assignment.xlsx"
main_sheet = pd.read_excel(main_file, sheet_name=None)  # its a dict


print("Sheet names found in Excel:")
for sheet in main_sheet.keys():
    print(sheet)


# Constituents input sheet
# c_input = list(main_sheet.keys())[1]

constituents_input_df = main_sheet["Input Constituents"]
print("Rows*Cols:", constituents_input_df.shape)
print("Columns:", constituents_input_df.columns.tolist())
print(constituents_input_df.head(5))


#Email input sheet
emails_input_df = main_sheet["Input Emails"]
print("Rows x Cols:", emails_input_df.shape)
print("Columns:", emails_input_df.columns.tolist())
print(emails_input_df.head(5))


#Donation input sheet
donations_history_input_df = main_sheet["Input Donation History"]
print("Rows x Cols:", donations_history_input_df.shape)
print("Columns:", donations_history_input_df.columns.tolist())
print(donations_history_input_df.head(5))



