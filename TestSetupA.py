from __future__ import print_function
from conversion_dictionary import Params
from Definitions import *
from GcodeStuff import Gplus
from Globals import test_name_list, test_precision_list, test_units_list
import numpy as np


class TestSetupA(object):
    def __init__(self, machine: Machine, material: Material, test_info: TestInfo, path: str, min_max_argument: list=None, min_max_speed_printing: list=None):
        """
        :param machine:
        :param material:
        :param test_name:
        :param path:
        :param min_max_argument:
        :param min_max_speed_printing:
        :param raft:
        """
        self.test_info = test_info
        self.ventilator_part_cooling =  machine.ventilators.part_cooling
        if self.ventilator_part_cooling:
            self.set_ventilator_part_cooling = machine.settings.ventilator_part_cooling
        self.ventilator_entry = machine.ventilators.entry
        if self.ventilator_entry:
            self.set_ventilator_entry = machine.settings.ventilator_entry
        self.ventilator_exit = machine.ventilators.exit
        if self.ventilator_exit:
            self.set_ventilator_exit = machine.settings.ventilator_exit

        self.number_of_test_structures = test_info.number_of_test_structures
        self.number_of_substructures = test_info.number_of_substructures
        self.number_of_layers = test_info.number_of_layers
        self.test_name = test_info.name

        self.coef_h_raft, self.coef_w_raft, self.coef_h_raft_all, self.coef_w_raft_all = minmax_path_width_height_raft(machine, self.number_of_test_structures) # TODO

        if machine.settings.path_height_raft is not None:
            self.coef_h_raft = machine.settings.path_height_raft/machine.nozzle.size_id
        if machine.settings.path_width_raft is not None:
            self.coef_w_raft = machine.settings.path_width_raft/machine.nozzle.size_id

        self.test_structure_size = get_test_structure_size(machine)

        self.speed_printing = [x*machine.settings.speed_printing for x in [1] * self.number_of_test_structures]
        self.speed_printing_raft = machine.settings.speed_printing_raft

        self.coef_h = [x * machine.settings.path_height / machine.settings.nozzle.size_id for x in [1] * self.number_of_test_structures]
        self.coef_w = [x * machine.settings.path_width / machine.settings.nozzle.size_id for x in [1] * self.number_of_test_structures]

        self.raft = test_info.raft

        if self.raft is False:
            self.abs_z = [x * self.coef_h_raft * machine.nozzle.size_id for x in [1] * self.number_of_test_structures]
        else:
            self.abs_z = [(x + self.coef_h_raft) * machine.nozzle.size_id for x in self.coef_h]

        self.extrusion_multiplier = [x * machine.settings.extrusion_multiplier for x in [1] * self.number_of_test_structures]
        self.extrusion_multiplier_raft = machine.settings.extrusion_multiplier

        if machine.printbed.printbed_heatable:
            self.temperature_printbed = machine.settings.temperature_printbed

        self.temperature_extruder = [x * machine.settings.temperature_extruder for x in [1] * self.number_of_test_structures]
        self.temperature_extruder_raft = machine.settings.temperature_extruder_raft

        self.retraction_speed = machine.settings.retraction_speed
        self.retraction_distance = [x * machine.settings.retraction_distance for x in [1] * self.number_of_test_structures]
        self.retraction_restart_distance = [x * machine.settings.retraction_restart_distance for x in [1] * self.number_of_test_structures]
        self.coasting_distance = [x * machine.settings.coasting_distance for x in [1] * self.number_of_test_structures]

        self.step_x = [x* np.mean(self.coef_w) * machine.nozzle.size_id for x in [1] * self.number_of_test_structures]
        self.step_y = self.test_structure_size - self.coef_w_raft * machine.nozzle.size_id / 2

        self.number_of_lines = int(1.25*(self.test_structure_size / (2 * self.number_of_test_structures + 1))/(np.mean(self.coef_w) * machine.nozzle.size_id))

        self.path_height = [x * machine.nozzle.size_id for x in self.coef_h]
        self.path_width = [x * machine.nozzle.size_id for x in self.coef_w]

        if self.number_of_lines % 4 == 0:
            pass
        else:
            if self.number_of_lines % 4 == 1:
                self.number_of_lines = self.number_of_lines + 3
            if self.number_of_lines % 4 == 2:
                self.number_of_lines = self.number_of_lines + 2
            if self.number_of_lines % 4 == 3:
                self.number_of_lines = self.number_of_lines + 1

        if self.test_name == 'first layer height':
            # FIRST LAYER HEIGHT test parameters
            if min_max_argument is None:
                self.coef_h = self.coef_h_raft_all
            else:
                self.coef_h = np.linspace(min_max_argument[0]/machine.nozzle.size_id, min_max_argument[1]/machine.nozzle.size_id, self.number_of_test_structures).tolist()
            self.temperature_extruder_raft = [x * machine.settings.temperature_extruder_raft for x in [1] * self.number_of_test_structures]
            self.temperature_extruder = self.temperature_extruder_raft

            self.abs_z = [x * machine.nozzle.size_id for x in self.coef_h]
            self.argument = self.coef_h
            self.values = [x * machine.nozzle.size_id for x in self.argument]

            self.path_height = self.values
            self.path_width = [x * machine.nozzle.size_id for x in [self.coef_w_raft] * self.number_of_test_structures]
            self.step_x = self.path_width

        elif self.test_name == 'first layer width':
            # FIRST LAYER WIDTH test parameters
            if min_max_argument is None:
                self.coef_w = self.coef_w_raft_all
            else:
                self.coef_w = np.linspace(min_max_argument[0]/machine.nozzle.size_id, min_max_argument[1]/machine.nozzle.size_id, self.number_of_test_structures).tolist()
            self.temperature_extruder_raft = [x * machine.settings.temperature_extruder_raft for x in [1] * self.number_of_test_structures]
            self.temperature_extruder = self.temperature_extruder_raft

            self.argument = self.coef_w
            self.values = [x * machine.nozzle.size_id for x in self.argument]

            self.path_width = self.values
            self.path_height = [x * machine.nozzle.size_id for x in [self.coef_h_raft] * self.number_of_test_structures]
            self.step_x = [x * machine.nozzle.size_id for x in self.coef_w]

        elif self.test_name == 'extrusion temperature':
            # EXTRUSION TEMPERATURE test parameters
            if min_max_argument is None:
                self.temperature_extruder = minmax_temperature(material, machine, self.number_of_test_structures)
            else:
                self.temperature_extruder = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()
            self.argument = self.temperature_extruder
            self.values = self.argument

        elif self.test_name == 'path height':
            # PATH HEIGHT test parameters
            if min_max_argument is None:
                self.coef_h = minmax_path_height(machine, self.number_of_test_structures)
            else:
                self.coef_h = np.linspace(min_max_argument[0] / machine.nozzle.size_id, min_max_argument[1] / machine.nozzle.size_id, self.number_of_test_structures).tolist()
            self.abs_z = [(x + self.coef_h_raft) * machine.nozzle.size_id for x in self.coef_h]
            self.argument = self.coef_h
            self.values = [x * machine.nozzle.size_id for x in self.argument]
            self.path_height = self.values

        elif self.test_name == 'path width':
            # PATH WIDTH test parameters
            if min_max_argument is None:
                self.coef_w, _ = minmax_path_width(machine, self.number_of_test_structures)
            else:
                self.coef_w = np.linspace(min_max_argument[0] / machine.nozzle.size_id, min_max_argument[1] / machine.nozzle.size_id, self.number_of_test_structures).tolist()
            self.step_x = [x * machine.nozzle.size_id for x in self.coef_w]
            self.argument = self.coef_w
            self.values = [x * machine.nozzle.size_id for x in self.argument]
            self.path_width = self.values

        elif self.test_name == 'extrusion multiplier':
            # EXTRUSION MULTIPLIER test parameters
            if min_max_argument is None:
                self.extrusion_multiplier = np.linspace(test_info.min_default, test_info.max_default, self.number_of_test_structures).tolist()
            else:
                self.extrusion_multiplier = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()
            self.argument = self.extrusion_multiplier
            self.values = self.argument

        elif self.test_name == 'printing speed':
            # PRINTING SPEED test parameters
            if min_max_argument is None:
                self.speed_printing = np.linspace(test_info.min_default * self.speed_printing[0],
                                                  test_info.max_default * self.speed_printing[0],
                                                  self.number_of_test_structures).tolist()
            else:
                self.speed_printing = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()
            self.argument = self.speed_printing
            self.values = self.argument

        elif self.test_name == 'retraction distance':
            # RETRACTION DISTANCE test parameters
            if min_max_argument is None:
                self.retraction_distance = np.linspace(test_info.min_default, test_info.max_default, self.number_of_test_structures).tolist()
            else:
                self.retraction_distance = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()
            self.argument = self.retraction_distance
            self.values = self.argument

        elif self.test_name == 'retraction restart distance':
            # RETRACTION RESTART DISTANCE amd COASTING DISTANCE test parameters
            if min_max_argument is None:
                self.retraction_restart_distance = np.linspace(test_info.min_default, test_info.max_default, self.number_of_test_structures).tolist()
            else:
                self.retraction_restart_distance = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()
            self.coasting_distance = 1.25
            self.argument = self.retraction_restart_distance
            self.values = self.argument

        elif self.test_name == 'bridging':
            # BRIDGING test parameters
            if min_max_argument is None:
                self.extrusion_multiplier_bridging = np.linspace(test_info.min_default, test_info.max_default, self.number_of_test_structures).tolist()
            else:
                self.extrusion_multiplier_bridging = np.linspace(min_max_argument[0], min_max_argument[1], self.number_of_test_structures).tolist()

            self.argument = self.extrusion_multiplier_bridging
            self.values = self.argument

        else:
            print('Unknown test')
            raise ValueError("{} is not a valid test.".format(test_info.name))

        if min_max_speed_printing is not None:
            self.min_max_speed_printing = np.linspace(min_max_speed_printing[0], min_max_speed_printing[1], self.number_of_substructures).tolist()
        if self.test_name == "retraction distance":
            self.min_max_speed_printing = [self.speed_printing[0]]

        volumetric_flow_rate = []
        volumetric_flow_rate_row = []

        for speed in self.min_max_speed_printing:
            for dummy in range(self.number_of_test_structures if self.test_name != "printing speed" else 1):
                value = round(flow_rate(self.path_height[dummy], self.path_width[dummy], speed, self.extrusion_multiplier[dummy]), 3)
                volumetric_flow_rate_row.append(value)
                if dummy == self.number_of_test_structures-1 or self.test_name == "printing speed":
                    volumetric_flow_rate.append(volumetric_flow_rate_row)
                    volumetric_flow_rate_row = []
        self.volumetric_flow_rate = volumetric_flow_rate

        self.title = addtitle(test_info, material, machine)
        self.comment1 = addcomment1(self.test_info, self.values)
        argument_list = [self.temperature_extruder, self.path_height, self.path_width, self.extrusion_multiplier, self.speed_printing, self.retraction_distance, self.retraction_restart_distance, self.extrusion_multiplier_bridging]
        self.comment2 = addcomment2(self.test_info, argument_list)

        self.g = Gplus(material, machine,
                       outfile=path,
                       layer_height=self.coef_h_raft * machine.nozzle.size_id,
                       extrusion_width=self.coef_w_raft * machine.nozzle.size_id,
                       aerotech_include=False, footer=footer, header=header, extrude=True,
                       extrusion_multiplier=self.extrusion_multiplier_raft)

    def get_values(self):
        return [round(value, 3) for value in self.values]


def addtitle(test_info: TestInfo, material: Material, machine: Machine):
    title = str("; --- 2D test for " + test_info.parameter + " of {0} from {1} (ID: {2}) using {3} {4} (SN: {5}) and {6} mm {7} nozzle---".format(material.name, material.manufacturer, material.id, machine.manufacturer, machine.model, machine.sn, machine.nozzle.size_id, machine.nozzle.type))
    return title


def addcomment1(test_info: TestInfo, values: list):
    comment1 = str('; --- testing the following ' + test_info.parameter + ' values: ' + ', '.join((test_info.precision + ' {}').format(*k) for k in zip(values, len(values)*[test_info.units])) + ' ---')
    return comment1


def addcomment2(test_info: TestInfo, argument_list: list):
    comment2 = []

    for dummy1 in range(0, test_info.number_of_test_structures):
        addcomment2 = str("; --- " + "".join("{0}: {1} {2}, ".format(*k) for k in zip(test_name_list[2:], test_precision_list[2:], test_units_list[2:])) +
                          " ---").format(*list(map(list, zip(*argument_list)))[dummy1])
        comment2.append(addcomment2)

    return comment2
