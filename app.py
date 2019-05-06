#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request, send_file
from persistence import Persistence
import os
from fill_values import fill_values
from initialize_test import OptimizerSession
from base64 import b64encode

app = Flask(__name__)


def json_coupler(persistence, content):
    return {"persistence": persistence, "content": b64encode(content)}


@app.route('/', methods=['POST'])
def initialize():
    if not request.json:
        return jsonify(Persistence(None).dict)
    else:
        persistence = Persistence(request.json)
        session = OptimizerSession(persistence)
        fill_values(persistence)
        return jsonify(json_coupler(persistence, session.g.buffer))


@app.route('/test_json', methods=['POST'])
def test_json():
    persistence = Persistence(request.json)
    return jsonify(persistence.dict)


# @app.route('/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# @app.route('/tasks/<int:task_id>', methods=['GET'])
# def get_task(task_id):
#     task = [task for task in tasks if task["id"] == task_id]
#     if len(task) == 0:
#         abort(404)
#     return jsonify({'task': task[0]})
#
#
# @app.route('/tasks', methods=['POST'])
# def create_task():
#     if not request.json or 'title' not in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': task}), 201


# @app.route('/')
# def index():
#     strIO = StringIO.StringIO()
#     strIO.write('Hello from Dan Jacob and Stephane Wirtel !')
#     strIO.seek(0)
#     return send_file(strIO,
#                      attachment_filename="testing.txt",
#                      as_attachment=True)

# return send_file(buffer, as_attachment=True,
#                      attachment_filename='a_file.txt',
#                      mimetype='text/csv')


if __name__ == '__main__':
    app.run(debug=True)
