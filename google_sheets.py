import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
import json

# Load environment variables from .env (works locally)
load_dotenv()

# Define Google Sheets API scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Get the Sheet ID from environment variable
SPREADSHEET_ID = os.getenv("SHEET_ID")

# Load credentials based on environment
if os.getenv("ENV") == "REPLIT":
    # Replit environment: Load JSON from secret
    service_account_info = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
    credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
else:
    # Local environment: Load from .json file
    SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Authorize the gspread client
client = gspread.authorize(credentials)

# Access the first sheet
sheet = client.open_by_key(SPREADSHEET_ID).sheet1
