import logging
from dataclasses import dataclass
from typing import List, Optional, Tuple
from urllib.parse import urljoin

from playwright.sync_api import Page, TimeoutError
from playwright_stealth import stealth_sync
from twilio.rest import Client

from config import AppConfig, TwilioConfig
from sqlite_setup import SQLiteCache

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class BallotChecker:
    """Handles checking for Liverpool ballot availability."""
    config: AppConfig
    twilio_config: TwilioConfig
    cache: SQLiteCache

    def alert_user(self, message: str) -> None:
        client = Client(
            self.twilio_config.account_sid,
            self.twilio_config.auth_token
        )
        
        for recipient in self.twilio_config.recipients:
            response = client.messages.create(
                messaging_service_sid=self.twilio_config.messaging_service_sid,
                to=recipient,
                body=message
            )
            logging.info(f"Alert sent to {recipient}: {message}")

    # Check if local general sale is available for a specific page link.
    def check_local_general_sale(self, page: Page, href: str) -> bool:
        ticket_items = page.locator("ul.accorMenu li.accorMenuList")
        title = ' '.join(href.split("/")[-1].split('-')[:-1]).upper()
        logging.info(f"Checking sale status for {title}")

        for i in range(ticket_items.count()):
            item = ticket_items.nth(i)
            sale_name = item.locator("span.salename").inner_text().strip()
            status = item.locator("span.status").inner_text().strip()

            if "LOCAL MEMBERS SALE BALLOT" in sale_name.upper() and "REGISTER NOW" in status.upper():
                if self.cache.is_href_cached(href):
                    return False
                    
                self.cache.cache_href(href)
                message = f"🚨 'Local Members Sale Ballot' found open! {title}"
                self.alert_user(message)
                logging.info(f"✅ {message}")
                return True

        logging.info(f"❌ No local general sale available for {title}")
        return False

    def get_ticket_links(self, page: Page) -> List[Tuple[str, str]]:
        ticket_links = page.locator("a.ticket-card.fixture").all()
        if not ticket_links:
            raise ValueError("No ticket links found. Page structure might have changed.")
            
        return [(link.get_attribute("href"), link.inner_text()) for link in ticket_links]

    # Configure the browser page with stealth settings.
    def setup_page(self, page: Page) -> None:
        stealth_sync(page)
    
    def check_tickets(self, page: Page) -> None:
        logging.info("Navigating to Liverpool ticketing...")
        
        try:
            page.goto(urljoin(self.config.base_url, self.config.tickets_path), timeout=30000)
            page.wait_for_selector("a.ticket-card.fixture", timeout=30000)
        except TimeoutError:
            self.alert_user("Failed to load the tickets availability page. The page might be down or structure changed.")
            return

        try:
            page_links = self.get_ticket_links(page)
        except ValueError as e:
            self.alert_user(str(e))
            return

        for idx, (href, text) in enumerate(page_links, 1):
            logging.info(f"Checking link {idx}/{len(page_links)}...")
            try:
                page.goto(urljoin(self.config.base_url, href), timeout=30000)
                page.wait_for_selector("ul.accorMenu li.accorMenuList", timeout=30000)
                self.check_local_general_sale(page, href)
            except TimeoutError:
                logging.error(f"Failed to load ticket link {href}")
