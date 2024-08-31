import psycopg2
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("database_manager.log"),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)

class DatabaseManager:
    def __init__(self, db_name, user, password, host='localhost'):
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host
            )
            self.cursor = self.conn.cursor()
            self.logger.info("Connected to the database successfully.")
        except Exception as e:
            self.logger.error(f"Failed to connect to the database: {e}")
            raise

    def create_table(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id SERIAL PRIMARY KEY,
                title TEXT UNIQUE,
                link TEXT UNIQUE,
                summary TEXT,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            self.conn.commit()
            self.logger.info("Table 'papers' created or verified successfully.")
        except Exception as e:
            self.logger.error(f"Failed to create table: {e}")

    def save_paper(self, paper):
        try:
            self.cursor.execute(
                "INSERT INTO papers (title, link, summary) VALUES (%s, %s, %s) ON CONFLICT (title) DO NOTHING;",
                (paper['title'], paper['link'], paper['summary'])
            )
            self.conn.commit()
            self.logger.info(f"Paper '{paper['title']}' saved to the database.")
        except Exception as e:
            self.logger.error(f"Failed to save paper '{paper['title']}': {e}")

    def paper_exists(self, title):
        try:
            self.cursor.execute("SELECT * FROM papers WHERE title = %s", (title,))
            exists = self.cursor.fetchone() is not None
            self.logger.debug(f"Checked existence of paper '{title}': {'Found' if exists else 'Not found'}.")
            return exists
        except Exception as e:
            self.logger.error(f"Failed to check existence for paper '{title}': {e}")
            return False

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            self.logger.info("Database connection closed successfully.")
        except Exception as e:
            self.logger.error(f"Failed to close the database connection: {e}")
