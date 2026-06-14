FROM python:3.14

MAINTAINER Borja Pintos

#download
RUN git clone https://github.com/BorjaPintos/whatthefinances.git

WORKDIR /whatthefinances

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

#update system
RUN apt update
RUN apt -y upgrade
RUN apt install -y locales locales-all libnspr4 libnss3 libdbus-1-3 libglib2.0-0 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libnspr4 libnss3 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 libgtk-3-0 fonts-liberation xdg-utils

RUN CHROME_VERSION=$(curl -fsSL https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE) \
    && wget -O /tmp/chrome.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip" \
    && wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip"
RUN unzip /tmp/chrome.zip -d /opt/
RUN unzip /tmp/chromedriver.zip -d /opt/
RUN ln -s /opt/chrome-linux64/chrome /usr/local/bin/chrome
RUN ln -s /opt/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chrome /usr/local/bin/chromedriver
RUN rm -f /tmp/chrome.zip /tmp/chromedriver.zip

# Crear enlaces simbólicos estándar en Linux
RUN ln -s /opt/chrome-linux64/chrome /usr/bin/google-chrome
RUN chmod +x /usr/bin/google-chrome /usr/local/bin/chromedriver

EXPOSE 9090

CMD ["sh", "entrypoint.sh"]