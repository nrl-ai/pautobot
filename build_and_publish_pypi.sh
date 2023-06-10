#!/bin/sh
set -e
bash build.sh
python -m twine upload --repository pypi dist/* --skip-existing
