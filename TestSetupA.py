from __future__ import print_function
from Definitions import *
from GcodeStuff import Gplus
import numpy as np


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
        self.coef_h_raft, self.coef_h_min_raft, self.coef_h_max_raft, self.coef_w_raft, self.coef_h_raft_all = minmax_path_width_height_raft(machine)

        if machine.settings.path_height_raft != None:
            self.coef_h_raft = machine.settings.path_height_raft/machine.nozzle.size_id

        self.test_structure_size = get_test_structure_size(machine)
        self.speed_printing = [x*machine.settings.speed_printing for x in [1] * self.number_of_test_structures]
        self.coef_h = [x * machine.settings.path_height / machine.settings.nozzle.size_id for x in [1] * self.number_of_test_structures]

        self.raft = raft
        if raft is False:
            self.abs_z = [x * machine.nozzle.size_id for x in self.coef_h]
        else:
            self.abs_z = [(x + self.coef_h_raft) * machine.nozzle.size_id for x in self.coef_h]

        self.coef_w = [x * machine.settings.path_width / machine.settings.nozzle.size_id for x in [1] * self.number_of_test_structures]
        self.extrusion_multiplier = [x * machine.settings.extrusion_multiplier for x in [1] * self.number_of_test_structures]
        self.temperature_extruder = [x * machine.settings.temperature_extruder for x in [1] * self.number_of_test_structures]
        self.temperature_extruder_raft = [x * machine.settings.temperature_extruder_raft for x in [1] * self.number_of_test_structures]
        self.retraction_speed = 60
        self.retraction_distance = [x * machine.settings.retraction_distance for x in [1] * self.number_of_test_structures]
        self.retraction_restart_distance = [x * machine.settings.retraction_restart_distance for x in [1] * self.number_of_test_structures]
        self.coasting_distance = [x * machine.settings.coasting_distance for x in [1] * self.number_of_test_structures]

        self.step_x = [x* np.mean(self.coef_w) * machine.nozzle.size_id for x in [1] * self.number_of_test_structures]
        self.step_y = self.test_structure_size - self.coef_w_raft * machine.nozzle.size_id / 2

        self.number_of_lines = int(1.25*(self.test_structure_size / (2 * self.number_of_test_structures + 1))/(np.mean(self.coef_w) * machine.nozzle.size_id))

        if min_max_speed_printing is not None:
            self.min_max_speed_printing = np.linspace(min_max_speed_printing[0], min_max_speed_printing[1], 4).tolist()
            
        if test_name == 'first layer height':
            # FIRST LAYER HEIGHT test parameters

            if min_max_argument is None:
                self.coef_h = np.linspace(self.coef_h_min_raft, self.coef_h_max_raft, self.number_of_test_structures).tolist()
            else:
                self.coef_h = np.linspace(min_max_argument[0] / machine.nozzle.size_id, min_max_argument[1] / machine.nozzle.size_id, self.number_of_test_structures).tolist()

            self.abs_z = [x * machine.nozzle.size_id for x in self.coef_h]
            self.argument = self.coef_h

        elif test_name == 'path height':
            # PATH HEIGHT test parameters

            if min_max_argument is None:
                self.coef_h, coef_h_mean = minmax_path_height(machine, self.number_of_test_structures)
            else:
                self.coef_h = np.linspace(min_max_argument[0] / machine.nozzle.size_id, min_max_argument[1] / machine.nozzle.size_id, self.number_of_test_structures).tolist()

            self.abs_z = [(x + self.coef_h_raft) * machine.nozzle.size_id for x in self.coef_h]
            self.argument = self.coef_h

        elif test_name == 'path width':
            # PATH WIDTH test parameters

            if min_max_argument is None:
                self.coef_w, coef_w_mean = minmax_path_width(machine)
            else:
                self.coef_w = np.linspace(min_max_argument[0] / machine.nozzle.size_id, min_max_argument[1] / machine.nozzle.size_id, self.number_of_test_structures).tolist()

            self.step_x = [x * machine.nozzle.size_id for x in self.coef_w]
            self.argument = self.coef_w

        elif test_name == 'printing speed':
            # PRINTING SPEED test parameters

            if min_max_argument is None:
                self.speed_printing = minmax_speed_printing(machine)
            else:
                self.speed_printing = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()

            self.argument = self.speed_printing

        elif test_name == 'extrusion multiplier':
            # EXTRUSION MULTIPLIER test parameters

            if min_max_argument is None:
                self.extrusion_multiplier = minmax_extrusion_multiplier(machine)
            else:
                self.extrusion_multiplier = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()

            self.argument = self.extrusion_multiplier

        elif test_name == 'extrusion temperature':
            # EXTRUSION TEMPERATURE test parameters

            if min_max_argument is None:
                self.temperature_extruder = minmax_temperature(material, machine)
            else:
                self.temperature_extruder = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()

            self.argument = self.temperature_extruder

        elif test_name == 'retraction distance':
            # RETRACTION DISTANCE test parameters

            if min_max_argument is None:
                self.retraction_distance = np.linspace(0.0, 5.0, self.number_of_test_structures).tolist()
            else:
                self.retraction_distance = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()

            self.argument = self.retraction_distance

        elif test_name == 'retraction restart distance and coasting distance':
            # RETRACTION RESTART DISTANCE amd COASTING DISTANCE test parameters

            if min_max_argument is None:
                self.retraction_restart_distance = np.linspace(0.0, 3.0, self.number_of_test_structures).tolist()
            else:
                self.retraction_restart_distance = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()

            self.coasting_distance = np.linspace(0.00, 1.25, 4).tolist()
            self.argument = [self.retraction_restart_distance, self.retraction_restart_distance]

        else:
            print('Unknown test')
            raise ValueError("%s is not a valid test." % test_name)


        self.title = addtitle(test_name, material)
        self.comment1 = addcomment1(self.argument, test_name, machine)
        self.comment2 = addcomment2(self.coef_h, self.coef_w, self.speed_printing, self.extrusion_multiplier, self.temperature_extruder, self.retraction_distance, self.retraction_restart_distance, machine) # TODO

        self.g = Gplus(material, machine,
                       outfile=path,
                       layer_height=self.coef_h_raft * machine.nozzle.size_id,
                       extrusion_width=self.coef_w_raft * machine.nozzle.size_id,
                       aerotech_include=False, footer=footer, header=header, extrude=True,
                       extrusion_multiplier=machine.settings.extrusion_multiplier_raft)


def addtitle(test_name: str, material: Material):
    title = str("; --- 2D test for " + test_name + " of %s from %s (ID: %s) ---" % (material.name, material.manufacturer, material.id))

    return title


def addcomment1(argument, test_name: str, machine: Machine):
    if test_name == 'printing speed':
        comment1 = str('; --- testing the following ' + test_name + ' values: ' + ', '.join('{:.3f} mm/s'.format(k) for k in argument) + ' ---')
    elif test_name == 'temperature':
        comment1 = str('; --- testing the following ' + test_name + ' values: ' + ', '.join('{:.3f} degC'.format(k) for k in argument) + ' ---')
    elif test_name == 'first layer height':
        argument_new = [x * machine.nozzle.size_id for x in argument]
        comment1 = str('; --- testing the following ' + test_name + ' values: ' + ', '.join('{:.3f} mm'.format(k) for k in argument_new) + ' ---')
    elif test_name == 'extrusion multiplier':
        comment1 = str('; --- testing the following ' + test_name + ' values: ' + ', '.join('{:.3f}'.format(k) for k in argument) + ' ---')
    elif test_name == 'extrusion temperature':
        comment1 = str('; --- testing the following ' + test_name + ' values: ' + ', '.join('{:.3f} degC'.format(k) for k in argument) + ' ---')
    elif test_name == 'retraction distance':
        comment1 = str('; --- testing the following ' + test_name + ' values: ' + ', '.join('{:.3f} mm'.format(k) for k in argument) + ' ---')
    elif test_name == 'retraction restart distance and coasting distance':
        comment1 = str('; --- testing the following ' + test_name[:27] + ' values: ' + ', '.join('{:.3f} mm'.format(k) for k in argument[0]) + ' and the following' + test_name[31:] + ' values: ' + ', '.join('{:.3f} mm'.format(j) for j in argument[1]) + ' ---')
    else:
        comment1 = str('; --- testing the following ' + test_name + ' values: ' + ', '.join('{:.3f} mm'.format(k) for k in [x * machine.nozzle.size_id for x in argument]) + ' ---')

    return comment1


def addcomment2(coef_h, coef_w, speed_printing, extrusion_multiplier, temperature_extruder, retraction_distance, retraction_restart_distance, machine):
    comment2 = []
    for dummy1 in range(0, machine.settings.number_of_test_structures):
        addcomment2 = str("; --- path height: %.3f mm, path width: %.3f mm, printing speed: %.1f mm/s, extrusion multiplier: %.2f, extrusion temperature: %.0f degC, retraction distance: %.3f mm, retraction restart distance: %.3f mm  ---" % (
                            round(coef_h[dummy1] * machine.nozzle.size_id, 3),
                            round(coef_w[dummy1] * machine.nozzle.size_id, 3),
                            round(speed_printing[dummy1], 2),
                            round(extrusion_multiplier[dummy1], 2),
                            round(temperature_extruder[dummy1], 0),
                            round(retraction_distance[dummy1], 3),
                            round(retraction_restart_distance[dummy1], 3)))
        comment2.append(addcomment2)

    return comment2
