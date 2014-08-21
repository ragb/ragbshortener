# RAGB Shortener

My own simple URL Shortener based on [Flask](http://flask.pocoo.org) and 
[Redis](http://redis.io)

## Features

* Simple and small: 58 lines of code counting command line argument parsing and such.
* Very simple *REST* *API, can be easily used using `curl`.
* Docker-ready: run it wherever you want.


### Usage

### Server

Install or find a `Redis` server and run `ragbshortener.py`. The server will listen for HTTP requests on port 5000 be default and will try to connect to `Redis`on `localhost`port 6379.  
Pass `-h`or `--help` help to `ragbshortener.py`to check all options. Main are the following:

* `-p` or `--port`change http port (default 5000)
* `--server-name` server name to use for url generation(you can also define a $VIRTUAL_HOST environment variable for this effect)
* `--ttl`change default link time to live (expiration time)
* `--redis-host` set `Redis`server host
* `--redis-post`set `Redis`port
* `--redis-db`set `Redis`database to use (default 0)


### Using docker

You can build a [Docker](https://www.docker.com) image for this app by running

```sh
docker build -t ragb/ragbshortener .
```

To run it, firstly have at hand a `Redis`container, for instance:

```sh
docker pul dockerfile/redis
docker run -t redis_server dockerfile/redis
```

Then run the app's container linking it to redis (use `redis_server`for the link name):```sh
docker run -t ragbshortener --links redis_server:redis_server -p 5000:5000 ragb/ragbshortener
```

This will publish port 5000 on your Docker host.

If you are using [Fig](http://www.fig.sh) you can run this setup simply by running


```sh
fig up -d
```

### Client usage

* to create a link redirection, simply post to the `/`endpoint the url in a `url`parameter in url-encoded form. On success (status 201 - Created) you will receive the new url, path is the `key`to use for redirection.
* To be redirected to the key's associated link use the `/<key>` endpoint (GET request).

A curl-based example follows:


```sh
# Create a redirection for http://github.com
url=$(curl -d*url=http://github.com' http://localhost:5000)

echo $url
# Retrieve the url (github's page must be shown)
curl $url
```

## License


Copyright 2014 Rui Batista

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
