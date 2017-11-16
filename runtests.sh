#!/bin/bash

python -m unittest discover -s tests -p 'test*.py'
result=$?

coverage2 run -m unittest discover -s tests -p 'test*.py'
coverage2 report --show-missing --fail-under=80
coverage2 html --directory=coverage.report

pylint --max-line-length=120 bun/*.py
flake8 --max-line-length=120 bun/*.py

exit $result

