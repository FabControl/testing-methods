from unittest import TestCase
from GcodeStuff import Gplus
from Definitions import Material, Machine
import re


class TestGplus(TestCase):
    _E0_TEST_GCODE = [
            ('G1 X0.0000 Y0.0000 E0.000','G1 X0.0000 Y0.0000 '),
            ('G1 X0.0000 Y0.0000 E0.000 F200','G1 X0.0000 Y0.0000  F200'),
            ('G1 X0.0000 Y0.0000 E-0.000 F200','G1 X0.0000 Y0.0000  F200'),
            ('G1 X0.0000 Y0.0000 E0.000; some comment','G1 X0.0000 Y0.0000 ; some comment'),
            ('G1 X0.0000 Y0.0000 E0.000 ; comment after space','G1 X0.0000 Y0.0000  ; comment after space'),
            ('G92 E0','G92 E0'),
            ('G1 X0.0000 Y0.0000 E0.001','G1 X0.0000 Y0.0000 E0.001')
            ]
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


    def test_E0(self):

        G = Gplus(Material("mat", 1.75), self.M)

        for (inCode, expected) in self._E0_TEST_GCODE:
            with self.subTest(expected=expected):
                G.write(inCode)
                self.assertEqual(G.gcode.split('\n')[-1], expected)


    def test_filament_diameter(self):
        G1 = Gplus(Material("mat", 1.0), self.M)
        G2 = Gplus(Material("mat", 2.0), self.M)
        G1.move(x=200, extrude=True)
        G2.move(x=200, extrude=True)

        e1 = re.search(r'E([0-9]+\.[0-9]+)', G1.gcode)
        self.assertIsNotNone(e1)

        e2 = re.search(r'E([0-9]+\.[0-9]+)', G2.gcode)
        self.assertIsNotNone(e2)

        length1 = round(float(e1.group(1)), 5)
        length2 = round(float(e2.group(1)), 5)

        # might fail if g-code command uses less than 6 decimal places
        self.assertEqual(length1, length2 * 2.0 ** 2)

