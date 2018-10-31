#!/usr/bin/python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from management import * 
PATH = "/root/"

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
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
    #print(sheet.get_all_records(head = 1))
    for i in sheet.get_all_records(head = 1):
        print(i)
        datafile.write(",".join([str(x) for x in [i["1"],i["2"],i["3"],i["4"],i["5"],i["6"],i["7"]]]))
        datafile.write("\n")

cell_list = sheet.range("A2:G"+str(len(list_of_hashes)+1))
for cell in cell_list:
    cell.value = ""
sheet.update_cells(cell_list)

ret,s = import_from_csv(PATH + "data/downloaded.csv")
if(ret != 0):
    sendEmail(str(ret) +"\n"+ s, "")

