#!/bin/sh
cd frontend && npm run build && cd ..
rm -rf pautobot/frontend-dist
mv frontend/dist pautobot/frontend-dist
