# StudyAchievers

A Python application that generates and sends rank lists for study achievers and SP book reading toppers on a weekly basis. The application reads data from Google Sheets and sends the rankings via Twilio SMS.

## Features

- Fetches data from multiple Google Sheets
- Generates rank lists based on scores
- Automatically sends rankings via SMS using Twilio
- Supports multiple ranking categories (Study Achievers and SP Book Reading)

## Prerequisites

- Python 3.x
- Google Sheets API credentials
- Twilio account

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd StudyAchievers
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in the required values in `.env`:
     ```
     CREDENTIALS_FILE=credentials.json
     TWILIO_SID=your_twilio_sid
     TWILIO_TOKEN=your_twilio_auth_token
     TWILIO_FROM=your_twilio_phone_number
     TWILIO_TO=recipient_phone_number
     SS_NAME_1=first_spreadsheet_name
     SS_NAME_2=second_spreadsheet_name
     SHEET=worksheet_name
     ```

4. Set up Google Sheets API:
   - Create a Google Cloud Project
   - Enable Google Sheets API
   - Create service account credentials
   - Download the credentials JSON file and save it as `credentials.json` in the project root

## Environment Configuration

### Setting up Base64 Encoded Configurations

The project uses base64 encoding for secure storage of configuration files. Here's how to generate and use them:

#### For macOS/Linux:

1. Generate base64 for `.env`:
```bash
base64 .env > .env.b64
```

2. Generate base64 for `credentials.json`:
```bash
base64 credentials.json > credentials.b64
```

3. To decode when needed:
```bash
base64 -d .env.b64 > .env
base64 -d credentials.b64 > credentials.json
```

#### For Windows (PowerShell):

1. Generate base64 for `.env`:
```powershell
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content -Path ".env" -Raw))) | Set-Content -Path ".env.b64"
```

2. Generate base64 for `credentials.json`:
```powershell
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content -Path "credentials.json" -Raw))) | Set-Content -Path "credentials.b64"
```

3. To decode when needed:
```powershell
[System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String((Get-Content -Path ".env.b64"))) | Set-Content -Path ".env"
[System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String((Get-Content -Path "credentials.b64"))) | Set-Content -Path "credentials.json"
```

### GitHub Repository Secrets

Add the following secrets to your GitHub repository (Settings > Secrets and Variables > Actions):

1. `ENV_B64`: The base64 encoded content of your `.env` file
   - Get the content: `cat .env.b64` (macOS/Linux) or `Get-Content .env.b64` (Windows PowerShell)
   - Copy the output and add it as a secret

2. `GSPREAD_CREDS_B64`: The base64 encoded content of your `credentials.json` file
   - Get the content: `cat credentials.b64` (macOS/Linux) or `Get-Content credentials.b64` (Windows PowerShell)
   - Copy the output and add it as a secret

### Setting up GitHub Actions Workflow

1. Create the workflow directory:
```bash
mkdir -p .github/workflows
```

2. Create the workflow file:
```bash
touch .github/workflows/run-sheet.yaml
```

3. Copy the following content into `run-sheet.yaml`:
```yaml
name: Run main.py

on:
  workflow_dispatch:  # adds "Run workflow" button in GitHub

jobs:
  run-script:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Decode .env from GitHub Secret
        run: echo "${{ secrets.ENV_B64 }}" | base64 -d > .env

      - name: Decode credentials.json from GitHub Secret
        run: echo "${{ secrets.GSPREAD_CREDS_B64 }}" | base64 -d > credentials.json

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run main.py
        run: python main.py
```

4. Commit and push the workflow file:
```bash
git add .github/workflows/run-sheet.yaml
git commit -m "Add GitHub Actions workflow"
git push
```

The workflow will be available in your GitHub repository under the "Actions" tab. You can manually trigger it using the "Run workflow" button.

## Usage

Run the script using:
```bash
python main.py
```

The script will:
1. Connect to the specified Google Sheets
2. Extract scores from the specified rows and columns
3. Generate rank lists for both Study Achievers and SP Book Reading
4. Send the rankings via SMS using Twilio

## Configuration

The main script uses the following parameters:
- Row positions: 25, 32 (Study Achievers), 25, 30 (SP Book Reading)
- Column range: 3 to 8
- Sheet names and worksheet are configured via environment variables

## Troubleshooting

1. Make sure all environment variables are properly set in the `.env` file
2. Verify that the `credentials.json` file is present and contains valid Google API credentials
3. Check if the Google Sheets API is enabled in your Google Cloud Console
4. Ensure your Twilio credentials are correct and the phone numbers are in the proper format

### Important Security Notes:

1. Never commit the original `.env` and `credentials.json` files to the repository
2. Add these files to your `.gitignore`:
   ```
   .env
   credentials.json
   ```

3. Only commit the base64 encoded files if your repository is private
4. Regularly rotate your credentials and update the base64 encoded files
5. Use GitHub Secrets for sensitive information in CI/CD pipelines

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
