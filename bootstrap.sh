#!/usr/bin/env sh
./load_data.py
df
uwsgi --module app:app --http 0.0.0.0:80 --processes 8 --threads 4