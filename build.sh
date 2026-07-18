#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <filename.py>"
    exit 1
fi

mypy "$1"
python3 "$1"