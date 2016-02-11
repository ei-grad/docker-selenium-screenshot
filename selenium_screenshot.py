from threading import RLock, local
from multiprocessing.pool import ThreadPool
from os import environ as ENV
import logging.config

from flask import Flask, request

from selenium import webdriver


logging.basicConfig()


app = Flask(__name__)


Driver = getattr(webdriver, ENV.get("WEBDRIVER", "Chrome"))


class RetryFailed(Exception):
    pass


class Engine():

    def __init__(self):
        self.driver = Driver()
        self.lock = RLock()

    def render(self, url, retry=0):
        if retry > 3:
            raise RetryFailed()
        with self.lock:
            try:
                self.driver.get(url)
                return self.driver.get_screenshot_as_png()
            except:
                self.driver = Driver()
                return self.render(url, retry + 1)


thread_local = local()


def thread_init():
    thread_local.engine = Engine()


pool = ThreadPool(int(ENV.get("SCREENSHOT_WORKERS", 4)),
                  thread_init)


def render(url):
    return thread_local.engine.render(url)


@app.route('/')
def screenshot():
    url = request.args.get('url')
    logging.info("Got request for url: %s", url)
    return pool.apply(render, (url,)), 200, {
        'Content-Type': 'image/png',
    }


if __name__ == '__main__':
    app.run(debug=True)
