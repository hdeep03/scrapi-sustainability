from playwright.async_api import Page

async def go_to_url(page: Page, url: str):
    try:
        await page.goto(url, wait_until="domcontentloaded")
    except TimeoutError:
        print(f"Timeout error while navigating to {url}")
    except Exception as e:
        print(f"An error occurred while navigating to {url}: {str(e)}")

