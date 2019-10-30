from flask_testing import TestCase
from app import app


# subclass this instead of TestCase
class CreateAppHelperClass(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app


class InitializeRoute(CreateAppHelperClass):
    blank_persistance = {
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

