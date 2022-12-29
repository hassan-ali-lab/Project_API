from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


# login handle
@app.route('/logins', methods=['POST'])
def handle_login():
    data = request.get_json()
    command = f"""select username, password, isAdmin from Previlages where username = '{data['username']}'
     and password = '{data['password']}';"""
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    record = cur.execute(command).fetchone()
    print(record)
    connection.commit()
    connection.close()
    if record is not None:
    	print({'success': True, 'isAdmin': record[2]})
        return jsonify({'success': True, 'isAdmin': record[2]})
    return jsonify({'success': False, 'isAdmin': -1})


@app.route('/question', methods=['POST'])
def add_question():
    data = request.get_json()
    print(data['question'])
    print(data['option1'])
    print(data['option2'])
    print(data['option3'])
    print(data['option4'])
    print(data['correct_option'])
    command = f"""insert into {data['table_name']} (question, option1, option2, option3, option4, correct_option)
values ('{data['question']}', '{data['option1']}', '{data['option2']}', '{data['option3']}', '{data['option4']}',
 '{data['correct_option']}');"""
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()
    connection.close()
    return jsonify({'success': True})


@app.route('/quizs', methods=['GET'])
def get_quizs_list():
    command = """SELECT tableName FROM Quiz"""
    import sqlite3
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    records = cur.execute(command).fetchall()

    print(records)
    return jsonify(records)


@app.route('/quizquestions/<quiz>', methods=['GET'])
def get_questionns(quiz):
    if quiz is not None:
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()
        records = cur.execute(f"""select * from {quiz}""").fetchall()
        connection.commit()
        connection.close()
        return jsonify(records)
    return jsonify({'result': 'failed'})


@app.route('/quiz/<quiz>', methods=['GET'])
def create_quiz(quiz):
    if quiz is not None:
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()
        cur.execute(f"""insert into Quiz (tableName) values ("{quiz}");""")
        cur.execute(f'''CREATE TABLE {quiz}
(
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    created        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    question       TEXT      NOT NULL,
    option1        TEXT      NOT NULL,
    option2        TEXT      NOT NULL,
    option3        TEXT      NOT NULL,
    option4        TEXT      NOT NULL,
    correct_option TEXT      NOT NULL
);''')
        connection.commit()
        connection.close()
        return jsonify({'result': 'passed'})
    return jsonify({'result': 'failed'})
