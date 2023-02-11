#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing the latest version of poetry..."
export POETRY_HOME="$(pwd)/.poetry"
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$POETRY_HOME/bin:$PATH"
poetry --version

poetry install

python manage.py collectstatic --no-input
python manage.py migrate