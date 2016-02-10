#!/bin/sh

xvfb-run gunicorn -b 0.0.0.0:8000 selenium_screenshot:app
