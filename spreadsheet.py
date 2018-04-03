#!/usr/bin/python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from management import * 
PATH = "/home/ubuntu/"

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(PATH + 'client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("ClassUCLA RSVP (Responses)").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(len(list_of_hashes))
#print(list_of_hashes)
with open(PATH + "data/downloaded.csv", "r+") as datafile:
    datafile.seek(0)
    datafile.truncate()
    datafile.write(sheet.export(format='csv'))

cell_list = sheet.range("A2:G"+str(len(list_of_hashes)+1))
for cell in cell_list:
    cell.value = ""
sheet.update_cells(cell_list)

ret,s = import_from_csv(PATH + "data/downloaded.csv")
if(ret != 0):
    sendEmail(str(ret) +"\n"+ s, "")
