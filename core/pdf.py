import asyncio

import requests

from pypdf import PdfReader

async def download_pdf(url: str, output_file: str):
    """
    Download a PDF file.
    This function downloads a PDF file from the specified URL.
    Args:
        url (str): The URL of the PDF file to download.
        output_directory (str): The directory path where the PDF file will be saved.
    Returns:
        None
    The function uses the requests library to download the PDF file and saves it
    as 'downloaded_pdf.pdf' in the specified output directory.
    """
    response = requests.get(url)
    with open(f"{output_file}.pdf", "wb") as f:
        f.write(response.content)

async def is_pdf(url: str):
    """
    Check if a URL points to a PDF file.
    This function checks if the specified URL points to a PDF file.
    Args:
        url (str): The URL to check.
    Returns:
        bool: True if the URL points to a PDF file, False otherwise.
    The function sends a HEAD request to the URL and checks the Content-Type header
    to determine if the URL points to a PDF file.
    """
    response = requests.head(url)
    content_type = response.headers.get("Content-Type")
    return content_type == "application/pdf"

async def get_text_on_pdf_page(pdf_path: str, queries: list):
    queries = [query.lower() for query in queries]
    reader = PdfReader(f"{pdf_path}")
    number_of_pages = len(reader.pages)
    matches = {}
    for page in range(number_of_pages):
        text = reader.pages[page].extract_text().lower()
        for query in queries:
            if query in text:
                matches[page] = matches.get(page, 0) + 1
        if matches.get(page):
            print("-"*50)
            print(text)
            print("-"*50)
    return [x[0] for x in sorted(matches.items(), key=lambda x: x[1], reverse=True)]

async def main():
    # url = "https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2024.pdf"
    # url = "https://docs.broadcom.com/doc/environment-social-governance-report"
    url = "https://www.ti.com/lit/ml/szzo105/szzo105.pdf"
    output_directory = "tmp"
    await download_pdf(url, output_directory)
    text = await get_text_on_pdf_page(f"{output_directory}/downloaded_pdf.pdf", ["scope 1", "scope 2", "scope 3"])
    print(text)

if __name__ == "__main__":
    asyncio.run(main())