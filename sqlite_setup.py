import sqlite3
from datetime import datetime

class SQLiteCache:
    def init_db(self):
        conn = sqlite3.connect("href_cache.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cached_hrefs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                href TEXT UNIQUE,
                added_on TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def is_href_cached(self, href):
        conn = sqlite3.connect("href_cache.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM cached_hrefs WHERE href = ?", (href,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def cache_href(self, href):
        conn = sqlite3.connect("href_cache.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO cached_hrefs (href, added_on) VALUES (?, ?)", (href, datetime.now()))
        conn.commit()
        conn.close()