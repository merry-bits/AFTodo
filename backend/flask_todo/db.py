# -*- coding: utf-8 -*-
from contextlib import closing
from flask import g
import sqlite3
from datetime import datetime

from . import app


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])  # @UndefinedVariable


def init_db():
    with closing(connect_db()) as db:
        open_resource = app.open_resource  # @UndefinedVariable
        with open_resource('../db/database.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def create_new_list(todolist_id):
    g.db.execute('INSERT INTO todolist(todolist_id) VALUES(?)', [todolist_id])
    g.db.commit()


def exists_todolist(todolist_id):
    cursor = g.db.execute(
        'SELECT todolist_id FROM todolist where todolist_id=?', [todolist_id])
    return cursor.fetchone() is not None


def get_todos(todolist_id):
    cursor = g.db.execute(
        'SELECT todo_id, todo_text, done, ordering '
        'FROM todo '
        'WHERE todolist_id=? '
        'ORDER BY ordering ASC',
        [todolist_id])
    return cursor.fetchall()


def add_todo(todolist_id, text):
    created = datetime.now().strftime(app.config['DATETIME_FORMAT'])
    cursor = g.db.execute(
        'INSERT INTO todo(todolist_id, todo_text, created, ordering) '
        'VALUES(?, ?, ?,'
        '    (SELECT COALESCE(MAX(ordering), 0) + 1 FROM todo '
        '        WHERE todolist_id=?))',
        [todolist_id, text, created, todolist_id])
    todo_id = cursor.lastrowid
    g.db.commit()
    return (
        todo_id,
        g.db.execute(
            'SELECT ordering from todo where todo_id=?',
            [todo_id]).fetchone()[0])


def mark_done(todolist_id, todo_id):
    done = datetime.now().strftime(app.config['DATETIME_FORMAT'])
    cursor = g.db.execute(
        'UPDATE todo SET done=? '
        'WHERE todolist_id=? AND todo_id=? AND done IS NULL',
        [done, todolist_id, todo_id])
    rowcount = cursor.rowcount
    g.db.commit()
    return rowcount > 0


def reorder(todolist_id, todo_id, ordering):
    g.db.execute(
        'UPDATE todo SET ordering=ordering + 1 '
        'WHERE todolist_id=? AND ordering >=?',
        [todolist_id, ordering])
    g.db.execute(
        'UPDATE todo SET ordering=? '
        'WHERE todolist_id=? AND todo_id=?',
        [ordering, todolist_id, todo_id])
    g.db.commit()
    return g.db.execute(
        'SELECT todo_id, ordering '
        'FROM todo '
        'WHERE todolist_id=? '
        'ORDER BY ordering ASC',
        [todolist_id]).fetchall()


def mark_all_done(todolist_id):
    done = datetime.now().strftime(app.config['DATETIME_FORMAT'])
    cursor = g.db.execute(
        'UPDATE todo SET done=? WHERE todolist_id=? AND done IS NULL',
        [done, todolist_id])
    rowcount = cursor.rowcount
    g.db.commit()
    return rowcount
