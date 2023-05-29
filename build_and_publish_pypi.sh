#!/bin/sh
bash build_frontend.sh
python -m build --sdist --wheel . && twine upload dist/*
