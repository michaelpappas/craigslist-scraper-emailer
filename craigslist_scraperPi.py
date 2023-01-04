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

load_dotenv()

from pyvirtualdisplay import Display

APP_PASSWORD = os.getenv('app_password')

#replace SEARCH_URL with the url of the search you want to run the script on
SEARCH_URL = 'https://sfbay.craigslist.org/search/sss?query=espresso%20machine#search=1~list~0~0'

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

def get_previous(text):
    """ Takes text file content and returns list of strings without newline"""
    previous_text = open(text, 'r')
    previous_links = previous_text.readlines()

    formatted_links = []
    for lines in previous_links:
        formatted_links.append(lines.rstrip())

    previous_text.close()
    return formatted_links

def item_content(url):
    """ returns tuple of price and image (if available) from individual item page
        if there is no image on the listing page it will return none. """
    listing = requests.get(url)
    content = BeautifulSoup(listing.content, 'html.parser')
    try:
        image = content.find('img')['src']
    except:
        image = None
    try:
        price = content.find(class_="price").get_text()
    except:
        price = None
    return (price, image)


def format_new_text(data):
    """ Takes in BFS 'ol' content and returns formated dictionary of strings formatted the same as .txt """
    new_results = []
    for x in range(20):
        title = data.find_all("a")[x].text
        link = data.find_all("a")[x]['href']
        new_results.append(f"{title} - {link}")
    return new_results

def format_new_html(data):
    """ Takes in BFS 'ol' content and returns html string for email content """
    new_results = ''
    for x in range(20):
        title = data.find_all("a")[x].text
        link = data.find_all("a")[x]['href']
        text_line = f"{title} - {link}"
        if text_line not in previous_results:
            content = item_content(link)
            price = content[0]
            image = content[1]
            new_results += (f'<a href={link}>{title} - {price}</a><br><img src="{image}"><br>')
    return new_results

posts = get_listings(SEARCH_URL)

previous_results = get_previous('/home/michael/Documents/craigslist_scraper/searchResults.txt')

new_formatted = format_new_text(posts)

email_content = format_new_html(posts)

with open('/home/michael/Documents/craigslist_scraper/searchResults.txt', 'w') as f:
    """ writes 20 most recent search results to text file for future reference """
    for x in range(20):
        f.write(new_formatted[x])
        f.write('\n')


################################# email logic #####################
sender_email = os.getenv('email_sender')
receiver_email = os.getenv('email_receiver')

message = MIMEMultipart("alternative")
message["Subject"] = "Craigslist Espresso Machines"
message["From"] = sender_email
message["To"] = receiver_email

html = f"""<html><body>{email_content}</body></html>"""

# Turn html into MIMEText object
part1 = MIMEText(html, "html")

# Content email client will put in body of message.
message.attach(part1)

# Create secure connection with server and send email
# If email_content length is greater than 0 (has new search results) -> send the email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, APP_PASSWORD)
    if len(email_content) > 0:
        server.sendmail(
            sender_email, receiver_email, message.as_string()
    )


