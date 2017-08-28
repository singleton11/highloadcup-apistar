#!/usr/bin/env sh
./load_data.py
gunicorn app:app --workers=4 --bind=0.0.0.0:80 --pid=pid --worker-class=meinheld.gmeinheld.MeinheldWorker