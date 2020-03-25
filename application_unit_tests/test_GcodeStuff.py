from unittest import TestCase
from GcodeStuff import Gplus
from Definitions import Material, Machine


class TestGplus(TestCase):
    _E0_TEST_GCODE = [
            ('G1 X0.0000 Y0.0000 E0.000','G1 X0.0000 Y0.0000 '),
            ('G1 X0.0000 Y0.0000 E0.000 F200','G1 X0.0000 Y0.0000  F200'),
            ('G1 X0.0000 Y0.0000 E0.000; some comment','G1 X0.0000 Y0.0000 ; some comment'),
            ('G1 X0.0000 Y0.0000 E0.000 ; comment after space','G1 X0.0000 Y0.0000  ; comment after space'),
            ('G92 E0','G92 E0'),
            ('G1 X0.0000 Y0.0000 E0.001','G1 X0.0000 Y0.0000 E0.001')
            ]
    def test_E0(self):
        M = Machine(model="",
                    temperature_controllers=dict(
                            extruder={"temperature_max": 100,
                                      "part_cooling": True,
                                      "nozzle": {"size_id": 0.4}},
                            chamber={"chamber_heatable": False},
                            printbed={"printbed_heatable": False}))

        M.settings = object()
        M.settings = type('settings_replacement', (), 
                            dict(extrusion_multiplier=1.0,
                                speed_printing=50,
                                retraction_speed=50,
                                track_height=0.1,
                                track_width=0.2))()

        G = Gplus(Material("mat", 1.75),
                M)

        for (inCode, expected) in self._E0_TEST_GCODE:
            with self.subTest(expected=expected):
                G.write(inCode)
                self.assertEqual(G.gcode.split('\n')[-1], expected)
