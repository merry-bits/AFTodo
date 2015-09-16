#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask_todo import app, init_db

if __name__ == "__main__":
    init_db()
    app.run(use_reloader=False)
