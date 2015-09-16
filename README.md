# To-do list

Simple to-do list implementation on Flask with a SQLite DB and an AngularJS
front-end.


## Features

 - add to-do:s
 - mark a todo as done
 - reorder the list
 - uuid key access
 - no-js functional


# Get it running

The project needs npm, Grunt, Bower a Python environment (optional) and pip
installed. The front-end part then needs some extra work, before the test
server can be started which then can be used to view the to-do page.


## Prerequisites

 - install Node.js and npm
 - install grunt globally:

    ```
    sudo npm install -g grunt-cli
    ```

 - install bower globally:

    ```
    sudo npm install -g bower
    ```

 - (optional) create and activate an empty Python 3 virtual environment with
 pip installed


## Run the project

 - change to the project directory and run the following commands:
 - ```pip install -r requirements.txt```
 - ```npm install```
 - ```grunt```
 - ```cd backend```
 - ```python3 main.py``` 
 - open http://127.0.0.1:5000/
