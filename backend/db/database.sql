PRAGMA foreign_keys = ON;

drop table if exists todo;
drop table if exists todolist;

create table todolist (
    todolist_id TEXT NOT NULL PRIMARY KEY
);

create table todo (
    todo_id INTEGER NOT NULL PRIMARY KEY ASC,
    todolist_id TEXT NOT NULL REFERENCES todolist,
    todo_text TEXT NOT NULL,
    created TEXT NOT NULL,
    done TEXT DEFAULT NULL,
    ordering INTEGER NOT NULL
);
