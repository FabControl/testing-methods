from __future__ import print_function
from Definitions import *
from GcodeStuff import Gplus
from Globals import comment
import numpy as np


class TestSetupA(object):
    def __init__(self, machine: Machine, material: Material, test_info: TestInfo, path: str, parameter_one_min_max: list=None, parameter_two_min_max: list=None, offset: list=None):
        """
        :param machine:
        :param material:
        :param path:
        :param parameter_one_min_max:
        :param parameter_two_min_max:
        """

        self.offset_x = offset[0] if offset else 0
        self.offset_y = offset[1] if offset else 0

        self.part_cooling = machine.temperaturecontrollers.extruder.part_cooling
        if self.part_cooling:
            self.set_part_cooling = machine.settings.part_cooling
        self.ventilator_entry = machine.temperaturecontrollers.chamber.ventilator_entry
        if self.ventilator_entry:
            self.set_ventilator_entry = machine.settings.ventilator_entry
        self.ventilator_exit = machine.temperaturecontrollers.chamber.ventilator_exit
        if self.ventilator_exit:
            self.set_ventilator_exit = machine.settings.ventilator_exit

        self.extruder = machine.temperaturecontrollers.extruder
        self.chamber = machine.temperaturecontrollers.chamber

        self.test_info = test_info
        self.number_of_test_structures = test_info.number_of_test_structures
        self.number_of_substructures = test_info.number_of_substructures
        self.number_of_layers = test_info.number_of_layers
        self.test_name = test_info.name
        self.parameter_one = test_info.parameter_one
        self.parameter_two = test_info.parameter_two

        if test_info.parameter_three:
            self.parameter_three = test_info.parameter_three

        self.raft = test_info.raft

        self.coef_h_raft, self.coef_w_raft, self.coef_h_raft_all, self.coef_w_raft_all = minmax_track_width_height_raft(machine, self.number_of_test_structures)

        if machine.settings.track_height_raft is not None:
            self.coef_h_raft = machine.settings.track_height_raft/machine.temperaturecontrollers.extruder.nozzle.size_id
        if machine.settings.track_width_raft is not None:
            self.coef_w_raft = machine.settings.track_width_raft/machine.temperaturecontrollers.extruder.nozzle.size_id

        self.test_structure_size = get_test_structure_size(machine)

        self.speed_printing = [x*machine.settings.speed_printing for x in [1] * self.number_of_test_structures]
        self.speed_printing_raft = machine.settings.speed_printing_raft

        self.coef_h = [x * machine.settings.track_height / machine.temperaturecontrollers.extruder.nozzle.size_id for x in [1] * self.number_of_test_structures]
        self.coef_w = [x * machine.settings.track_width / machine.temperaturecontrollers.extruder.nozzle.size_id for x in [1] * self.number_of_test_structures]

        if self.raft is False:
            self.abs_z = [x * self.coef_h_raft * machine.temperaturecontrollers.extruder.nozzle.size_id for x in [1] * self.number_of_test_structures]
        else:
            self.abs_z = [(x + self.coef_h_raft) * machine.temperaturecontrollers.extruder.nozzle.size_id for x in self.coef_h]

        self.extrusion_multiplier = [x * machine.settings.extrusion_multiplier for x in [1] * self.number_of_test_structures]
        self.extrusion_multiplier_raft = machine.settings.extrusion_multiplier_raft

        self.temperature_printbed = machine.settings.temperature_printbed
        self.temperature_chamber = machine.settings.temperature_chamber

        self.temperature_extruder = [x * machine.settings.temperature_extruder for x in [1] * self.number_of_test_structures]
        self.temperature_extruder_raft = machine.settings.temperature_extruder_raft

        self.retraction_speed = machine.settings.retraction_speed
        self.retraction_distance = [x * machine.settings.retraction_distance for x in [1] * self.number_of_test_structures]
        self.retraction_restart_distance = [x * machine.settings.retraction_restart_distance for x in [1] * self.number_of_test_structures]
        self.coasting_distance = [x * machine.settings.coasting_distance for x in [1] * self.number_of_test_structures]

        self.extrusion_multiplier_bridging = [x * 1.0 for x in [1] * self.number_of_test_structures]

        self.step_x = [x* np.mean(self.coef_w) * machine.temperaturecontrollers.extruder.nozzle.size_id for x in [1] * self.number_of_test_structures]
        self.step_y = self.test_structure_size - self.coef_w_raft * machine.temperaturecontrollers.extruder.nozzle.size_id / 2

        self.track_height = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in self.coef_h]
        self.track_width = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in self.coef_w]

        if self.test_name == "first-layer track height vs first-layer printing speed":
            # FIRST LAYER HEIGHT test parameters
            if parameter_one_min_max is None:
                self.coef_h = self.coef_h_raft_all
            else:
                self.coef_h = np.linspace(parameter_one_min_max[0] / machine.temperaturecontrollers.extruder.nozzle.size_id, parameter_one_min_max[1] / machine.temperaturecontrollers.extruder.nozzle.size_id, self.number_of_test_structures).tolist()

            self.temperature_extruder_raft = [x * machine.settings.temperature_extruder_raft for x in [1] * self.number_of_test_structures]
            self.temperature_extruder = self.temperature_extruder_raft

            self.abs_z = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in self.coef_h]

            self.parameter_one.values = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in self.coef_h]

            self.step_x = self.track_width

            self.track_height = self.parameter_one.values
            self.track_height_raft = self.parameter_one.values
            self.track_width = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in [self.coef_w_raft] * self.number_of_test_structures]
            self.track_width_raft = self.track_width

            self.speed_printing = self.parameter_two.values
            self.speed_printing_raft = self.parameter_two.values

        elif self.test_name == "first-layer track width":
            # FIRST LAYER WIDTH test parameters
            if parameter_one_min_max is None:
                self.coef_w = self.coef_w_raft_all
            else:
                self.coef_w = np.linspace(parameter_one_min_max[0] / machine.temperaturecontrollers.extruder.nozzle.size_id, parameter_one_min_max[1] / machine.temperaturecontrollers.extruder.nozzle.size_id, self.number_of_test_structures).tolist()

            self.temperature_extruder_raft = [x * machine.settings.temperature_extruder_raft for x in [1] * self.number_of_test_structures]
            self.temperature_extruder = self.temperature_extruder_raft

            self.abs_z = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in self.coef_h]

            self.parameter_one.values = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in self.coef_w]
            self.parameter_two.values = [self.speed_printing_raft] * self.number_of_test_structures
            self.speed_printing = self.parameter_two.values

            self.track_width = self.parameter_one.values
            self.track_height = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in [self.coef_h_raft] * self.number_of_test_structures]
            self.step_x = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in self.coef_w]

        elif self.test_name == "extrusion temperature vs printing speed":
            # EXTRUSION TEMPERATURE test parameters
            if parameter_one_min_max is None:
                self.temperature_extruder = minmax_temperature(material, machine, self.number_of_test_structures)
            else:
                self.temperature_extruder = np.linspace(parameter_one_min_max[0], parameter_one_min_max[1], self.number_of_test_structures).tolist()

            self.parameter_one.values = self.temperature_extruder
            self.speed_printing = self.parameter_two.values

        elif self.test_name == "track height vs printing speed":
            # PATH HEIGHT test parameters
            if parameter_one_min_max is None:
                self.coef_h = minmax_track_height(machine, self.number_of_test_structures)
            else:
                self.coef_h = np.linspace(parameter_one_min_max[0] / machine.temperaturecontrollers.extruder.nozzle.size_id, parameter_one_min_max[1] / machine.temperaturecontrollers.extruder.nozzle.size_id, self.number_of_test_structures).tolist()

            self.abs_z = [(x + self.coef_h_raft) * machine.temperaturecontrollers.extruder.nozzle.size_id for x in self.coef_h]

            self.parameter_one.values = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in self.coef_h]
            self.track_height = self.parameter_one.values
            self.speed_printing = self.parameter_two.values

        elif self.test_name == "track width":
            # PATH WIDTH test parameters
            if parameter_one_min_max is None:
                self.coef_w, _ = minmax_track_width(machine, self.number_of_test_structures)
            else:
                self.coef_w = np.linspace(parameter_one_min_max[0] / machine.temperaturecontrollers.extruder.nozzle.size_id, parameter_one_min_max[1] / machine.temperaturecontrollers.extruder.nozzle.size_id, self.number_of_test_structures).tolist()
            self.step_x = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in self.coef_w]

            self.parameter_one.values = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in self.coef_w]
            self.parameter_two.values = [machine.settings.speed_printing] * self.number_of_substructures

            self.track_width = self.parameter_one.values
            self.speed_printing = self.parameter_two.values

        elif self.test_name == "extrusion multiplier vs printing speed":
            # EXTRUSION MULTIPLIER test parameters
            if parameter_one_min_max is None:
                self.extrusion_multiplier = np.linspace(test_info.parameter_one.min_default, test_info.parameter_one.max_default, self.number_of_test_structures).tolist()
            else:
                self.extrusion_multiplier = np.linspace(parameter_one_min_max[0], parameter_one_min_max[1], self.number_of_test_structures).tolist()

            self.parameter_one.values = self.extrusion_multiplier
            self.speed_printing = self.parameter_two.values

        elif self.test_name == "printing speed":
            # PRINTING SPEED test parameters
            if parameter_one_min_max is None:
                self.speed_printing = np.linspace(test_info.parameter_one.min_default * self.speed_printing[0],
                                                  test_info.parameter_one.max_default * self.speed_printing[0],
                                                  self.number_of_test_structures).tolist()
            else:
                self.speed_printing = np.linspace(parameter_one_min_max[0], parameter_one_min_max[1], self.number_of_test_structures).tolist()
            self.parameter_one.values =  self.speed_printing

        elif self.test_name == "retraction distance":
            # RETRACTION DISTANCE test parameters
            if parameter_one_min_max is None:
                self.retraction_distance = np.linspace(test_info.parameter_one.min_default, test_info.parameter_one.max_default, self.number_of_test_structures).tolist()
            else:
                self.retraction_distance = np.linspace(parameter_one_min_max[0], parameter_one_min_max[1], self.number_of_test_structures).tolist()
            self.parameter_one.values = self.retraction_distance

        elif self.test_name == "retraction-restart distance":
            # RETRACTION RESTART DISTANCE amd COASTING DISTANCE test parameters
            if parameter_one_min_max is None:
                self.retraction_restart_distance = np.linspace(test_info.min_default, test_info.max_default, self.number_of_test_structures).tolist()
            else:
                self.retraction_restart_distance = np.linspace(parameter_one_min_max[0], parameter_one_min_max[1], self.number_of_test_structures).tolist()
            self.coasting_distance = 1.25
            self.parameter_one.values = self.retraction_restart_distance

        elif self.test_name == "bridging extrusion-multiplier vs bridging printing speed":
            # BRIDGING test parameters
            if parameter_one_min_max is None:
                self.extrusion_multiplier_bridging = np.linspace(test_info.parameter_one.min_default, test_info.parameter_one.max_default, self.number_of_test_structures).tolist()
            else:
                self.extrusion_multiplier_bridging = np.linspace(parameter_one_min_max[0], parameter_one_min_max[1], self.number_of_test_structures).tolist()
            self.parameter_one.values = self.extrusion_multiplier_bridging

        elif self.test_name == "extrusion temperature vs retraction distance":
            # RETRACTION DISTANCE vs EXTRUSION TEMPERATURE
            if parameter_two_min_max is None:
                self.retraction_distance = np.linspace(np.mean(self.retraction_distance)-0.25*(self.number_of_substructures-1)/2, np.mean(self.retraction_distance)+0.25*(self.number_of_substructures-1)/2, self.number_of_substructures).tolist()
            else:
                self.retraction_distance = np.linspace(parameter_two_min_max[0], parameter_two_min_max[1], self.number_of_substructures).tolist()

            if parameter_one_min_max is not None:
                self.temperature_extruder = np.linspace(parameter_one_min_max[0], parameter_one_min_max[1], self.number_of_test_structures).tolist()
            else:
                self.temperature_extruder = np.linspace(np.mean(self.temperature_extruder)-5*(self.number_of_test_structures-1)/2, np.mean(self.temperature_extruder)+5*(self.number_of_test_structures-1)/2, self.number_of_test_structures).tolist()

            self.parameter_one.values = self.temperature_extruder
            self.parameter_two.values = self.retraction_distance

        else:
            raise ValueError("{} is not a valid test.".format(test_info.name))

        self.number_of_lines = int(2*self.test_structure_size/((3*self.number_of_test_structures + 1)*np.mean(self.track_width)))

        if self.number_of_lines % 4 == 0:
            pass
        else:
            if self.number_of_lines % 4 == 1:
                self.number_of_lines = self.number_of_lines -1
            if self.number_of_lines % 4 == 2:
                self.number_of_lines = self.number_of_lines -2
            if self.number_of_lines % 4 == 3:
                self.number_of_lines = self.number_of_lines -3

        self.test_structure_width = [0.]

        for current_test_structure in range(self.number_of_test_structures):
            dummy = self.track_width[current_test_structure] * self.number_of_lines
            self.test_structure_width.append(dummy)

        self.test_structure_separation = abs(self.test_structure_size - sum(self.test_structure_width))/(self.number_of_test_structures + 1)

        if parameter_two_min_max is not None:
            if test_info.number_of_substructures == 1:
                self.parameter_two.values = parameter_two_min_max
            else:
                self.parameter_two.values = np.linspace(parameter_two_min_max[0], parameter_two_min_max[1], self.number_of_substructures).tolist()
        else:
            if self.test_name == "bridging extrusion-multiplier vs bridging printing speed":
                self.parameter_two.values = np.linspace(0.50 * self.speed_printing[0], 1.25 * self.speed_printing[0], self.number_of_substructures).tolist()

        volumetric_flow_rate = []
        volumetric_flow_rate_row = []

        if self.number_of_substructures != 1:

            for speed in self.speed_printing:
                for dummy in range(self.number_of_test_structures):
                    if self.test_name == "bridging extrusion-multiplier":
                        value = round(flow_rate(self.track_height[dummy], self.track_width[dummy], speed, self.extrusion_multiplier_bridging[dummy]), 3)
                    else:
                        value = round(flow_rate(self.track_height[dummy], self.track_width[dummy], speed, self.extrusion_multiplier[dummy]), 3)
                    volumetric_flow_rate_row.append(value)
                    if dummy == self.number_of_test_structures-1:
                        volumetric_flow_rate.append(volumetric_flow_rate_row)
                        volumetric_flow_rate_row = []
        else:
            for dummy in range(self.number_of_test_structures):
                value = round(flow_rate(self.track_height[dummy], self.track_width[dummy], self.speed_printing[dummy], self.extrusion_multiplier[dummy]), 3)
                volumetric_flow_rate_row.append(value)
                if dummy == self.number_of_test_structures-1:
                    volumetric_flow_rate.append(volumetric_flow_rate_row)
                    volumetric_flow_rate_row = []

        self.volumetric_flow_rate = volumetric_flow_rate

        self.title = addtitle(test_info, material, machine)
        self.comment1 = addcomment1(self.test_info)
        self.comment2 = addcomment2()
        self.comment3 = addcomment3(self.test_info)

        self.g = Gplus(material, machine,
                       outfile=path,
                       layer_height=self.coef_h_raft * machine.temperaturecontrollers.extruder.nozzle.size_id,
                       extrusion_width=self.coef_w_raft * machine.temperaturecontrollers.extruder.nozzle.size_id,
                       aerotech_include=False, footer=footer, header=header, extrude=True,
                       extrusion_multiplier=self.extrusion_multiplier_raft)

    def get_values_parameter_one(self):
        return [float(self.parameter_one.precision.format(value)) for value in self.parameter_one.values]

    def get_values_parameter_two(self):
        return [float(self.parameter_two.precision.format(value)) for value in self.parameter_two.values]


def addtitle(test_info: TestInfo, material: Material, machine: Machine):
    title = str("; --- " + test_info.name + " 2D test for {0} from {1} (batch: {2}) 3D printed using {3} {4} (SN: {5}) and {6} mm {7} nozzle ---".format(material.name, material.manufacturer, material.id, machine.manufacturer, machine.model, machine.sn, machine.temperaturecontrollers.extruder.nozzle.size_id, machine.temperaturecontrollers.extruder.nozzle.type))
    return title


def addcomment1(test_info: TestInfo):
    comment1 = str("; --- testing the following " + test_info.parameter_one.name + " values: " + ", ".join((test_info.parameter_one.precision + " {}").format(*k) for k in zip(test_info.parameter_one.values, len(test_info.parameter_one.values)*[test_info.parameter_one.units])) + " ---\n")
    if test_info.name not in ["first-layer track width", "track width", "printing speed", "retraction distance"]:
        comment2 = str("; --- and the following " + test_info.parameter_two.name + " values: " + ", ".join((test_info.parameter_two.precision + " {}").format(*k) for k in zip(test_info.parameter_two.values, len(test_info.parameter_two.values)*[test_info.parameter_two.units])) + " ---")
        return comment1+comment2
    return comment1


def addcomment2():
    comment2 = comment

    # for dummy1 in range(0, test_info.number_of_test_structures):
    #     addcomment2 = str("; --- " + "".join("{0}: {1} {2}, ".format(*k) for k in zip(test_parameter_one_name_list, test_parameter_one_precision_list, test_parameter_one_units_list)) +
    #                       " ---").format(*list(map(list, zip(*argument_list)))[dummy1])
    #     comment2.append(addcomment2)

    return comment2


def addcomment3(test_info: TestInfo):
    dummy = []

    for k in range(test_info.number_of_test_structures):
        comment = str("; --- {0}: {1} {2} ---\n").format(test_info.parameter_one.name, test_info.parameter_one.precision, test_info.parameter_one.units)

        dummy.append(comment.format(test_info.parameter_one.values[k]))

    return dummy
