#!/usr/bin/env python

import argparse
import os
import random
from urlparse import urlparse 
from flask import request, abort, redirect, Flask, url_for
import redis


app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=5000, type=int)
parser.add_argument("--redis-host", metavar='redis_host', default=os.getenv('REDIS_HOST', 'localhost'), help='Redis host to connect to')
parser.add_argument('--redis-port', metavar='redis_port', default=int(os.getenv('REDIS_PORT', '6379')), type=int, help='Redis port to connect to')
parser.add_argument('--redis-db', metavar='redis_db', default=os.getenv('REDIS_DB', '0'), help='Redis database to use')
parser.add_argument('--ttl', default=86400, type=int, help='Link TTL (expiration time)')
parser.add_argument('--server-name', metavar='server_name', default=os.getenv('VIRTUAL_HOST'), help='Server name (used for url generation)')
arguments = parser.parse_args()

app.config['server_name'] = arguments.server_name

keyPrefix = "ragbshortener:"

@app.route("/<key>", methods=['GET'])
def get_url(key):
	try:
		return redirect(db[keyPrefix + key])
	except KeyError:
		return abort(404)

@app.route("/", methods=['POST'])
def create_url():
	url = request.form['url']
	u = urlparse(url)
	if u.scheme not in ('http', 'https'):
		return abort(400)
	key = create_key(7)
	db.set(keyPrefix + key, url, ex=arguments.ttl)
	logger.info("Created key %s", key)
	return url_for('get_url', key=key, _external=True), 201, {}


alphanum = '0123456789ABCDEFGHIJKLMNOPQRSTuVWXYZabcdefghijklmnopqrstuvwxyz'
def create_key(length):
	return "".join((random.choice(alphanum) for i in xrange(length)))


def create_redis():
	return redis.StrictRedis(host=arguments.redis_host, port=arguments.redis_port, db=arguments.redis_db)



logger = app.logger

db = create_redis()


if __name__ == '__main__':
	app.run(port=arguments.port, host='0.0.0.0')