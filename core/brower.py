import asyncio
import logging

from playwright.async_api import Page, async_playwright

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

async def go_to_url(page: Page, url: str):
    try:
        logger.info(f"Navigated to {url}")
        await page.goto(url, wait_until="domcontentloaded")
    except TimeoutError:
        logger.error(f"Timeout error while navigating to {url}")

async def get_urls(page: Page):
    urls = await page.evaluate("() => {return Array.from(document.querySelectorAll(\'a\')).map(a => a.href);}")
    return urls

async def get_full_coverage_screenshots(page: Page):
    pass

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await go_to_url(page, "https://www.google.com")
        urls = await get_urls(page)
        print(urls)

if __name__ == "__main__":
    asyncio.run(main())
    
