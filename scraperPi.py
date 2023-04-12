from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service #pi specific
from webdriver_manager.chrome import ChromeDriverManager #pi specific
import requests
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from models import db, connect_db, URL, Listing
from pyvirtualdisplay import Display
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

load_dotenv()

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

connect_db(app)

APP_PASSWORD = os.getenv('app_password')

def get_active():
    """ fetches list of active search queries from URL table """
    searches = URL.get_searches()
    results = {}

    for search in searches:
        listings = get_listings(search.search_url)
        new_results = []
        for x in range(10):
            title = listings.find_all("a")[x].text
            listing_url = listings.find_all("a")[x]['href']
            listing_db = Listing.find_listing(listing_url)
            if len(listing_db) == 0:
                (price, img_url) = item_content(listing_url)
                Listing.add_listing(listing_url, title)
                new_results.append({"title":title,
                                    "listing_url":listing_url,
                                    "price":price,
                                    "img_url":img_url
                                    })
        results[search.name] = new_results
    return results

def get_listings(url):
    """ fetches page data, waits for content to load, and returns 'ol' from page """

    display = Display(visible=0, size=(1600, 1200))
    display.start()
    browser_driver = Service('/usr/lib/chromium-browser/chromedriver')
    driver = webdriver.Chrome(service=browser_driver)
    response = driver.get(url)
    time.sleep(1)
    html = driver.page_source
    html_soup = BeautifulSoup(html, 'html.parser')
    driver.quit()
    display.stop()
    return html_soup.find('ol')

def item_content(url):
    """ returns tuple of price integer and image (if available) from individual item page
        if there is no image or price on the listing page it will return none for each value. """
    listing = requests.get(url)
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


new_results = get_active()
email_content = format_html(new_results)


################################# email logic #####################
sender_email = os.getenv('email_sender')
receiver_email = os.getenv('email_receiver')

message = MIMEMultipart("alternative")
message["Subject"] = "Craigslist Espresso Machines"
message["From"] = sender_email
message["To"] = receiver_email

html = f"""<html><body>{email_content[0]}</body></html>"""

# Turn html into MIMEText object
part1 = MIMEText(html, "html")

# Content email client will put in body of message.
message.attach(part1)

# Create secure connection with server and send email
# If email_content length is greater than 0 (has new search results) -> send the email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, APP_PASSWORD)
    if email_content[1] == True:
        server.sendmail(
            sender_email, receiver_email, message.as_string()
    )


