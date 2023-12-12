[![Build](https://github.com/zeek/package-website/actions/workflows/build.yml/badge.svg)](https://github.com/zeek/package-website/actions/workflows/build.yml)
[![Test Suite](https://github.com/zeek/package-website/actions/workflows/pytest.yml/badge.svg)](https://github.com/zeek/package-website/actions/workflows/pytest.yml)
[![license](https://img.shields.io/github/license/zeek/package-website?color=23228B22)](https://github.com/zeek/package-website/blob/main/LICENSE)

# Zeek Package Website Repository
...

### Running locally via docker-compose

1. Clone this repository with `git clone https://github.com/zeek/package-website` and `cd` into the checkout.
2. Run `docker compose up -d` to start the service. It will build the Docker image on the fly.

### Running locally directly via docker

1. Clone this repository with `git clone https://github.com/zeek/package-website` and `cd` into the checkout.
2. Run `docker build -t zeek_website .` to build the site's image.
3. Run `docker run -it --rm -p 9000:80 zeek_website` to launch the site at port 9000 on the local system.

### Running with Docker on the AWS Instance

1. SSH into the AWS instance using `<user>@nau.zeek.org`.
2. Clone this repository with `git clone https://github.com/zeek/package-website`.
3. Run `cd ~/package-website && docker build -t zeek_website . --no-cache` to build the container image.
4. Run `docker compose up -d` to start the service.
5. If you need to take the site down, use `docker compose down`.
