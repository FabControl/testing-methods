from flask_testing import TestCase
from app import app
import json
from base64 import b64decode
from .persistences import PersistencesIterator
import re


# subclass this instead of TestCase
class CreateAppHelperClass(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app


class InitializeRoute(CreateAppHelperClass):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.blank_persistance = {
                "machine": {
                    "buildarea_maxdim1": None,
                    "buildarea_maxdim2": None,
                    "firmware": {
                        "fw_type": "fw_type",
                        "version": "2.0"
                        },
                    "form": None,
                    "manufacturer": None,
                    "max_dimension_z": None,
                    "model": None,
                    "sn": None,
                    "gcode_header": "",
                    "gcode_footer": "",
                    "software": {
                        "version": "version"
                        },
                    "temperature_controllers": {
                        "chamber": {
                            "chamber_heatable": False,
                            "gcode_command": "M141 S{0}",
                            "temperature_chamber_setpoint": None,
                            "temperature_max": None,
                            "temperature_min": None,
                            "tool": "",
                            "ventilator_entry": False,
                            "ventilator_entry_gcode_command": "M106 {0} S{1}",
                            "ventilator_entry_tool": "P2",
                            "ventilator_exit": False,
                            "ventilator_exit_gcode_command": "M106 {0} S{1}",
                            "ventilator_exit_tool": "P1"
                            },
                        "extruder": {
                            "gcode_command": "M109 S{0} {1}",
                            "gcode_command_immediate": "M104 S{0} {1}",
                            "nozzle": {
                                "size_angle": None,
                                "size_capillary_length": None,
                                "size_extruder_id": 1.95,
                                "size_id": None,
                                "size_od": None,
                                "type": None
                                },
                            "part_cooling": True,
                            "part_cooling_gcode_command": "M106 S{0}",
                            "part_cooling_setpoint": None,
                            "temperature_max": None,
                            "temperature_min": None,
                            "tool": ""
                            },
                        "printbed": {
                            "coating": "None",
                            "gcode_command": "M190 S{0}",
                            "gcode_command_immediate": "M140 S{0}",
                            "material": "?",
                            "printbed_heatable": False,
                            "temperature_max": None,
                            "temperature_min": None,
                            "tool": "T1"
                            }
                        }
                    },
                "material": {
                        "density_rt": None,
                        "drying": {
                            "dried": False,
                            "drying_airflow": 0,
                            "drying_temperature": 0,
                            "drying_time": 0,
                            "feeding_airflow": 0,
                            "feeding_temperature": 0
                            },
                        "id": None,
                        "load_mfr": None,
                        "manufacturer": None,
                        "material_group": "non-filled",
                        "mvr": None,
                        "name": None,
                        "size_od": None,
                        "temperature_glass": None,
                        "temperature_mfr": None
                        },
                "session": {
                        "min_max_parameter_one": [],
                        "min_max_parameter_three": [],
                        "min_max_parameter_two": [],
                        "number_of_test_structures": 7,
                        "offset": [
                            0,
                            0
                            ],
                        "previous_tests": [],
                        "slicer": "prusa slic3r",
                        "target": "mechanical_strength",
                        "test_number": "01",
                        "test_type": "A",
                        "uid": 135,
                        "user_id": None
                        },
                "settings": {
                        "bridging_extrusion_multiplier": 0,
                        "bridging_part_cooling": 0,
                        "bridging_speed_printing": 0,
                        "coasting_distance": 0,
                        "critical_overhang_angle": 27.0,
                        "extrusion_multiplier": None,
                        "optimize_speed_printing": True,
                        "part_cooling_setpoint": 0,
                        "raft_density": 100,
                        "retraction_distance": 0,
                        "retraction_restart_distance": 0,
                        "retraction_speed": 0,
                        "speed_printing": 0,
                        "speed_printing_raft": None,
                        "speed_travel": 140,
                        "temperature_chamber_setpoint": 0,
                        "temperature_extruder": None,
                        "temperature_extruder_raft": None,
                        "temperature_printbed_setpoint": 0,
                        "track_height": None,
                        "track_height_raft": None,
                        "track_width": None,
                        "track_width_raft": None
                        }
                }


    def assertCoupledCorrectly(self, resp):
        expectedKeys = ["persistence", "test_info", "content"]
        expectedKeys.sort()
        receivedKeys = list(resp.json.keys())
        receivedKeys.sort()
        self.assertTrue(expectedKeys == receivedKeys)

    def test_empty_post(self):
        resp = self.client.post('/')
        self.assert200(resp)
        self.assertCoupledCorrectly(resp)

        self.assertTrue(resp.json['content'] is None)
        self.assertEqual(resp.json['persistence'], self.blank_persistance)


class NotFoundRoute(CreateAppHelperClass):
    def test_route_response(self):
        resp = self.client.get('/some_not_existing_endpoint/')
        self.assert404(resp)
        self.assertEqual(resp.json, dict(error='Not found'))

class RoutineRoute(CreateAppHelperClass):
    def test_get_routine(self):
        resp = self.client.get('/routine')
        self.assert200(resp)
        self.assertEqual(sorted(resp.json.keys()),
                # For some reason test number 12 is missing
                list('{0:02}'.format(x) for x in range(1, 14)))

        # all routine subitems should be dict, containing only name and priority keys
        self.assertTrue(all(sorted(x.keys()) == ['name', 'priority'] for x in resp.json.values()))

        # Priority can only be primary or secondary
        self.assertTrue(all(x['priority'] in ['primary', 'secondary'] for x in resp.json.values()))

class GcodeRoute(CreateAppHelperClass):
    def test_gcode_header_footer(self):
        header = "Test header included"
        footer = "Footer test passed"
        for test_name, p in PersistencesIterator():
            p["machine"]["gcode_header"] = header
            p["machine"]["gcode_footer"] = footer
            print(test_name)
            resp = self.client.post('/',
                                    data=json.dumps(p),
                                    content_type='application/json')

            self.assert200(resp, message=test_name)

            g_lines = b64decode(resp.json["content"]).decode().split('\n')
            # For some unknown reason, G91 is included before header
            self.assertEqual(header, g_lines[1], test_name)
            self.assertEqual(footer, g_lines[-1], test_name)

    def test_gcode_validity(self):
        invalid_F_matcher = re.compile(' F[0-9]+\.[0-9]+')
        # check if regex works
        self.assertIsNotNone(invalid_F_matcher.search('G28\nG1 F20.0\nG1 X50'))

        invalid_S_matcher = re.compile(' S[0-9]+\.[0-9]+')
        # check if regex works
        self.assertIsNotNone(invalid_S_matcher.search('G28\nM104 S120.0\nG1 X50'))

        for test_name, p in PersistencesIterator():
            print(test_name)
            resp = self.client.post('/',
                                    data=json.dumps(p),
                                    content_type='application/json')
            self.assert200(resp, message=test_name)

            g_lines = b64decode(resp.json["content"]).decode()

            with self.subTest(msg='F not formatted as integer', test_name=test_name):
                self.assertIsNone(invalid_F_matcher.search(g_lines), msg=test_name)

            with self.subTest(msg='S not formatted as integer', test_name=test_name):
                self.assertIsNone(invalid_S_matcher.search(g_lines), msg=test_name)

            with self.subTest(msg='F0 found in generated g-code', test_name=test_name):
                self.assertFalse('G1 F0' in g_lines.split('\n'), msg=test_name)

            with self.subTest(msg='Missing/multiple homings in generated g-code', test_name=test_name):
                self.assertEqual(g_lines.count('This is homing sequence'), 1, msg=test_name)
