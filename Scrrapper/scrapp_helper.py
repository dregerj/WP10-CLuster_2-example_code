

import pandas as pd
import asyncio
import logging

from numpy import number
from typing import List
from urllib.parse import urljoin
from random import uniform
from playwright.async_api import async_playwright
from URL_Helper.url_helper import return_clear_URL


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

handler = logging.FileHandler("errors.log")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


###
## Page - Content page 
## base_url - url for page 
## ABOUT_KEYWORDS - list phases for find on page
###
@staticmethod
async def find_about_page(page:str, base_url: str, ABOUT_KEYWORDS: List[str])->str | None:
    links = await page.query_selector_all("a")
    for link in links:
        text = (await link.inner_text() or "").lower()
        href = await link.get_attribute("href")
        if any(keyword in text for keyword in ABOUT_KEYWORDS):
            return urljoin(base_url, href)
    return None

###
## Scrap text from page to the limit chars
###
@staticmethod
async def extract_text(page, limit: number)-> str:
    text = await page.evaluate("() => document.body?.innerText || ''")
    text = " ".join(text.split())
    return text[:limit] if limit else text

###
## Get context data from main or about page, and return the infomation to save in DF. 
###
@staticmethod
async def process_url(browser, url, ABOUT_KEYWORDS: List[str], limit: number) -> dict[str, str] | None:
    page = await browser.new_page()
    try:
        response =await page.goto(url, timeout=60000, wait_until="domcontentloaded")
        if response.status >= 400:
            return {
                source: None,
                content: None
            }
        await asyncio.sleep(uniform(5, 10))
        about_url = await find_about_page(page, url, ABOUT_KEYWORDS)
        if about_url:
            await page.goto(about_url, timeout=60000, wait_until="domcontentloaded")
            await asyncio.sleep(uniform(5, 10)) 
            source = "About"
        else:
            source = "Main Page"
        content =await extract_text(page, limit)
        return {
                "source": source,
                "content": content
            }
    except Exception:
        logger.exception(f"Could not enter {url}")
        return None
    finally:
        if page and not page.is_closed():
            await page.close()


###
## Function for start scraping, this function use others functions, from this file, to scraping, and save information to csv file
###   
@staticmethod
async def start_scrap(df:pd.DataFrame, ABOUT_KEYWORDS: List[str], CHAR_LIMIT: number, BATCH_SIZE: number) -> pd.DataFrame:
    save = 0
    async with async_playwright() as p:
        browser =await p.chromium.launch(headless=True)
        for i, url in enumerate(df["WWW"]):
            if (pd.isna(df.loc[i, "Description"])) or (df.loc[i, "Description"] == "NO Description") or (df.loc[i, "Description"] == "NULL") or (len(df.loc[i, "Description"]) <=5):
                url = return_clear_URL(url)
                if url is not None:
                    try:
                        result = await process_url(browser, url, ABOUT_KEYWORDS, CHAR_LIMIT)
                        if result is None:
                            logger.exception("Problem with the procedure PROCESS_URL")
                            df.loc[i, "Description"] = "NO Description"
                            df.loc[i, "URL_SCRAP"] = "Niewłaściwy format adres URL"
                            continue
                        else:
                            df.loc[i, "Description"] = result['content']
                            df.loc[i, "URL_SCRAP"] = result['source']
                    except Exception as e:
                        logger.exception("Problem with the procedure: PROCESS_URL")
                        df.loc[i, "Description"] = "NO Description"
                        df.loc[i, "URL_SCRAP"] = "Błąd w adresie URL"    
                else:
                    df.loc[i, "Description"] = "NO Description"
                    df.loc[i, "URL_SCRAP"] = "BRAK URL DO SCRAPOWANIA" 
                save = save + 1
                if save - BATCH_SIZE == 0:
                    df.to_csv('output.csv', sep=';')
                    save = 0
        df.to_csv('output.csv', sep=';',index=False)
        await browser.close()
    return df
