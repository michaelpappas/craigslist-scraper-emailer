FROM python:3.9-alpine
WORKDIR /dockerScraper
COPY dockerScraper/requirements.txt .
RUN pip install -r requirements.txt
RUN apk update
RUN apk add firefox
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
RUN tar -xzf geckodriver-v0.33.0-linux64.tar.gz -C /usr/local/bin && rm geckodriver-v0.33.0-linux64.tar.gz
RUN chmod +x /usr/local/bin/geckodriver
RUN apk add xvfb
COPY /dockerScraper .
Copy /dockerScraper/cronjob /etc/crontabs/root
CMD [ "python3", "-m" , "flask", "run", "-p", "5005", "--host=0.0.0.0"]
# RUN echo '*/2  *  *  *  *    python3 /dockerScraper/scraper.py' > /etc/crontabs/root
# CMD crond


