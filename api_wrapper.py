from flask import Flask, request
import subprocess
'''
generate_suggested_values, session_id, output
cli, session_id
skip_test, session_id, test
fill_value, session_id
generate_report, session_id
generate_configuration, session_id, [optimizer, prusa, simplify, cura]

/?session_id=12345&action=generate_suggested_values
/?session_id=12345&action=cli
/?session_id=12345&action=skip_test&test=01
/?session_id=12345&action=fill_values
/?session_id=12345&action=generate_report
/?session_id=12345&action=generate_configuration&for=optimizer
'''

app = Flask(__name__)


def null_check(token):
    if token is not None:
        return True
    else:
        return False


@app.route('/')
def return_requests():
    session_id = request.args.get('session_id')
    action = request.args.get('action')
    config_target = request.args.get('for')
    test_number = request.args.get('test')

    if action is None:
        raise ValueError("No action specified")

    popen_payload = list(filter(None, ["python3", "{}.py".format(action), str(session_id), config_target, test_number]))
    process = subprocess.Popen(popen_payload, shell=False, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.stdout.read()
