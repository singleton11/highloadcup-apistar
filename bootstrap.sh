#!/usr/bin/env sh
./load_data.py
df
uwsgi --module app:app --http-socket 0.0.0.0:80 --processes 4 --threads 2