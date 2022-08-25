#!/usr/bin/env bash

set -x

isort --check-only app
flake8