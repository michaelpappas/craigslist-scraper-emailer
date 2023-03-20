# Craigslist Scraper/Emailer
A Python script that reads Craigslist listings for a provided search URL. If a new search result is found then an email is send with the posting image, price, and link to the posting.

Two versions scripts are available; one for running on OSX and one for running on a Raspberry Pi.


## Table of Contents
- [Manual Installation](#manual-installation)
- [Dev Environment](#development-environment)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Further Improvements](#further-improvements)

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

The environment variables are configured to work with a gmail account as the sending email address configured to use an app password.
More info on configuring Gmail to work with an app password can be seen [here](https://support.google.com/accounts/answer/185833?hl=en).

You will need a sender email address, sender email address app password, and a recipient email address.

## Development Environment

You will need to create a text file to store the previous search results. It can be empty and will be populated when you run the script for the first time.

```bash
touch searchResults.txt
# create emtpy text file for storing search results
```

To run the script you will need to create a CRONjon to run the script.

Example CRONjob
```bash
*/2 * * * * python3 [path_to_directory]/cragslist_scraperPi.py
# this script will run every 2 minutes forever
```
more info about setting up CRONjobs can be found [here](https://crontab.guru/).

### Project Structure

```
\                           # project directory
 |--.env.example            # example environment variables
 |--craigslist_scraper.py   # main script for OSX
 |--craigslist_scraperPi.py # main script for Raspberry Pi
```










