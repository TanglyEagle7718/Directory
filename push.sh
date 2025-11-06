#!/bin/bash
set -e

python3 updater.py

git add .
git commit -m "Auto-update directory on $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"

git push origin main
