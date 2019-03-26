from CLI_helpers import separator
import json
import jsonpickle
import math
import numpy as np
from paths import header, footer

class DryingProcess(object):
    """
    definition of the drying process:
    dried                 - True / False
    drying_temperature    - drying temperature(degC)
    drying_time           - drying time (min)
    drying_airflow        - airflow during drying (%)
    feeding_temperature   - feeding temperature(degC)
    feeding_airflow       - airflow during feeding(%)
    """
    def __init__(self, dried: bool, drying_temperature: int, drying_time: int, drying_airflow: int, feeding_temperature: int, feeding_airflow: int, *args, **kwargs):
        self.dried = dried
        if self.dried:
            self.drying_temperature = drying_temperature
            self.drying_time = drying_time
            self.drying_airflow = drying_airflow
            self.feeding_temperature = feeding_temperature
            self.feeding_airflow = feeding_airflow


class Material(object):
    """
    definition of the filament properties:
    name                   - filament name
    manufacturer           - manufacturer's/supplier's name
    id                     - material ID
    size_od                - outer diameter
    temperature_melting    - melting point (degC)
    temperature_destr      - destruction temperature in air (degC)
    temperature_glass      - glass transition temperature (degC)
    temperature_vicat      - Vicat softening point (degC)
    mvr                    - melt flow rate (cm3)
    mfi                    - melt flow index (g)
    temperature_mfr        - temperature at which MFR has been determined (degC)
    load_mfr               - load under which the MFR has been determined (kg)
    capillary_length_mfr   - capillary length in the MFR measurement device (mm)
    capillary_diameter_mfr - capillary diameter in the MFR measurement device (mm)
    time_mfr               - extrusion time in the MFR experiment (min)
    density_rt             - density at RT (g/cc)
    lcte                   - linear coefficient of thermal expansion (1/K)
    heat_capacity          - specific heat capacity (J/kg/K)
    """

    def __init__(self, name, manufacturer, material_group=None, polymer_class=None, id=None, size_od: float=None,
                 temperature_melting=None, temperature_destr=None, temperature_glass=None, temperature_vicat=None,
                 mvr=None, mfi=None, temperature_mfr=None, load_mfr=None, capillary_length_mfr=None, capillary_diameter_mfr=None,
                 time_mfr=None, density_rt=None, lcte=None, heat_capacity=None, price_eur_per_kg=None, *args, **kwargs):
        self.name = name
        self.material_group = material_group
        self.polymer_class = polymer_class
        self.manufacturer = manufacturer
        self.id = id
        self.size_od = size_od
        self.temperature_melting = temperature_melting
        self.temperature_destr = temperature_destr
        self.temperature_glass = temperature_glass
        self.temperature_vicat = temperature_vicat
        self.mvr = mvr  # respect the units: mm3/time
        self.mfi = mfi  # respect the units: g/time
        self.temperature_mfr = 220 if temperature_mfr is None else temperature_mfr
        self.capillary_diameter_mfr = 2.095 if capillary_diameter_mfr is None else capillary_diameter_mfr  # respect the units: mm
        self.capillary_length_mfr = 8 if capillary_length_mfr is None else capillary_length_mfr  # respect the units: mm
        self.time_mfr = 10 if time_mfr is None else time_mfr  # respect the units: min
        self.density_rt = 1 if density_rt is None else density_rt  # respect the units: g/cm3
        self.lcte = lcte
        self.load_mfr = load_mfr  # respect the units: kg
        self.heat_capacity = heat_capacity  # respect the units: J / K / g
        self.price_eur_per_kg = price_eur_per_kg
        self.drying = None


class Chamber(object):
    """

    """

    def __init__(self, chamber_heatable: bool, ventilator_exit: bool, ventilator_entry: bool, tool: str=None, gcode_command: str=None, temperature_min: float=None, temperature_max: float=None, temperature_chamber_setpoint: float=None, ventilator_exit_tool: str=None, ventilator_exit_gcode_command: str=None, ventilator_entry_tool: str=None, ventilator_entry_gcode_command: str=None, *args, **kwargs):
        self.chamber_heatable = chamber_heatable
        if chamber_heatable:
            self.tool = tool  # tool number, e.g. T1, T2
            self.gcode_command = gcode_command  # G-code command used to control the temperature of the nozzle, e.g. Mddd {0} S{1}, where {0} is a tool string
            self.temperature_max = temperature_max
            self.temperature_min = temperature_min
            self.temperature_chamber_setpoint = temperature_chamber_setpoint

        self.ventilator_exit = ventilator_exit
        self.ventilator_entry = ventilator_entry

        if ventilator_exit:
            self.ventilator_exit_tool = ventilator_exit_tool
            self.ventilator_exit_gcode_command = ventilator_exit_gcode_command

        if ventilator_entry:
            self.ventilator_entry_tool = ventilator_entry_tool
            self.ventilator_entry_gcode_command = ventilator_entry_gcode_command


class Printbed(object):
    """

    """
    def __init__(self, printbed_heatable: bool, tool: str, gcode_command: str, temperature_max: float, temperature_min: float, material: str, coating: str, gcode_command_immediate=None, *args, **kwargs):
        self.printbed_heatable = printbed_heatable
        if printbed_heatable:
            self.tool = tool
            self.gcode_command = gcode_command  # G-code command used to control the temperature of the print bed, e.g. Mddd {0} S{1}, where {0} is a tool string
            self.gcode_command_immediate = gcode_command_immediate  # G-code command used to control the temperature of the print bed, e.g. Mddd {0} S{1}, where {0} is a tool string
            self.temperature_max = temperature_max
            self.temperature_min = temperature_min

        self.material = material
        self.coating = coating


class Nozzle(object):
    """
    definition of the nozzle properties:
    id - nozzle id
    size_id - inner diameter of the nozzle (mm)
    size_od - outer diameter of the nozzle (mm)
    size_capillary_length - length of the capillary in the nozzle (mm)
    size_angle - angle in the nozzle (deg)
    size_extruder_id - inner diameter of the extruder (mm)
    type - nozzle metal (e.g. brass or steel)
    """

    def __init__(self, size_id: float, size_od: float, type: str, size_capillary_length=None, size_angle=None, size_extruder_id=None, *args, **kwargs):
        self.size_id = size_id  # respect the units: mm
        self.size_od = size_od  # respect the units: mm
        self.size_capillary_length = size_capillary_length  # respect the units: mm
        if size_angle:
            self.size_angle = math.radians(size_angle)  # respect the units: conversion from angles to radians
        self.size_extruder_id = size_extruder_id  # respect the units: mm
        self.type = type


class Extruder(object):
    """

    """
    def __init__(self, temperature_max: float, temperature_min: float, part_cooling: bool, tool: str, gcode_command: str = "M109 S{} {}", gcode_command_immediate=None, part_cooling_gcode_command:str=None, *args, **kwargs):
        if tool == "":
            self.tool = "T0"  # tool number, e.g. T1, T2
        else:
            self.tool = tool
        self.gcode_command = gcode_command  # G-code command used to control the temperature, e.g. M104 {0} S{1}, where {0} is a tool string
        self.gcode_command_immediate = gcode_command_immediate  # G-code command used to control the temperature, e.g. M104 {0} S{1}, where {0} is a tool string
        self.temperature_max = temperature_max
        self.temperature_min = temperature_min
        self.part_cooling = part_cooling
        if part_cooling:
            self.part_cooling_gcode_command = part_cooling_gcode_command
        self.nozzle = Nozzle(**kwargs["nozzle"])


class TemperatureControllers(object):
    """
    """
    def __init__(self, *args, **kwargs):
        self.extruder = Extruder(**kwargs["extruder"])
        self.chamber = Chamber(**kwargs["chamber"])
        self.printbed = Printbed(**kwargs["printbed"])


class Software(object):
    """
    """
    def __init__(self, version: str, *args, **kwargs):
        self.version = version


class Firmware(object):
    """
    """

    def __init__(self, fw_type: str, version: str, *args, **kwargs):
        self.fw_type = fw_type
        self.version = version


class Machine(object):
    """
    definition of the machine (i.e. 3D printer):
    id - machine ID
    manufacturer - machine's manufacturer
    model - machine's model
    sn - machine's SN
    buildarea_maxdim1 - maximum buildarea in dimension 1 (mm)
    buildarea_maxdim2 - maximum buildarea in dimension 2 (mm)
    """

    def __init__(self, id: str=None, manufacturer: str=None, model: str=None, sn: str=None, form: str=None, buildarea_maxdim1: float=None, buildarea_maxdim2: float=None,
                 *args, **kwargs):

        self.id = id
        self.manufacturer = manufacturer
        self.model = model
        self.sn = sn
        self.form = form
        self.buildarea_maxdim1 = buildarea_maxdim1  # respect the units: mm
        self.buildarea_maxdim2 = buildarea_maxdim2  # respect the units: mm

        self.temperaturecontrollers = TemperatureControllers(**kwargs["temperature_controllers"])
        self.software = Software(**kwargs["software"])
        self.firmware = Firmware(**kwargs["firmware"])


class Settings(object):
    """
    definition of the user's settings:
    track_height - height of the path (mm)
    track_width - width of the path (mm)
    temperature_extruder_raft - temperature of the extruder when printing the first layer (mm)
    temperature_printbed_raft - temperature of the printbed when printing the first layer (mm)
    extrusion_multiplier_raft - when printing the first layer (1)
    speed_printing_raft - printing speed when printing the first layer (mm/s)
    temperature_extruder - temperature of the extruder (mm)
    temperature_printbed - temperature of the printbed (mm)
    extrusion_multiplier - (1)
    speed_printing - printing speed (mm/s)
    part_cooling - cooler power (%)
    raft_density - raft filling density (%)
    retraction_distance - retraction distance (mm)
    """

    def __init__(self, material=None, nozzle=None, machine=None,
                 track_width=None, track_width_raft =None, track_height=None, track_height_raft=None,
                 temperature_extruder_raft=None, temperature_extruder=None,
                 speed_travel=None, speed_printing=None, speed_printing_raft=None, extrusion_multiplier=None,
                 retraction_distance=None, retraction_restart_distance=None, retraction_speed=None, coasting_distance=None,
                 raft_density=None,
                 temperature_chamber_setpoint:int=None, temperature_printbed_setpoint:int=None,
                 part_cooling_setpoint:int=None, ventilator_entry_setpoint:int=None, ventilator_exit_setpoint:int=None, *args, **kwargs):

        self.speed_travel = speed_travel

        self.material = Material(None, None, None, None, None) # TODO why 1.75
        self.nozzle = nozzle

        self.track_width = track_width
        self.track_width_raft = track_width_raft
        self.track_height = track_height
        self.track_height_raft = track_height_raft

        self.speed_printing = speed_printing
        self.speed_printing_raft = speed_printing/2 if speed_printing_raft is None else speed_printing_raft

        self.temperature_extruder_raft = temperature_extruder_raft
        self.temperature_extruder = temperature_extruder

        self.extrusion_multiplier = 1 if extrusion_multiplier is None else extrusion_multiplier
        self.extrusion_multiplier_raft = self.extrusion_multiplier

        self.retraction_distance = retraction_distance
        self.retraction_restart_distance = retraction_restart_distance
        self.retraction_speed = retraction_speed
        self.coasting_distance = coasting_distance

        self.raft_density = 100 if raft_density is None else raft_density  # (%)
        #
        # self.optimize_temperature_printbed = optimize_temperature_printbed  # True if ones wants to optimize temperature_printbed
        # self.optimize_speed_printing = optimize_speed_printing  # True if ones wants to optimize speed_printing
        # self.optimize_track_height = optimize_track_height  # True if ones wants to optimize track_height

        self.temperature_chamber_setpoint = temperature_chamber_setpoint if temperature_chamber_setpoint else 0
        self.temperature_printbed_setpoint = temperature_printbed_setpoint if temperature_printbed_setpoint else 0

        self.part_cooling_setpoint = part_cooling_setpoint if part_cooling_setpoint else 0
        self.ventilator_entry_setpoint = ventilator_entry_setpoint if ventilator_entry_setpoint else 0
        self.ventilator_exit_setpoint = ventilator_exit_setpoint if ventilator_exit_setpoint else 0


class Parameter(object):
    def __init__(self, name: str=None, units: str=None, precision: str=None, value: float or list=None, default_value: list=None):
        self.name = name
        self.units = units
        self.precision = precision
        self.values = value
        #if value:
        #     if isinstance(value, list):
        #     else:
        #         print(value) if name == "printing speed" else print("hello")
        #         self.value = value
        # else:
        #     self.value = None
        if default_value is not None:
            self.default_value = default_value
            self.min_default = default_value[0]
            self.max_default = default_value[1]


class TestInfo(object):
    def __init__(self, name: str, test_number: str, number_of_layers: int, number_of_test_structures: int, raft: bool, parameter_one: Parameter, parameter_two: Parameter, number_of_substructures: int, other_parameters: list, parameter_three: Parameter=None):
        self.name = name
        self.test_number = test_number
        self.number_of_layers = number_of_layers
        self.number_of_test_structures = number_of_test_structures
        self.number_of_substructures = number_of_substructures
        self.raft = raft
        self.parameter_one = parameter_one
        self.parameter_two = parameter_two
        self.parameter_three = parameter_three
        self.other_parameters = other_parameters


def get_minmax_track_width_coef(size_id: float, number_of_test_structures: int):
    if size_id < 0.6:
        coef_w_min = 0.90
        coef_w_max = 1.10
    if size_id >= 0.6:
        coef_w_min = 0.90
        coef_w_max = 1.20
    if size_id >= 0.8:
        coef_w_min = 1.00
        coef_w_max = 1.30
    if size_id >= 1.0:
        coef_w_min = 0.90
        coef_w_max = 1.40

    coef_w= np.linspace(coef_w_min, coef_w_max, number_of_test_structures).tolist()

    return coef_w


def get_minmax_track_height_coef(size_id: float, number_of_test_structures: int):
    if size_id == 0.1:
        coef_h_min = 0.10
        coef_h_max = 0.50
    else:
        coef_h_min = 1./5.
        coef_h_max = 2./3.

    coef_h = np.linspace(0.90*coef_h_min, 1.10*coef_h_max, number_of_test_structures).tolist()

    return coef_h


def get_minmax_track_height_raft_coef(size_id: float, number_of_test_structures=None):

    if size_id == 0.1:
        coef_h_min_raft = 0.50
        coef_h_max_raft = 0.70
    elif size_id == 0.2:
        coef_h_min_raft = 0.50
        coef_h_max_raft = 0.75
    elif size_id == 0.4:
        coef_h_min_raft = 0.33
        coef_h_max_raft = 0.50
    elif size_id == 0.6:
        coef_h_min_raft = 0.30
        coef_h_max_raft = 0.66
    elif size_id == 0.8:
        coef_h_min_raft = 0.30
        coef_h_max_raft = 0.50
    elif size_id >= 1.0:
        coef_h_min_raft = 0.30
        coef_h_max_raft = 0.75
    else:
        coef_h_min_raft = 1/4
        coef_h_max_raft = 1/2

    coef_h_raft = np.linspace(0.90*coef_h_min_raft, 1.10*coef_h_max_raft, number_of_test_structures).tolist()

    return coef_h_raft


def get_minmax_track_width_raft_coef(size_id: float, number_of_test_structures=None):
    coef_w_max_raft = 1.4
    coef_w_min_raft = 1.0

    if size_id >= 1.0:
        coef_w_min_raft = 1.0
        coef_w_max_raft = 2.0

    coef_w_raft = np.linspace(0.90*coef_w_min_raft, 1.00*coef_w_max_raft, number_of_test_structures).tolist()

    return coef_w_raft


def get_minmax_temperature(temperature_extruder_raft: float, temperature_max: float, number_of_test_structures: int):
    temperature_extruder_min = temperature_extruder_raft
    temperature_extruder_max = min(temperature_max, 1.070 * (temperature_extruder_raft + 273.15) - 273.15)

    temperature_all = np.linspace(temperature_extruder_min,
                                  temperature_extruder_max, number_of_test_structures).tolist()

    return temperature_all


def get_test_structure_size(machine):
    test_structure_size = 60
    if machine.temperaturecontrollers.extruder.nozzle.size_id > 0.29:
        test_structure_size = 70
        if machine.temperaturecontrollers.extruder.nozzle.size_id > 0.39:
            test_structure_size = 80
            if machine.temperaturecontrollers.extruder.nozzle.size_id > 0.59:
                test_structure_size = 90
                if machine.temperaturecontrollers.extruder.nozzle.size_id > 0.99:
                    test_structure_size = 100

    return test_structure_size


def get_flow_rate(height, width, speed_printing, extrusion_multiplier=1):
    if height < width / (2 - math.pi / 2):
        flow_rate = extrusion_multiplier * speed_printing * (height * (width - height) + math.pi * (height / 2) ** 2)
    else:
        flow_rate = extrusion_multiplier * speed_printing * height * width

    return flow_rate


def sum_of_list_elements(my_list, index):
    sum_of_elements = [sum(my_list[0:x + 1]) for x in range(0, index + 1)]

    return sum_of_elements[-1]


def save_session_file_as(session_id: str, extension: str) -> str:
    """
    Takes a save_session_file_as extension and returns a full file-name based on the following convention:
    'cwd\\folder\\YYYYMMDDxxx_TestNumber.extension' where x is a number character from [0-9a-z] and TestNumber is a
    double-digit zero-padded number.
    :param session_id:
    :param extension:
    :return:
    """
    from paths import gcode_folder, json_folder, pdf_folder, stl_folder, png_folder
    from CLI_helpers import separator
    from Globals import persistence

    if not extension.startswith("."):
        extension = "." + extension

    folder = None

    if extension == ".gcode":
        folder = gcode_folder
    elif extension == ".json":
        folder = json_folder
    elif extension == ".pdf":
        folder = pdf_folder
    elif extension == ".stl":
        folder = stl_folder
    elif extension == ".png":
        folder = png_folder

    if extension == ".gcode":
        output = str(folder + separator() + session_id) + "_{}".format(str(persistence["session"]["test_number"])) + extension
    elif extension == ".png":
        output = str(folder + separator() + session_id) + "_{}".format(str(persistence["session"]["test_number"])) + extension
    else:
        output = str(folder + separator() + session_id + extension)

    return output


def border_values(_list: list):
   return [_list[0], _list[-1]]