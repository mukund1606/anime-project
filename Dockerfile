# 
FROM python:3.11-alpine

# Install Chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable

# # Installing Unzip
# RUN apt-get install -yqq unzip

# # Download the Chrome Driver
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# # Unzip the Chrome Driver into /usr/local/bin directory
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# # Set display port as an environment variable
# ENV DISPLAY=:99

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


# 
COPY ./server /code/server
COPY ./utils /code/utils
COPY ./main.py /code/main.py

# 
# CMD [ "uvicorn", "server.api:app", "--port", "8000"]
CMD [ "python", "main.py"]
