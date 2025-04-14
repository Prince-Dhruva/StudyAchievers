import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

def extractData(ssName,row1,row2,col1,col2):
    
    for i,ss in enumerate(ssName):
        if i==0:
            row1_data = ss.row_values(row1)[col1-1:col2]
            row2_data = ss.row_values(row2)[col1-1:col2]
            continue
        row1_data += ss.row_values(row1)[col1-1:col2]
        row2_data += ss.row_values(row2)[col1-1:col2]
    return row1_data,row2_data


def main(ssName,sheet,rankListName,row1,row2,col1,col2):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("CREDENTIALS_FILE"),scope)
    client = gspread.authorize(creds)
    print("Authorisation completed")
    print(f"opening Sheet:{ssName[0]}:",end="")
    sheet1 = client.open(ssName[0]).worksheet(sheet)
    print("SUcessfull")
    print(f"opening Sheet:{ssName[1]}:",end="")
    sheet2 = client.open(ssName[1]).worksheet(sheet)
    print("SUcessfull")

    row1_data,row2_data = extractData([sheet1,sheet2],row1,row2,col1,col2)

    print('Data Extracted')
    data_dict = {k:float(v) for k,v in zip(row1_data,row2_data) if k and v}
    sorted_items = sorted(data_dict.items(),key=lambda x: x[1])
    sorted_items = sorted_items[::-1]
    print("Rank list generated")
    message = f"{rankListName} of this week:\n"
    i=0
    for key,value in sorted_items:
        message += f"{i+1}: {key} scored {value}\n"
        i+=1
    print("Message written")
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_TOKEN")
    from_number = os.getenv("TWILIO_FROM")
    to_number = os.getenv("TWILIO_TO")
    print("Message ready to send")

    client = Client(account_sid,auth_token)
    client.messages.create(body=message,from_=from_number,to=to_number)
    print("Message sent")

if __name__ == '__main__':
    print("Start")
    ssName1 = os.getenv("SS_NAME_1")
    ssName2 = os.getenv("SS_NAME_2")
    sheet = os.getenv("SHEET")
    print("Env variables Opened:",[ssName1,ssName2],sheet)
    main([ssName1,ssName2],sheet,"Study Acheivers",25,32,3,8)
    main([ssName1,ssName2],sheet,"SP Book Reading Acheivers",25,30,3,8)


