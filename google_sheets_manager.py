import gspread
from google.oauth2.service_account import Credentials
import hashlib
import logging
from datetime import datetime
from gspread_formatting import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("google_sheets_manager.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)

class GoogleSheetsManager:
    def __init__(self, credentials_file, sheet_name, worksheet_name):
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            # Define the scope
            self.scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            # Create credentials object
            self.creds = Credentials.from_service_account_file(credentials_file, scopes=self.scope)
            # Authorize the client
            self.client = gspread.authorize(self.creds)
            # Open the Google Sheet
            self.sheet = self.client.open(sheet_name).worksheet(worksheet_name)
            self.logger.info(f"Successfully connected to Google Sheet '{sheet_name}' and worksheet '{worksheet_name}'.")
            # Initialize the sheet with headers if it's empty
            self.initialize_sheet()
        except Exception as e:
            self.logger.error(f"Failed to connect to Google Sheet: {e}")
            raise

    def initialize_sheet(self):
        """Initialize the Google Sheet with headers and format if empty."""
        if not self.sheet.get_all_values():  # Check if the sheet is empty
            headers = ["Title", "Link", "Publication Date", "Summary", "Hash", "Timestamp"]
            self.sheet.append_row(headers)
            self.logger.info("Added headers to the Google Sheet.")
            self.format_headers()
    
    def format_headers(self):
        """Apply formatting to the header row."""
        try:
            header_format = cellFormat(
                backgroundColor=color(0.9, 0.9, 0.9),  # Light grey background
                textFormat=textFormat(bold=True),  # Bold text
                horizontalAlignment='CENTER'
            )
            format_cell_range(self.sheet, 'A1:F1', header_format)
            self.logger.info("Formatted header row.")
        except Exception as e:
            self.logger.error(f"Failed to format headers: {e}")

    def add_paper_to_sheet(self, paper):
        try:
            # Create a hash of the paper's title
            paper_hash = hashlib.md5(paper['title'].encode('utf-8')).hexdigest()
            # Get the current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Append the paper details to the sheet
            self.sheet.append_row([paper['title'], paper['link'], paper['publication_date'], paper['summary'], paper_hash, timestamp])
            self.logger.info(f"Successfully added paper '{paper['title']}' to the Google Sheet.")

            # Auto-resize columns to fit content
            self.auto_resize_columns()
        except Exception as e:
            self.logger.error(f"Failed to add paper '{paper['title']}' to the Google Sheet: {e}")

    def auto_resize_columns(self):
        """Auto-resize the columns to fit the content."""
        try:
            sheet_id = self.sheet.id
            body = {
                "requests": [{
                    "autoResizeDimensions": {
                        "dimensions": {
                            "sheetId": sheet_id,
                            "dimension": "COLUMNS",
                            "startIndex": 0,  # Start from the first column
                            "endIndex": 6     # End after the last column
                        }
                    }
                }]
            }
            self.sheet.spreadsheet.batch_update(body)
            self.logger.info("Auto-resized columns to fit content.")
        except Exception as e:
            self.logger.error(f"Failed to auto-resize columns: {e}")
