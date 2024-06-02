FROM python:3.12

MAINTAINER Borja Pintos

#download
RUN git clone https://github.com/BorjaPintos/whatthefinances.git

WORKDIR /whatthefinances

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

#update system
RUN apt update
RUN apt -y upgrade
RUN apt install -y locales locales-all

EXPOSE 9090

CMD ["sh", "entrypoint.sh"] 


