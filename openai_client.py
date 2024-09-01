import requests
import fitz  # PyMuPDF
from io import BytesIO
from openai import OpenAI

class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def extract_text_from_pdf_url(self, pdf_url):
        # Fetch the PDF file from the URL
        response = requests.get(pdf_url)
        response.raise_for_status()  # Ensure the request was successful

        # Use BytesIO to read the PDF from memory
        pdf_file = BytesIO(response.content)

        # Open the PDF with PyMuPDF
        document = fitz.open(stream=pdf_file, filetype="pdf")

        # Extract text from each page
        text = ""
        for page_num in range(document.page_count):
            page = document[page_num]
            text += page.get_text()

        document.close()
        return text

    def summarize_paper(self, title, paper_text):
        # Create a structured prompt with the extracted text
        prompt = (
            f"Summarize the following paper in the format below:\n"
            f"Paper Title: {title}\n\n"
            f"Content:\n{paper_text}\n\n"
            f"1. Key Idea:\n"
            f"2. Motivation:\n"
            f"3. Experiments / Datasets / Evals:\n"
            f"4. Results:\n"
            f"5. Strengths and Weakness:\n"
            f"6. Conclusion:"
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Convert the response to a dictionary
        response_dict = response.to_dict()
        return response_dict['choices'][0]['message']['content']
