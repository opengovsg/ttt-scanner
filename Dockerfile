FROM resin/raspberrypi3-python:2.7-slim

ENV TZ Asia/Singapore

WORKDIR /mrt

RUN apt-get update \
  && apt-get install -y wireless-tools iputils-ping net-tools rfkill

COPY requirements.txt /mrt
RUN pip install --trusted-host pypi.python.org --only-binary all -r requirements.txt

COPY ./scrape /mrt/
COPY wait_for_ntp_sync.py /mrt/mrtScanner
COPY start.sh /mrt/mrtScanner
WORKDIR /mrt/mrtScanner

CMD rfkill unblock wlan; ifconfig wlan0 down; ifconfig wlan0 up; python mrtScanner.py
