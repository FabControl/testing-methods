#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request, send_file
from persistence import Persistence
from initialize_test import OptimizerSession
from base64 import b64encode

app = Flask(__name__)


def json_coupler(persistence, test_info, content):
    if content is not None:
        return {"persistence": persistence, "test_info": test_info, "content": b64encode(content.encode()).decode("utf-8")}
    else:
        return {"persistence": persistence, "test_info": test_info, "content": None}


@app.route('/', methods=['POST'])
def initialize():
    if not request.json:
        return jsonify(json_coupler(Persistence(None).dict, Persistence(None).blank_test_info, None))
    else:
        persistence = Persistence(request.json)
        session = OptimizerSession(persistence)
        persistence.update(session.values)
        return jsonify(json_coupler(persistence.dict, persistence.test_info.dict(), str(session.g.gcode)))


@app.route('/test_info', methods=['POST'])
def get_test_info():
    assert request.json["session"] is not None
    persistence = Persistence(request.json)
    return jsonify(persistence.test_info.dict())


@app.route('/routine', methods=['GET', 'POST'])
def get_routine():
    routine = {
        "01": {"name": "First-layer track height vs First-layer printing speed", "priority": "primary"},
        "02": {"name": "First-layer track width", "priority": "secondary"},
        "03": {"name": "Extrusion temperature vs Printing speed", "priority": "primary"},
        "04": {"name": "Track height vs Printing speed", "priority": "secondary"},
        "05": {"name": "Track width", "priority": "secondary"},
        "06": {"name": "Extrusion multiplier vs Printing speed", "priority": "secondary"},
        "07": {"name": "Printing speed", "priority": "secondary"},
        "08": {"name": "Extrusion temperature vs Retraction distance", "priority": "secondary"},
        "09": {"name": "Retraction distance vs Printing speed", "priority": "secondary"},
        "10": {"name": "Retraction distance", "priority": "primary"},
        "11": {"name": "Retraction distance vs Retraction speed", "priority": "secondary"},
        "12": {"name": "Retraction restart distance vs Printing speed and Coasting distance", "priority": "secondary"},
        "13": {"name": "Bridging extrusion multiplier vs Bridging printing speed", "priority": "primary"}
    }
    return jsonify(routine)


@app.route('/config/<slicer>', methods=['POST'])
@app.route('/config/<slicer>/<quality_type>', methods=['POST'])
def serve_config(slicer, quality_type='normal'):
    assert request.json is not None
    from generate_configuration import Converter
    converter = Converter(request.json)
    content = None
    config_format = None
    if "simplify" in slicer:
        content = converter.to_simplify()
        config_format = "fff"
    elif "slic3r_pe" in slicer:
        content = converter.to_prusa().encode()
        config_format = "ini"
    elif "cura" in slicer:
        content = converter.to_cura(quality_type)
        config_format = "curaprofile"
    return jsonify({"format": config_format, "content": b64encode(content).decode()})


@app.route('/report/', methods=['POST'])
def serve_report():
    assert request.json is not None
    from generate_report import generate_report
    content = generate_report(request.json)
    config_format = "pdf"
    return jsonify({"format": config_format, "content": b64encode(content).decode()})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
