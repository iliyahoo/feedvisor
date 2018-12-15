from typing import List, Dict
from flask import Flask
import mysql.connector
import json


app = Flask(__name__)

# DB connection config
config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'knights'
}


# execute SQL queries
def db(command, get_cursor):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(command)
    # COMMIT if sql query is not 'select'
    if command.split()[0].lower() != 'select':
        connection.commit()
        results = True
    else:
        results = eval(get_cursor)
    cursor.close()
    connection.close()
    return results


def increment() -> str:
    # SELECT
    command = 'SELECT views FROM feedvisor;'
    get_cursor = '[x for x in cursor][0][0]'
    # increment by 1
    results = db(command, get_cursor) + 1
    # UPDATE
    command = 'UPDATE feedvisor SET views = %s;' % results
    db(command, get_cursor)
    return results


def favorite_colors() -> List[Dict]:
    command = 'SELECT name, color FROM favorite_colors'
    get_cursor = '[{name: color} for (name, color) in cursor]'
    results = db(command, get_cursor)
    return results


@app.route('/')
def index() -> str:
    return json.dumps({'favorite_colors': favorite_colors()})


@app.route('/counter')
def counter() -> str:
    return "counter: %s" % increment()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
