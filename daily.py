import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client
import datetime
import os
from dotenv import load_dotenv
import traceback

# Load environment variables from .env file
load_dotenv()

spScore = 12
stScore = 15

try:
    # Set up Google Sheets API client
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("CREDENTIALS_FILE"), scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet and worksheet
    spreadsheet = client.open(os.getenv('SS_NAME_1'))
    sheet_name = "template"
    sheet = spreadsheet.worksheet(sheet_name)

    # Find today's column index
    today_str = datetime.datetime.today().date().day

    print(today_str)
    date_row = sheet.row_values(5)[2:9]  # Columns C to I

    todayDateInd = -1
    for idx, cell_date in enumerate(date_row):
        try:
            formatted_date = cell_date[5:7]
            print(formatted_date)
            if int(formatted_date) == int(today_str)-1:
                todayDateInd = idx + 2  # Adjusting for actual column index
                break
        except ValueError:
            continue

    if todayDateInd == -1:
        print("Today's date not found in the template sheet.")
    else:
        print(f"Found today's column index: {todayDateInd + 1}")
        
        data = dict()
        sanatanGrp = ['Prince Pr', 'Raghav Pr', 'Sahil Pr', 'Shashank Pr', 'Varun Pr', 'Vishal Pr']
        rupaGrp = ['Basavesh Pr', 'Nandish Pr', 'Manjunath Pr', 'Nishant Pr']

        ss1 = client.open(os.getenv("SS_NAME_1"))
        ss2 = client.open(os.getenv("SS_NAME_2"))

        for sheetName in sanatanGrp:
            sheet = ss1.worksheet(sheetName)
            data[sheetName] = [sheet.row_values(stScore)[todayDateInd], sheet.row_values(spScore)[todayDateInd]]

        for sheetName in rupaGrp:
            sheet = ss2.worksheet(sheetName)
            data[sheetName] = [sheet.row_values(stScore)[todayDateInd], sheet.row_values(spScore)[todayDateInd]]

        print("Collected Data:")
        print(data)

        study_sorted = sorted(data.items(), key=lambda x: float(x[1][0]), reverse=True)
        sp_sorted = sorted(data.items(), key=lambda x: float(x[1][1]), reverse=True)

        # Create message parts
        study_message = "📘 *Study Score*\n"
        for name, (study, _) in study_sorted:
            study_message += f"{name} scored {study} hours\n"

        sp_message = "📖 *SP Book Reading*\n"
        for name, (_, sp) in sp_sorted:
            sp_message += f"{name} scored {sp} min\n"

        # Combine both messages
        message = study_message + "\n" + sp_message
        print(message)

        print(f"Message Ready:\n{message}")
        print("Sending SMS...")

        TWILIO_SID = os.getenv('TWILIO_SID')
        TWILIO_AUTH_TOKEN = os.getenv('TWILIO_TOKEN')
        TWILIO_PHONE_NUMBER = os.getenv('TWILIO_FROM')
        recipient_number = os.getenv('TWILIO_TO')

        twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        twilio_message = twilio_client.messages.create(
            body=message,
            from_='whatsapp:' + TWILIO_PHONE_NUMBER,
            to='whatsapp:' + recipient_number
        )
        print(f"Message sent to {recipient_number}: {twilio_message.sid}")

    print('exit')

except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()