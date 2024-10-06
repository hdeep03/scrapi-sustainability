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
    """
    Navigate to the specified URL.
    This function navigates to the given URL and waits for the DOM content to load.
    Args:
        page (Page): The Playwright Page object representing the current browser page.
        url (str): The URL to navigate to.
    Returns:
        None
    """
    try:
        logger.info("Navigated to %s", url)
        await page.goto(url, wait_until="domcontentloaded")
    except TimeoutError:
        logger.error("Timeout error while navigating to %s", url)


async def get_urls(page: Page):
    """
    Get all URLs on the page.
    This function retrieves all URLs from the page's anchor (a) elements.
    Args:
        page (Page): The Playwright Page object representing the current browser page.
    Returns:
        list: A list of URLs found on the page.
    """
    links = await page.query_selector_all('a')
    link_data = [{'text': (await link.inner_text()).strip(),
                  'href': await link.get_attribute('href')} for link in links]
    return link_data


async def get_full_coverage_screenshots(page: Page, output_directory: str):
    """
    Take a full coverage screenshot of the page.
    This function captures a full-page screenshot of the current page.    
    Args:
        page (Page): The Playwright Page object representing the current browser page.
        output_directory (str): The directory path where the screenshot will be saved.
    Returns:
        None
    The function sets the viewport size to 1280x720 pixels and then takes a full-page
    screenshot, saving it as 'full_page_screenshot.png' in the specified output directory.
    """
    await page.set_viewport_size({"width": 1280, "height": 720})
    await page.screenshot(path=f"{output_directory}/full_page_screenshot.png",
                          full_page=True)

async def search_for_urls(page, search_term: str):
    await go_to_url(page, f"https://www.google.com/search?q={search_term}")
    h3_links = await page.evaluate('''
        () => Array.from(document.querySelectorAll('h3'))
            .map(h3 => {
                const a = h3.closest('a');
                return a ? {
                    text: h3.textContent.trim(),
                    href: a.href
                } : null;

            })
            .filter(link => link && link.href && link.href.startsWith('http'))
    ''')
    logger.info("Found %d links for %s", len(h3_links), search_term)
    return h3_links

async def get_search_url(name, pool):
    page = await pool.get()
    res = await search_for_urls(page, f"{name} environmental report")
    pool.put_nowait(page)
    return res

def get_page_text(page):
    return page.evaluate("""
        () => {
            const elements = document.querySelectorAll('body *');
            let visibleText = [];
            for (let element of elements) {
                const style = window.getComputedStyle(element);
                if (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0') {
                    const text = element.textContent.trim();
                    if (text) {
                        visibleText.push(text);
                    }
                }
            }
            return visibleText.join('\\n');
        }
    """)

async def main():
    """
    Main function to execute the browser operations.
    This function initializes the Playwright browser and page, navigates to the specified URL,
    retrieves all URLs on the page, and takes a full coverage screenshot.
    Returns:
        None
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        # companies = ["microsoft", "google", "apple", "amazon", "facebook", "netflix", "tesla"]
        # parallelism = 4
        # pool = asyncio.Queue(maxsize=parallelism)
        # for _ in range(parallelism):
        #     pool.put_nowait(await context.new_page())

        # partial_results = []
        # for company in companies:
        #     partial_results.append(get_urls(company, pool))
        # res = await asyncio.gather(*partial_results)
        # for company, links in zip(companies, res):
        #     for x in links:
        #         print(f"{x['text']}: {x['href']}")
        page = await context.new_page()
        await go_to_url(page, "https://corporate.walmart.com/purpose/esgreport/environmental/climate-change")
        text = await get_page_text(page)
        print(text)

if __name__ == "__main__":
    asyncio.run(main())
    
