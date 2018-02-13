from __future__ import print_function
from Definitions import *
from GcodeStuff import Gplus
import numpy as np


class TestSetupB(object):
    def __init__(self, machine: Machine, material: Material, test_name: str, path: str, min_max_argument: list = None, min_max_speed_printing: list = None, raft: bool = True):
        """
        :param machine:
        :param material:
        :param test_name:
        :param path:
        :param min_max:
        """

        self.number_of_test_structures = machine.settings.matrix_size
        self.test_name = test_name

        self.raft = raft

        self.coef_h_raft, _, _, self.coef_w_raft, _ = minmax_path_width_height_raft(machine)

        # if machine.settings.path_height_raft != None:
        #     self.coef_h_raft = machine.settings.path_height_raft/machine.nozzle.size_id
        # if machine.settings.path_width_raft != None:
        #     self.coef_w_raft = machine.settings.path_width_raft/machine.nozzle.size_id

        self.test_structure_size = get_test_structure_size(machine)
        self.speed_printing = np.linspace(min_max_speed_printing[0], min_max_speed_printing[1], self.number_of_test_structures).tolist()

        self.coef_h = [x * machine.settings.path_height / machine.settings.nozzle.size_id for x in [1] * self.number_of_test_structures]
        self.abs_z = [(x + self.coef_h_raft) * machine.nozzle.size_id for x in self.coef_h]
        self.coef_w = [x * machine.settings.path_width / machine.settings.nozzle.size_id for x in [1] * self.number_of_test_structures]
        self.extrusion_multiplier = [x * machine.settings.extrusion_multiplier for x in [1] * self.number_of_test_structures]
        self.temperature_extruder = [x * machine.settings.temperature_extruder for x in [1] * self.number_of_test_structures]
        self.retraction_speed = 60
        self.retraction_distance = [x * machine.settings.retraction_distance for x in [1] * self.number_of_test_structures]
        self.retraction_restart_distance = [x * machine.settings.retraction_restart_distance for x in [1] * self.number_of_test_structures]
        self.coasting_distance = [x * machine.settings.coasting_distance for x in [1] * self.number_of_test_structures]

        self.perimeter = [x * machine.settings.perimeter for x in [1] * self.number_of_test_structures]
        self.overlap = [x * machine.settings.overlap for x in [1] * self.number_of_test_structures]
        self.layers =[x * machine.settings.layers for x in [1] * self.number_of_test_structures]

        self.step_x = [x* np.mean(self.coef_w) * machine.nozzle.size_id for x in [1] * self.number_of_test_structures]
        self.step_y = self.test_structure_size - self.coef_w_raft * machine.nozzle.size_id / 2

        if test_name == 'perimeter':
            # PERIMETER test
            self.perimeter = range(1, 1+self.number_of_test_structures)

            self.argument_row = self.speed_printing
            self.argument_column = self.perimeter

        elif test_name == 'overlap':
            # OVERLAP test
            self.overlap = np.linspace(3, 7, self.number_of_test_structures).tolist()

            self.argument_row = self.speed_printing
            self.argument_column = self.overlap

        elif test_name == 'path height':
            # PATH HEIGHT test
            self.coef_h, _ = minmax_path_height(machine, self.number_of_test_structures)

            self.argument_row = self.speed_printing
            self.argument_column = self.coef_h

        elif test_name == 'temperature':
            # EXTRUSION TEMPERATURE test
            self.temperature_extruder = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()

            self.argument_row = self.speed_printing
            self.argument_column = self.temperature_extruder


        self.title = addtitle(test_name, material)
        self.comment1 = addcomment1(self.argument_column, test_name, machine)
        self.comment2 = addcomment2(self.coef_h, self.coef_w, self.speed_printing, self.extrusion_multiplier, self.temperature_extruder, self.retraction_distance, self.retraction_restart_distance, machine) # TODO

        self.g = Gplus(material, machine,
                       outfile=path,
                       layer_height=self.coef_h_raft * machine.nozzle.size_id,
                       extrusion_width=self.coef_w_raft * machine.nozzle.size_id,
                       aerotech_include=False, footer=footer, header=header, extrude=True,
                       extrusion_multiplier=machine.settings.extrusion_multiplier_raft)


def addtitle(test_name: str, material: Material):
    title = str("; --- 3D test for " + test_name + " of %s from %s (ID: %s) ---" % (material.name, material.manufacturer, material.id))

    return title


def addcomment1(argument_column, test_name: str, machine: Machine):
    if test_name == 'perimeter':
        comment1 = str('; --- testing the following ' + test_name + ' values: ' + ', '.join('{:d}'.format(k) for k in argument_column) + ' ---')
    elif test_name == 'overlap':
        comment1 = str('; --- testing the following ' + test_name + ' values: ' + ', '.join('{:.1f} %'.format(k) for k in argument_column) + ' ---')
    elif test_name == 'path height':
        dummy = [x * machine.nozzle.size_id for x in argument_column]
        comment1 = str('; --- testing the following ' + test_name + ' values: ' + ', '.join('{:.3f} mm'.format(k) for k in dummy) + ' ---')
    elif test_name == 'temperature':
        dummy = [x * machine.nozzle.size_id for x in argument_column]
        comment1 = str('; --- testing the following ' + test_name + ' values: ' + ', '.join('{:.3f} degC'.format(k) for k in dummy) + ' ---')
    else:
        pass
    return comment1


def addcomment2(coef_h, coef_w, speed_printing, extrusion_multiplier, temperature_extruder, retraction_distance, retraction_restart_distance, machine): #TODO
    comment2 = []
    for dummy1 in range(0, machine.settings.matrix_size):
        addcomment2 = str("; --- path height: %.3f mm, path width: %.3f mm, printing speed: %.1f mm/s, extrusion multiplier: %.2f, extrusion temperature: %.0f degC, retraction distance: %.3f mm, retraction restart distance: %.3f mm  ---" % (round(coef_h[dummy1] * machine.nozzle.size_id, 3),
                            round(coef_w[dummy1] * machine.nozzle.size_id, 3),
                            round(speed_printing[dummy1], 2),
                            round(extrusion_multiplier[dummy1], 2),
                            round(temperature_extruder[dummy1], 0),
                            round(retraction_distance[dummy1], 3),
                            round(retraction_restart_distance[dummy1], 3)))
        comment2.append(addcomment2)

    return comment2