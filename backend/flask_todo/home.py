# -*- coding: utf-8 -*-
from flask import redirect, url_for
from uuid import uuid4

from . import app
from .db import create_new_list


@app.route('/')
def index():
    new_id = uuid4().hex
    create_new_list(new_id)
    return redirect(url_for('list_index', todolist_id=new_id))
