#!/bin/sh
set -e
rm -rf pautobot/frontend-dist
rm -rf build
rm -rf dist
rm -rf pautobot.egg-info
rm -rf frontend/.next
rm -rf frontend/dist
bash build_frontend.sh
python -m build --sdist --wheel .
