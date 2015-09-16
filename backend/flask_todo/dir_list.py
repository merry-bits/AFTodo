# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, jsonify

from . import app
from .db import add_todo, exists_todolist, get_todos, mark_done, \
    mark_all_done, reorder


@app.route('/api/list/<todolist_id>/')
def list_api_index(todolist_id, json=True):
    todos = None
    if exists_todolist(todolist_id):
        todos = get_todos(todolist_id)
    # todos: [(id, text, done date, ordering), ]
    if json:
        obj = False
        if todos is not None:
            obj = [
                {'id': tid, 'text': text, 'done': done is not None,
                    'ordering': ordering}
                for tid, text, done, ordering in todos]
        return jsonify(todos=obj)
    return todos


@app.route('/api/list/<todolist_id>/add', methods=['POST'])
def list_api_add(todolist_id, json=True):
    data = request.get_json() if json else request.form
    todo_text = data.get('todo_text', None)
    todo_id = None
    if todo_text:
        todo_id, ordering = add_todo(todolist_id, todo_text)
    if json:
        return jsonify(todo_id=todo_id, ordering=ordering)
    return todo_id, ordering


@app.route('/api/list/<todolist_id>/done', methods=['POST'])
def list_api_done(todolist_id, json=True):
    data = request.get_json() if json else request.form
    todo_id = data.get('todo', None)
    success = False
    if todo_id:
        success = mark_done(todolist_id, todo_id)
    if json:
        return jsonify(success=success)
    return success


@app.route('/api/list/<todolist_id>/reorder', methods=['POST'])
def list_api_reorder(todolist_id, json=True):
    data = request.get_json() if json else request.form
    todo_id = data.get('todo_id', None)
    ordering = data.get('ordering', None)
    new_ordering = []
    if todo_id is not None and ordering is not None:
        new_ordering = reorder(todolist_id, todo_id, ordering)
    if json:
        return jsonify(ordering=new_ordering)
    return new_ordering


@app.route('/api/list/<todolist_id>/all')
def list_api_all(todolist_id, json=True):
    updated = mark_all_done(todolist_id)
    if json:
        return jsonify(updated=updated)
    return updated


@app.route('/list/<todolist_id>/')
def list_index(todolist_id):
    todos = list_api_index(todolist_id, json=False)
    if todos is None:
        return redirect('/')
    todos_left = len([True for _, _, done, _ in todos if done is None])
    return render_template(
        'list_index.html', todolist_id=todolist_id, todos=todos,
        todos_left=todos_left)


@app.route('/list/<todolist_id>/add', methods=['POST'])
def list_add(todolist_id):
    list_api_add(todolist_id, json=False)  # returns (todo_id, ordering)
    return redirect(url_for('list_index', todolist_id=todolist_id))


@app.route('/list/<todolist_id>/done', methods=['POST'])
def list_done(todolist_id):
    list_api_done(todolist_id, json=False)  # returns success, ignored for now
    return redirect(url_for('list_index', todolist_id=todolist_id))


@app.route('/list/<todolist_id>/all')
def list_all(todolist_id):
    list_api_all(todolist_id, json=False)  # returns updated, ignored for now
    return redirect(url_for('list_index', todolist_id=todolist_id))
