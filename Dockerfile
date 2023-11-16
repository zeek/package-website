FROM ubuntu

RUN apt update
RUN apt -y upgrade
RUN apt install -y wget git vim python3

RUN cd ~/ && wget https://bootstrap.pypa.io/get-pip.py \
&& python3 get-pip.py && rm get-pip.py

RUN cd ~/ && git clone --branch cjb873/docker-compose https://github.com/zeek/package-website.git

RUN python3 -m pip install --upgrade pip

RUN cd ~/package-website \
&& pip install -r requirements.txt
