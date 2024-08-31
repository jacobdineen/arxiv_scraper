import requests

class ArxivClient:
    ARXIV_BASE_URL = "http://export.arxiv.org/api/query?"

    def __init__(self, search_query, max_results=1):
        self.search_query = search_query
        self.max_results = max_results

    def fetch_papers(self):
        # Construct query URL
        query = f"{self.ARXIV_BASE_URL}search_query={self.search_query}&start=0&max_results={self.max_results}"
        response = requests.get(query)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to fetch papers from arXiv.")
            return None

    def parse_papers(self, arxiv_response):
        papers = []
        entries = arxiv_response.split('<entry>')
        for entry in entries[1:]:
            title_start = entry.find('<title>') + 7
            title_end = entry.find('</title>')
            title = entry[title_start:title_end].strip()

            link_start = entry.find('<link href="') + 12
            link_end = entry.find('"/>', link_start)
            link = entry[link_start:link_end].strip()

            # Extract publication date
            pub_date_start = entry.find('<published>') + 11
            pub_date_end = entry.find('</published>', pub_date_start)
            publication_date = entry[pub_date_start:pub_date_end].strip()

            if title and link:
                papers.append({
                    'title': title,
                    'link': link,
                    'publication_date': publication_date  # Include publication date
                })
        return papers
