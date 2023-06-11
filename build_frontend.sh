#!/bin/sh
set -e
cd frontend && npm install && npm run build && cd ..
rm -rf pautobot/frontend-dist || true
mv frontend/dist pautobot/frontend-dist
