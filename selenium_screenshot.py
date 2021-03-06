from threading import Lock
from os import environ as ENV
import logging.config

from flask import Flask, request

from raven.contrib.flask import Sentry

from selenium import webdriver


logging.basicConfig()


app = Flask(__name__)

if ENV.get("SENTRY_DSN"):
    sentry = Sentry(app, dsn=ENV['SENTRY_DSN'])


Driver = getattr(webdriver, ENV.get("WEBDRIVER", "Firefox"))


class Engine():

    def __init__(self):
        self.driver = Driver()
        self.lock = Lock()

    def render(self, url):
        with self.lock:
            self.driver.get(url)
            return self.driver.get_screenshot_as_png()


engine = Engine()


@app.route('/')
def screenshot():
    url = request.args.get('url')
    logging.info("Got request for url: %s", url)
    return engine.render(url), 200, {
        'Content-Type': 'image/png',
    }


if __name__ == '__main__':
    app.run(debug=True)
