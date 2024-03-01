[![Build](https://github.com/zeek/package-website/actions/workflows/build.yml/badge.svg)](https://github.com/zeek/package-website/actions/workflows/build.yml)
[![Test Suite](https://github.com/zeek/package-website/actions/workflows/pytest.yml/badge.svg)](https://github.com/zeek/package-website/actions/workflows/pytest.yml)
[![license](https://img.shields.io/github/license/zeek/package-website?color=23228B22)](https://github.com/zeek/package-website/blob/main/LICENSE)

# Zeek Package Website Repository

...

### Running with Docker on the AWS Instance

1. SSH into the AWS instance using `<user>@nau.zeek.org`.
2. Clone this repository with `cd ~/ && git clone https://github.com/zeek/package-website`.
3. Run `cd ~/package-website && docker build -t zeek_website . --no-cache` to build the container image.
4. Run `docker compose up -d` to start the service.
5. If you need to take the site down, use `docker compose down`.
