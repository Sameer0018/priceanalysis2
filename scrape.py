import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_website(website):
    """
    Function to scrape a website and return cleaned body content.
    Uses Selenium to fetch the HTML and BeautifulSoup to extract the body content.
    """
    print("Connecting to Scraping Browser...")

    # Set up Chrome options for headless mode (for running without a UI)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")

    # Initialize the Selenium WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(website)  # Open the website
        
        # Wait for the page to load by waiting for the body element to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Get the page source (HTML content)
        html_content = driver.page_source
        
        if not html_content:
            print(f"Error: No HTML content found for {website}.")
            return ""

        # Extract body content
        body_content = extract_body_content(html_content)
        print(f"Body content extracted: {body_content[:1000]}...")  # Preview first 1000 chars

        # Clean the extracted body content
        cleaned_content = clean_body_content(body_content)
        print(f"Cleaned content preview: {cleaned_content[:1000]}...")  # Preview first 1000 chars
        
        # Split content if necessary (e.g., to prevent exceeding max length in some use cases)
        content_chunks = split_dom_content(cleaned_content)
        
        return content_chunks  # List of cleaned and split content chunks

    except Exception as e:
        print(f"Error while scraping {website}: {str(e)}")
        return ""

    finally:
        driver.quit()  # Always close the browser after scraping

def extract_body_content(html_content):
    """
    Extracts the body content from the raw HTML using BeautifulSoup.
    """
    if html_content is None:
        print("Error: No HTML content found.")
        return ""
    
    # Ensure html_content is a string, not a list
    if isinstance(html_content, list):
        html_content = ''.join(html_content)

    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    """
    Cleans the body content by removing scripts, styles, and extra spaces.
    """
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove all script and style tags
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text and clean it
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    """
    Splits the DOM content into chunks of a maximum length.
    """
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]


