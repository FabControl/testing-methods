from __future__ import print_function
from Definitions import *
from GcodeStuff import Gplus
import numpy as np
from conversion_dictionary import Params


class TestSetupA(object):
    def __init__(self, machine: Machine, material: Material, test_name: str, path: str, min_max_argument: list = None, min_max_speed_printing: list = None, raft: bool = None):
        """

        :param machine:
        :param material:
        :param test_name:
        :param path:
        :param min_max_argument:
        """

        self.number_of_test_structures = machine.settings.number_of_test_structures
        self.test_name = test_name
        self.coef_h_raft, _, _, self.coef_w_raft, self.coef_h_raft_all = minmax_path_width_height_raft(machine)

        if machine.settings.path_height_raft != None: self.coef_h_raft = machine.settings.path_height_raft/machine.nozzle.size_id
        if machine.settings.path_width_raft != None: self.coef_w_raft = machine.settings.path_width_raft/machine.nozzle.size_id

        self.test_structure_size = get_test_structure_size(machine)

        self.speed_printing = [x*machine.settings.speed_printing for x in [1] * self.number_of_test_structures]
        self.speed_printing_raft = [x * machine.settings.speed_printing_raft for x in [1] * self.number_of_test_structures]

        self.coef_h = [x * machine.settings.path_height / machine.settings.nozzle.size_id for x in [1] * self.number_of_test_structures]
        self.coef_w = [x * machine.settings.path_width / machine.settings.nozzle.size_id for x in [1] * self.number_of_test_structures]

        self.raft = raft

        if raft is False:
            self.abs_z = [x * self.coef_h_raft * machine.nozzle.size_id for x in [1] * self.number_of_test_structures]
        else:
            self.abs_z = [(x + self.coef_h_raft) * machine.nozzle.size_id for x in self.coef_h]

        self.extrusion_multiplier = [x * machine.settings.extrusion_multiplier for x in [1] * self.number_of_test_structures]
        self.temperature_extruder = [x * machine.settings.temperature_extruder for x in [1] * self.number_of_test_structures]
        self.temperature_extruder_raft = [x * machine.settings.temperature_extruder_raft for x in [1] * self.number_of_test_structures]
        self.retraction_speed = machine.settings.retraction_speed
        self.retraction_distance = [x * machine.settings.retraction_distance for x in [1] * self.number_of_test_structures]
        self.retraction_restart_distance = [x * machine.settings.retraction_restart_distance for x in [1] * self.number_of_test_structures]
        self.coasting_distance = [x * machine.settings.coasting_distance for x in [1] * self.number_of_test_structures]

        self.step_x = [x* np.mean(self.coef_w) * machine.nozzle.size_id for x in [1] * self.number_of_test_structures]
        self.step_y = self.test_structure_size - self.coef_w_raft * machine.nozzle.size_id / 2

        self.number_of_lines = int(1.25*(self.test_structure_size / (2 * self.number_of_test_structures + 1))/(np.mean(self.coef_w) * machine.nozzle.size_id))

        path_height = [round(x * machine.nozzle.size_id, 3) for x in self.coef_h]
        path_width = [round(x * machine.nozzle.size_id, 3) for x in self.coef_w]

        if self.number_of_lines % 4 == 0:
            pass
        else:
            if self.number_of_lines % 4 == 1:
                self.number_of_lines = self.number_of_lines + 3
            if self.number_of_lines % 4 == 2:
                self.number_of_lines = self.number_of_lines + 2
            if self.number_of_lines % 4 == 3:
                self.number_of_lines = self.number_of_lines + 1

        if test_name == 'first layer height':
            # FIRST LAYER HEIGHT test parameters

            self.units = ['mm']* self.number_of_test_structures

            self.coef_h = self.coef_h_raft_all if min_max_argument is None else np.linspace(min_max_argument[0]/machine.nozzle.size_id, min_max_argument[1]/machine.nozzle.size_id, self.number_of_test_structures).tolist()

            self.abs_z = [x * machine.nozzle.size_id for x in self.coef_h]
            self.argument = self.coef_h
            self.values = [round(x * machine.nozzle.size_id, 3) for x in self.argument]

            path_height = self.values
            path_width = [round(x * machine.nozzle.size_id, 3) for x in [self.coef_w_raft] * self.number_of_test_structures]

        elif test_name == 'path height':
            # PATH HEIGHT test parameters

            self.units = ['mm']* self.number_of_test_structures

            self.coef_h, _ = minmax_path_height(machine, self.number_of_test_structures) if min_max_argument is None else (np.linspace(min_max_argument[0] / machine.nozzle.size_id, min_max_argument[1] / machine.nozzle.size_id, self.number_of_test_structures).tolist(), (min_max_argument[0] + min_max_argument[1]) / 2 / machine.nozzle.size_id)

            self.abs_z = [(x + self.coef_h_raft) * machine.nozzle.size_id for x in self.coef_h]
            self.argument = [round(x,3) for x in self.coef_h]
            self.values = [x * machine.nozzle.size_id for x in self.argument]

            path_height = self.values

        elif test_name == 'path width':
            # PATH WIDTH test parameters

            self.units = ['mm']* self.number_of_test_structures

            self.coef_w, _ = minmax_path_width(machine) if min_max_argument is None else (np.linspace(min_max_argument[0] / machine.nozzle.size_id, min_max_argument[1] / machine.nozzle.size_id, self.number_of_test_structures).tolist(), (min_max_argument[0] + min_max_argument[1]) / 2 / machine.nozzle.size_id)

            self.step_x = [x * machine.nozzle.size_id for x in self.coef_w]
            self.argument = [round(x,3) for x in self.coef_w]
            self.values = [x * machine.nozzle.size_id for x in self.argument]
            print(self.values)

            path_width = self.values

        elif test_name == 'printing speed':
            # PRINTING SPEED test parameters

            self.units = ['mm/s']* self.number_of_test_structures

            self.speed_printing = minmax_speed_printing(machine) if min_max_argument is None else np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()

            self.argument = [round(x,1) for x in self.speed_printing]
            self.values = self.argument

        elif test_name == 'extrusion multiplier':
            # EXTRUSION MULTIPLIER test parameters

            self.units = ['-']* self.number_of_test_structures

            self.extrusion_multiplier = minmax_extrusion_multiplier(machine) if min_max_argument is None else np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()

            self.argument = [round(x,3) for x in self.extrusion_multiplier]
            self.values = self.argument

        elif test_name == 'extrusion temperature':
            # EXTRUSION TEMPERATURE test parameters

            self.units = ['degC']* self.number_of_test_structures

            self.temperature_extruder = minmax_temperature(material, machine) if min_max_argument is None else np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()

            self.argument = [round(x,0) for x in self.temperature_extruder]
            self.values = self.argument

        elif test_name == 'retraction distance':
            # RETRACTION DISTANCE test parameters

            self.units = ['mm']* self.number_of_test_structures

            self.retraction_distance = np.linspace(0.0, 4.0, self.number_of_test_structures).tolist() if min_max_argument is None else np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()

            self.argument = [round(x, 2) for x in self.retraction_distance]
            self.values = self.argument

        # elif test_name == 'retraction restart distance and coasting distance':
        #     # RETRACTION RESTART DISTANCE amd COASTING DISTANCE test parameters
        #
        #     self.units = ['mm']* self.number_of_test_structures
        #
        #     if min_max_argument is None:
        #         self.retraction_restart_distance = np.linspace(0.0, 3.0, self.number_of_test_structures).tolist()
        #     else:
        #         self.retraction_restart_distance = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()
        #
        #     self.coasting_distance = np.linspace(0.00, 1.25, 4).tolist()
        #     self.argument = [self.retraction_restart_distance, self.coasting_distance]
        #     self.values = self.argument

        else:
            print('Unknown test')
            raise ValueError("%s is not a valid test." % test_name)

        if min_max_speed_printing is not None:
            self.min_max_speed_printing = np.linspace(min_max_speed_printing[0], min_max_speed_printing[1], 4).tolist()
        elif self.test_name != "first layer height":
            self.min_max_speed_printing = self.speed_printing
        if self.test_name == "retraction distance":
            self.min_max_speed_printing = [self.speed_printing[0]]

        q = []
        q_row = []
        for speed in self.min_max_speed_printing:
            for dummy in range(self.number_of_test_structures if test_name != "printing speed" else 1):
                value = round(q_v(path_height[dummy], path_width[dummy], speed, self.extrusion_multiplier[dummy]), 3)
                q_row.append(value)
                if dummy == self.number_of_test_structures-1 or test_name == "printing speed":
                    q.append(q_row)
                    q_row = []
        self.q = q

        self.title = addtitle(test_name, material)
        self.comment1 = addcomment1(self.values, self.units, test_name)
        self.comment2 = addcomment2(path_height, path_width, self.speed_printing, self.extrusion_multiplier, self.temperature_extruder, self.retraction_distance, self.retraction_restart_distance, machine) # TODO add flow rate, brush up the comments!

        self.g = Gplus(material, machine,
                       outfile=path,
                       layer_height=self.coef_h_raft * machine.nozzle.size_id,
                       extrusion_width=self.coef_w_raft * machine.nozzle.size_id,
                       aerotech_include=False, footer=footer, header=header, extrude=True,
                       extrusion_multiplier=machine.settings.extrusion_multiplier_raft)

    def get_values(self):
        return [round(value, 3) for value in self.values]


def addtitle(test_name: str, material: Material):
    title = str("; --- 2D test for " + test_name + " of %s from %s (ID: %s) ---" % (material.name, material.manufacturer, material.id))

    return title


def addcomment1(values, units, test_name: str):
    comment1 = str('; --- testing the following ' + test_name + ' values: ' + ', '.join('{:.3f} {}'.format(*k) for k in zip(values, units)) + ' ---')

    return comment1


def addcomment2(path_height, path_width, speed_printing, extrusion_multiplier, temperature_extruder, retraction_distance, retraction_restart_distance, machine):
    comment2 = []
    for dummy1 in range(0, machine.settings.number_of_test_structures):
        addcomment2 = str("; --- path height: %.3f mm, path width: %.3f mm, printing speed: %.1f mm/s, extrusion multiplier: %.2f, extrusion temperature: %.0f degC, retraction distance: %.3f mm, retraction restart distance: %.3f mm  ---" % (round(path_height[dummy1], 3),
                            round(path_width[dummy1], 3),
                            round(speed_printing[dummy1], 2),
                            round(extrusion_multiplier[dummy1], 2),
                            round(temperature_extruder[dummy1], 0),
                            round(retraction_distance[dummy1], 3),
                            round(retraction_restart_distance[dummy1], 3)))
        comment2.append(addcomment2)

    return comment2