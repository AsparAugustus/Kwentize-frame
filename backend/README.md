# Remove background with Python

This repository is needed to remove the background from any image. Is created as a Docker to be sure it can run in any device. 
Under the hood uses Flask and popular `rembg` packaged.

Supposing you have Docker already installed in your machine here you can find instructions to run the package

# Create docker

docker build --tag removebg .

# Run docker

docker run -d --restart unless-stopped -p 5000:5000 removebg
docker run -d -p 5000:5000 removebg

# Check status

Go to http://172.17.0.2:5000

# Remove bg

```[POST] http://172.17.0.2:5000/remove
{url: "https://to.img"}
```
Files are served at: `http://172.17.0.2:5000/static/RESPONSE_FROM_PREV_REQUEST`

