FROM ubuntu

RUN apt -q update \
    && apt install -q -y --no-install-recommends \
        python3 \
        python3-pip \
        vim \
        wget \
 && apt clean \
 && rm -rf /var/lib/apt/lists/*

COPY zeek-package-website /opt/zeek-package-website/
COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /opt/zeek-package-website
ENTRYPOINT uvicorn app.main:app --host 0.0.0.0 --reload --port 80
