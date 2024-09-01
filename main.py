from arxiv_client import ArxivClient
from openai_client import OpenAIClient
from db_manager import DatabaseManager
from google_sheets_manager import GoogleSheetsManager
import os
from dotenv import load_dotenv

# Load environment variables from the configuration file
load_dotenv('config.env')

def main():
    # Initialize clients
    arxiv_client = ArxivClient(search_query="reasoning", max_results=3)
    openai_client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
    db_manager = DatabaseManager(
        db_name=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    # Initialize Google Sheets Manager for the specified sheet and tab
    sheets_manager = GoogleSheetsManager(
        credentials_file=os.getenv("SHEETS_CREDENTIALS_FILE"),
        sheet_name=os.getenv("SHEETS_NAME"),
        worksheet_name=os.getenv("SHEETS_WORKSHEET")
    )

    # Create database table if it does not exist
    db_manager.create_table()

    # Fetch and process papers
    arxiv_response = arxiv_client.fetch_papers()
    if not arxiv_response:
        return

    papers = arxiv_client.parse_papers(arxiv_response)
    for paper in papers:
        if db_manager.paper_exists(paper['title']):
            print(f"Paper '{paper['title']}' already exists in the database.")
            continue

        # Extract the actual content of the paper from the PDF URL
        pdf_url = paper['link'].replace('abs', 'pdf') + ".pdf"  # Convert to direct PDF URL
        paper_text = openai_client.extract_text_from_pdf_url(pdf_url)

        # Summarize the paper using the actual text content
        summary = openai_client.summarize_paper(paper['title'], paper_text)
        paper['summary'] = summary
        db_manager.save_paper(paper)
        print(f"Title: {paper['title']}\nLink: {paper['link']}\nPublication Date: {paper['publication_date']}\nSummary: {paper['summary']}\n")

        # Add to Google Sheet in the "auto" tab
        sheets_manager.add_paper_to_sheet(paper)

    # Close database connection
    db_manager.close()

if __name__ == "__main__":
    main()
