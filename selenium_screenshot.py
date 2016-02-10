from threading import Lock
import logging.config

from flask import Flask, request

from selenium import webdriver


logging.basicConfig()


app = Flask(__name__)


class Engine():

    def __init__(self):
        self.driver = webdriver.Firefox()
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
