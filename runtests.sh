#!/bin/bash

PY=3.9

python${PY} -m unittest discover -s tests -p 'test*.py'
result=$?

coverage-${PY} run -m unittest discover -s tests -p 'test*.py'
coverage-${PY} report --show-missing --fail-under=80
coverage-${PY} html --directory=coverage.report

pylint --max-line-length=120 bun/*.py
flake8 --max-line-length=120 bun/*.py

exit $result

