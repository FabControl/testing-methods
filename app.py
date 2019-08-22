#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request, send_file
from persistence import Persistence
from initialize_test import OptimizerSession
from base64 import b64encode

app = Flask(__name__)


def json_coupler(persistence, content):
    if content is not None:
        return {"persistence": persistence, "content": b64encode(content.encode()).decode("utf-8")}
    else:
        return {"persistence": persistence, "content": None}


@app.route('/', methods=['POST'])
def initialize():
    if not request.json:
        return jsonify(json_coupler(Persistence(None).dict, None))
    else:
        persistence = Persistence(request.json)
        persistence.fill_values()
        session = OptimizerSession(persistence)
        return jsonify(json_coupler(persistence.dict, str(session.g.gcode)))


@app.route('/test_info', methods=['POST'])
def get_test_info():
    assert request.json["session"] is not None
    persistence = Persistence(request.json)
    return jsonify(persistence.test_info.dict())


@app.route('/routine', methods=['GET', 'POST'])
def get_routine():
    routine = {
        "01": {"name": "first-layer track height vs first-layer printing speed", "priority": "primary"},
        "02": {"name": "first-layer track width", "priority": "secondary"},
        "03": {"name": "extrusion temperature vs printing speed", "priority": "primary"},
        "05": {"name": "track width", "priority": "secondary"},
        "06": {"name": "extrusion multiplier vs printing speed", "priority": "secondary"},
        "07": {"name": "printing speed", "priority": "primary"},
        "08": {"name": "extrusion temperature vs retraction distance", "priority": "primary"},
        "09": {"name": "retraction distance vs printing speed", "priority": "secondary"},
        "10": {"name": "retraction distance", "priority": "secondary"},
        "11": {"name": "retraction distance vs retraction speed", "priority": "secondary"},
        "12": {"name": "retraction-restart distance vs coasting distance", "priority": "secondary"},
        "13": {"name": "bridging extrusion multiplier vs bridging printing speed", "priority": "primary"}
    }
    return jsonify(routine)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True, host="ec2-54-93-100-66.eu-central-1.compute.amazonaws.com")
