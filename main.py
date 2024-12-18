from playwright.sync_api import sync_playwright
from config import AppConfig, TwilioConfig
from sqlite_setup import SQLiteCache
from ballot_checker import BallotChecker

def main():
    config = AppConfig()
    twilio_config = TwilioConfig()
    cache = SQLiteCache()
    cache.init_db()
    
    checker = BallotChecker(config, twilio_config, cache)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=config.user_agent,
            ignore_https_errors=True
        )
        
        page = context.new_page()
        checker.setup_page(page)
        checker.check_tickets(page)
        browser.close()

if __name__ == "__main__":
    main()