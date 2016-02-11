#!/bin/sh

[ -z "$SCREENSHOT_WORKERS" ] && export SCREENSHOT_WORKERS="`grep processor /proc/cpuinfo | wc -l`"

xvfb-run gunicorn -b 0.0.0.0:8000 --workers "$SCREENSHOT_WORKERS" selenium_screenshot:app
