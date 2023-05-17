from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service #pi specific
# from webdriver_manager.chrome import ChromeDriverManager #pi specific
from pyvirtualdisplay import Display #pi specific
from selenium.webdriver.firefox.options import Options #docker specific
import requests
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import URL, Listing
from app import scraper_enable

load_dotenv()
db_string = os.environ['DATABASE_URL']

db = create_engine(db_string)

Session = sessionmaker(db)
session = Session()

def get_active():
    """ fetches list of active search queries from URL table """
    searches = session.query(URL).filter(URL.active==True).all()
    results = {}

    for search in searches:
        listings = get_listings(search.search_url)
        extracted_listings = extract_listings(listings)

        new_results = []
        for listing in extracted_listings:

            (price, img_url) = item_content(listing[1])
            listing_db = session.query(Listing).filter(Listing.url==listing[1]).all()

            if len(listing_db) == 0:
                listing_data = {"title":listing[0],
                                "listing_url":listing[1],
                                "price":price,
                                "img_url":img_url
                                }
                new_results.append(listing_data)
                add_listing_db(listing[0], listing[1])
        results[search.name] = new_results

    return results


# # Mac os specific function below. Comment out if using a Rapsberry Pi
# def get_listings(url):
#     """ fetches page data, waits for content to load, and returns 'ol' from page """
#     driver = webdriver.Firefox()
#     response = driver.get(url)
#     time.sleep(2)
#     html = driver.page_source
#     html_soup = BeautifulSoup(html, 'html.parser')
#     driver.quit()
#     return html_soup.find('ol')


# Raspberry Pi specific function below. Comment out if using Mac OS.
def get_listings(url):
    """ fetches page data, waits for content to load, and returns 'ol' from page """

    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()
    response = driver.get(url)
    time.sleep(2)
    html = driver.page_source
    html_soup = BeautifulSoup(html, 'html.parser')
    driver.quit()
    display.stop()
    return html_soup.find('ol')

def extract_listings(inputHTML):
    """ exctracts listing title and url from beautiful soup data
        returns list of tuples """

    listings = []
    listing_count = 1
    while listing_count <= 10:
        try:
            title = inputHTML.find_all("a")[listing_count].text
            listing_url = inputHTML.find_all("a")[listing_count]['href']
            listings.append((title, listing_url))
            listing_count = listing_count + 1
        except:
            return listings

    return listings
def item_content(url):
    """ returns tuple of price integer and image (if available) from individual item page
        if there is no image or price on the listing page it will return none for each value. """
    try:
        listing = requests.get(url)
    except:
        return None
    content = BeautifulSoup(listing.content, 'html.parser')
    try:
        image = content.find('img')['src']
    except:
        image = "no img url"
    try:
        price = content.find(class_="price").get_text()
        formatted_price = price[1:].replace(",", "")
    except:
        formatted_price = "no price"
    return (formatted_price, image)


def format_html(input):
    has_content = False
    email_html = ""
    for search_name, results in input.items():
        email_html += f'<h2>{search_name}</h2>'

        if len(results) == 0:
            email_html += "<p> No new listings</p>"
        else:
            for result in results:
                has_content = True
                email_html += f'<a href={result["listing_url"]}>{result["title"]} - ${result["price"]}</a><br><img src="{result["img_url"]}"><br>'

    return (email_html, has_content)

def get_searches():
    """ queries db and returns active search queries """
    searches = URL.query.filter_by(active=True).all()
    return searches

def add_listing_db(new_title, new_url):
    """ adds new listing to Listings table """
    new_listing = Listing(url = new_url, title = new_title)
    session.add(new_listing)
    session.commit()


if scraper_enable:
    new_results = get_active()
    email_content = format_html(new_results)

################################# email logic #####################
SENDER_EMAIL = os.environ['email_sender']
RECEIVER_EMAIL = os.environ['email_receiver']
APP_PASSWORD = os.environ['app_password']


message = MIMEMultipart("alternative")
message["Subject"] = "Craigslist Scraper"
message["From"] = SENDER_EMAIL
message["To"] = RECEIVER_EMAIL

html = f"""<html><body>{email_content[0]}</body></html>"""

# Turn html into MIMEText object
part1 = MIMEText(html, "html")

# Content email client will put in body of message.
message.attach(part1)

# Create secure connection with server and send email
# If email_content length is greater than 0 (has new search results) -> send the email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(SENDER_EMAIL, APP_PASSWORD)
    if email_content[1]:
        server.sendmail(
            SENDER_EMAIL, RECEIVER_EMAIL, message.as_string()
    )


