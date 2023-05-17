# Craigslist Scraper/Emailer
A Python script that reads Craigslist listings for a provided search URL. If a new search result is found then an email is sent with the posting image, price, and link to the posting.

Two versions of the script are available; one for running on unix and one for running on a Raspberry Pi.


## Table of Contents
- [Docker Installation](#manual-installation)
- [Manual Installation](#manual-installation)
- [Dev Environment](#development-environment)
- [Project Structure](#project-structure)
- [Further Improvements](#further-improvements)

## Docker Installation
Clone the repo:

```bash
git clone https://github.com/michaelpappas/craigslist-scraper-emailer
cd craigslist-scraper-emailer
```
Fill in your environment variables in the sample-docker-file.yml as described below for secret key,
app password, email sender, and email receiver and rename the sample-docker-file.yml to docker-file.yml

Run
```bash
docker compose build
```
Note: this will take a long time. Firefox alone takes about 5 minutes to install on my 2019 macbook pro.

Once done you can run
```bash
docker composer up
```
Confirm that the containers are running and navigate to localhost:8000 to get to the main page. Here you can add, remove, activate, and deactivate search queries.

To enable the cronjob inside the Docker container you'll need to run
```bash
docker exec -it craigslist_scraper crond -f
```

By default the frequency the script exectures is every 2 minutes. You can change this by modifyin the cronjob file in the dockerscraper directory before building the containers or by editing the crontab in the container.
You can access the container crontab using
```bash
docker exec -it craigslist_scraper crontab -e
```


## Manual Installation

Clone the repo:

```bash
git clone https://github.com/michaelpappas/craigslist-scraper-emailer
cd craigslist-scraper-emailer
```

Set the environment variables:
```bash
touch .env
# open .env and modify the environment variables
```
or
```bash
cp .env.example .env
# open .env and modify the environment variables
```
SECRET_KEY - Choose any string

DATABASE_URL - Replace the {postgres username} and {postgres password} with your personal postgres username and password.

More info regarding configuring postgres on a raspberry pi can be found [here](https://pimylifeup.com/raspberry-pi-postgresql/)

The email environment variables are configured to work with a gmail account as the sending email address configured to use an app password.
More info on configuring Gmail to work with an app password can be seen [here](https://support.google.com/accounts/answer/185833?hl=en).

You will need also sender email address, sender email address app password, and a recipient email address.


## Development Environment

In the cloned directory create a virtual environment
```bash
python3 -m venv venv
```

Activate that venv
```bash
source venv/bin/activate
```

Install the requirements
```
pip3 install -r requirements.txt
```

### Install additional dependencies (for raspberry pi)

chromium-chromdriver
```bash
sudo apt-get install chromium-chromedriver
```

xvfb
```bash
sudo apt-get install xvfb
```

Once all of the dependencies and packages have been installed you can now seed the database with the two tables.
```bash
python3 seed.py
```
If this returns no errors then the database has been correctly seeded.

Start the flask server with:
```bash
flask run -p 5000
```
Navigate to localhost:5000 where you can start configuring search queries to scrape.

To find a search query, search to something on Craigslist, configure the view to "list" and copy the url.
Paste this url into the search url field on the flask app and give the search query a unique name.
Once the search query has been successfully added you can toggle the query active/inactive.
The scraper will only search active search queries.

To test the script you can run:
```bash
python3 scraperPi.py
#or
python3 scraper.py
```
You should receive an email once the script has finished running if new search results are found.

**Caution!**
It is likely that Craigslist will soft ban your IP if you run this too frequently. It is recomendeded that you route your traffic through a VPN.
I used Openvpn with Surfshark and have it configured to start on boot on the RaspberryPi. Info on how to configure Openvpn to start on boot with systemctl can be found [here](https://askubuntu.com/questions/229800/how-to-auto-start-openvpn-client-on-ubuntu-cli/898437#898437?newreg=b08e700a6d814115b9c33628c7a05891) Look for the answer dated March 30, 2017.

To run the script you will need to create a CRONjon.

Example CRONjob
```bash
*/2 * * * * [path_to_venv]/bin/python3 [path_to_directory]/scraperPi.py
# this script will run every 2 minutes forever
```
You will also need to change permissions to execute the file.
```bash
sudo chmod -x [filepath]
```

more info about setting up CRONjobs can be found [here](https://crontab.guru/).

## Project Structure

```
\                           # project directory
 |--.env.example            # example environment variables
 |--craigslist_scraper.py   # main script for OSX
 |--craigslist_scraperPi.py # main script for Raspberry Pi
```

## Further Improvements

1. Write tests for scraper logic and for Flask app
2. Make page to see list of search results for a given query.










