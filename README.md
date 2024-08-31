# arxiv_scraper
A simple package to scrape arxiv papers, use openai to summarize them, and put them in a google sheet.

`python main.py` will scrape the arxiv papers, summarize them with openai, and put them in a google sheet.

Requires a `config.env` file, a postgres db setup, and a google sheets api key.:
```
OPENAI_API_KEY=
DB_NAME=
DB_USER=
DB_PASSWORD=
SHEETS_CREDENTIALS_FILE=
SHEETS_NAME=
SHEETS_WORKSHEET=
```

Setting up Postgres:
```
sudo -u postgres psql
CREATE DATABASE arxiv;
CREATE USER arxiv_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE arxiv TO arxiv_user;
```

Setting up Google Sheets:
1. Go to the Google Cloud Console and create a new project.
2. Enable the Google Sheets API.
3. Create a service account and download the credentials file.
4. Share the google sheet with the service account email.
5. Add the path to the credentials file to the `config.env` file.


Setting up openai:
1. Create an account and get an api key.
2. Add the api key to the `config.env` file.
3. Install the openai python package:
```
