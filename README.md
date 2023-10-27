# Zeek Package Website Repository
...


### Running with Docker on the AWS Instance

1. SSH into the AWS instance using `<user>@nau.zeek.org`.
2. Run ```docker start website_container```. If the website is currently running in the container and you with to make some changes, first run
```docker stop website_container```.
3. Run ```docker exec -it website_container /bin/bash``` to access the container.
4. Change into the proper directory with ```cd ~/package-website/zeek-package-website/```.
5. Pull in any new changes with ```git pull```.
6. Start the application with ```uvicorn app.main:app --host 0.0.0.0 --reload --timeout-keep-alive=65 --port 80```. We're running this server as a test instance, so you can just
close your terminal window and everything will work as expected. Eventually, this will all be done with a docker-compose file.
