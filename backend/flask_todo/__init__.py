# -*- coding: utf-8 -*-
from flask import Flask, g
from . import config
app = Flask(__name__)
app.config.from_object(config)

from .db import connect_db, init_db


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# Register URLs.
from . import home
from . import dir_list
