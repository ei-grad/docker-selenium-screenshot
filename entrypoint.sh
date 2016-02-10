#!/bin/sh

xvfb-run gunicorn -b 0.0.0.0:8000 selenum_screenshot:app
