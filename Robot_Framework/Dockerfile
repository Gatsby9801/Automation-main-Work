FROM ubuntu
RUN apt-get update

RUN apt install -y python3.10
RUN apt install -y python3-pip

RUN apt-get install -y xvfb 
RUN apt-get install -y zip 
RUN apt-get install -y wget 
RUN apt-get install ca-certificates 
RUN apt-get install -y libnss3-dev libasound2 libxss1 libappindicator3-1 libindicator7 gconf-service libgconf-2-4 libpango1.0-0 xdg-utils fonts-liberation
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb 
RUN apt-get install -y ./google-chrome*.deb 
RUN rm google-chrome*.deb


COPY requirements.txt    /

RUN pip install -r requirements.txt

RUN wget -N https://chromedriver.storage.googleapis.com/107.0.5304.62/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN chmod +x chromedriver
RUN rm chromedriver_linux64.zip


COPY . /Automation
RUN cp chromedriver /Automation/Driver/

RUN cd Automation
### RUN xvfb-run google-chrome --no-sandbox

CMD ["robot", "-d", "Output", "TestCases/*"]