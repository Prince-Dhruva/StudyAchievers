import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

def extractData(ssName,row1,row2,col1,col2):
    # For different Group or sheets we are extracting data
    for i,ss in enumerate(ssName):
        if i==0:
            row1_data = ss.row_values(row1)[col1-1:col2]
            row2_data = ss.row_values(row2)[col1-1:col2]
            continue
        row1_data += ss.row_values(row1)[col1-1:col2]
        row2_data += ss.row_values(row2)[col1-1:col2]
    return row1_data,row2_data


def main(ssName:list,sheet,rankListName:list,row1,row2:list,col1,col2):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("CREDENTIALS_FILE"),scope)
    client = gspread.authorize(creds)
    print("Authorisation completed",flush=True)
    print(f"opening Sheet:{ssName[0]}:",end="",flush=True)
    sheet1 = client.open(ssName[0]).worksheet(sheet)
    print("SUcessfull",flush=True)
    print(f"opening Sheet:{ssName[1]}:",end="")
    sheet2 = client.open(ssName[1]).worksheet(sheet)
    print("SUcessfull",flush=True)
    message="X-----X-----X-----X-----X\n"
    for i,ss in enumerate(ssName):
        row1_data,row2_data = extractData([sheet1,sheet2],row1,row2[i],col1,col2)

        print('Data Extracted',flush=True)
        data_dict = {k:float(v) for k,v in zip(row1_data,row2_data) if k and v}
        sorted_items = sorted(data_dict.items(),key=lambda x: x[1])
        sorted_items = sorted_items[::-1]
        print("Rank list generated",flush=True)
        message += f"{rankListName[i]} of this week:\n"
        i=0
        for key,value in sorted_items:
            message += f"{i+1}: {key} scored {value}\n"
            i+=1
        print("Message written",flush=True)
        message+="-----X-----X-----X-----X\n"
        print(message,flush=True)
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_TOKEN")
    from_number = os.getenv("TWILIO_FROM")
    to_number = os.getenv("TWILIO_TO")
    print("Message ready to send")

    client = Client(account_sid,auth_token)
    print(client,flush=True)
    client.messages.create(body=message,from_='whatsapp:'+from_number,to='whatsapp:'+to_number)
    print("Message sent",flush=True)

if __name__ == '__main__':
    print("Start")
    ssName1 = os.getenv("SS_NAME_1")
    ssName2 = os.getenv("SS_NAME_2")
    sheet = os.getenv("SHEET")
    print("Env variables Opened:",[ssName1,ssName2],sheet,flush=True)

    main([ssName1,ssName2],sheet,["Study Acheivers","SP Book Reading Acheivers"],25,[32,30],3,8)
    # main([ssName1,ssName2],sheet,"SP Book Reading Acheivers",25,30,3,8)


