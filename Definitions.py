from CLI_helpers import separator
import json
import jsonpickle
import math
import numpy as np
from paths import header

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
    def __init__(self,
                 dried: bool, *args, **kwargs):
        self.dried = dried


class Material(object):
    """
    definition of the filament properties:
    name                        - filament name
    size_od                     - outer diameter
    manufacturer                - manufacturer's/supplier's name
    id                          - material ID
    temperature_destr           - destruction temperature in air (degC)
    temperature_glass           - glass transition temperature (degC)
    temperature_vicat           - Vicat softening point (degC)
    mvr                         - melt flow rate (cm3)
    mfi                         - melt flow index (g)
    temperature_mfr             - temperature at which MFR has been determined (degC)
    load_mfr                    - load under which the MFR has been determined (kg)
    capillary_length_mfr        - capillary length in the MFR measurement device (mm)
    capillary_diameter_mfr      - capillary diameter in the MFR measurement device (mm)
    time_mfr                    - extrusion time in the MFR experiment (min)
    density_rt                  - density at RT (g/cc)
    lcte                        - linear coefficient of thermal expansion (1/K)
    heat_capacity               - specific heat capacity (J/kg/K)
    """

    def __init__(self,
                 name: str,
                 size_od: float=None, *args, **kwargs):
        self.name = name
        self.size_od = size_od


class Chamber(object):
    """
    chamber_heatable
    tool
    gcode_command
    gcode_command_immediate
    temperature_min
    ventilator_exit
    ventilator_entry
    ventilator_exit_tool
    ventilator_exit_gcode_command
    ventilator_entry_tool
    ventilator_entry_gcode_command
    """
    def __init__(self,
                 chamber_heatable: bool,
                 tool: str=None,
                 gcode_command: str="M141 S$temp",
                 gcode_command_immediate: str=None,
                 temperature_max: float=None, *args, **kwargs):
        self.chamber_heatable = chamber_heatable
        if chamber_heatable:
            self.tool = tool # tool number, e.g. T1, T2
            self.gcode_command = gcode_command # G-code command used to control the temperature of the chamber, e.g. Mddd {0} S{1}, where {0} is a tool string
            self.gcode_command_immediate = gcode_command_immediate # G-code command used to control the temperature of the chamber, e.g. Mddd {0} S{1}, where {0} is a tool string
            self.temperature_max = temperature_max


class Printbed(object):
    """

    """
    def __init__(self,
                 printbed_heatable: bool,
                 gcode_command: str = "M190 S$temp",
                 gcode_command_immediate: str = "M140 S$temp",
                 temperature_max: float = None, *args, **kwargs):

        self.printbed_heatable = printbed_heatable
        if printbed_heatable:
            self.temperature_max = temperature_max
            self.gcode_command = gcode_command  # G-code command used to control the temperature of the print bed, e.g. Mddd S$temp ($tool)
            self.gcode_command_immediate = gcode_command_immediate  # G-code command used to control the temperature of the print bed, e.g. Mddd S$temp ($tool)


class Nozzle(object):
    """
    definition of the nozzle properties:
    size_id - inner diameter of the nozzle (mm)
    size_od - outer diameter of the nozzle (mm)
    size_capillary_length - length of the capillary in the nozzle (mm)
    size_angle - angle in the nozzle (deg)
    size_extruder_id - inner diameter of the extruder (mm)
    type - nozzle metal (e.g. brass or steel)
    """
    def __init__(self,
                 size_id: float, *args, **kwargs):

        self.size_id = size_id  # respect the units: mm


class Extruder(object):
    """
    tool - tool number, e.g. T1, T2
    gcode_command - G-code command to set the temperature and wait till it has been reached, e.g. M109 S$temp $tool, where tool is a tool string
    gcode_command_immediate - G-code command to set the temperature immediately, e.g. M104 S$temp $tool, where tool is a tool string
    """
    def __init__(self,
                 temperature_max: int,
                 part_cooling: bool,
                 tool: str = "T0",
                 gcode_command: str = "M109 S$temp $tool",
                 gcode_command_immediate: str = "M104 S$temp $tool",
                 part_cooling_gcode_command: str = "M106 S$cool", *args, **kwargs):

        self.tool = tool
        self.gcode_command = gcode_command
        self.gcode_command_immediate = gcode_command_immediate
        self.temperature_max = temperature_max
        self.part_cooling = part_cooling
        if part_cooling:
            self.part_cooling_gcode_command = part_cooling_gcode_command
        self.nozzle = Nozzle(**kwargs["nozzle"])


class TemperatureControllers(object):
    """
    all temperature controllers
    """
    def __init__(self, *args, **kwargs):
        self.extruder = Extruder(**kwargs["extruder"])
        self.chamber = Chamber(**kwargs["chamber"])
        self.printbed = Printbed(**kwargs["printbed"])


class Machine(object):
    """
    definition of the machine (i.e. 3D printer):
    sn - machine's SN
    form - form factor
    buildarea_maxdim1 - maximum buildarea in dimension 1 (mm)
    buildarea_maxdim2 - maximum buildarea in dimension 2 (mm)
    id - machine ID
    manufacturer - machine's manufacturer
    model - machine's model
    """

    def __init__(self,
                 sn: str = None,
                 model: str = None,
                 form: str = "",
                 buildarea_maxdim1: float = None,
                 buildarea_maxdim2: float = None,
                 *args, **kwargs):

        self.sn = sn
        self.model = model
        self.form = form
        self.buildarea_maxdim1 = buildarea_maxdim1  # respect the units: mm
        self.buildarea_maxdim2 = buildarea_maxdim2  # respect the units: mm
        self.temperaturecontrollers = TemperatureControllers(**kwargs["temperature_controllers"])


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
                 track_width=None, track_width_raft =None,
                 track_height=None, track_height_raft=None,
                 temperature_extruder_raft=None, temperature_extruder=None,
                 speed_travel=None, speed_printing=None, speed_printing_raft=None,
                 extrusion_multiplier=None,
                 retraction_distance=None, retraction_restart_distance=None, retraction_speed=None, coasting_distance=None,
                 bridging_extrusion_multiplier=None, bridging_part_cooling=None, bridging_speed_printing=None,
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

        self.bridging_extrusion_multiplier = bridging_extrusion_multiplier
        self.bridging_part_cooling = bridging_part_cooling
        self.bridging_speed_printing = bridging_speed_printing

        self.raft_density = 100 if raft_density is None else raft_density  # (%)

        self.temperature_chamber_setpoint = temperature_chamber_setpoint if temperature_chamber_setpoint else 0
        self.temperature_printbed_setpoint = temperature_printbed_setpoint if temperature_printbed_setpoint else 0

        self.part_cooling_setpoint = part_cooling_setpoint if part_cooling_setpoint else 0
        self.ventilator_entry_setpoint = ventilator_entry_setpoint if ventilator_entry_setpoint else 0
        self.ventilator_exit_setpoint = ventilator_exit_setpoint if ventilator_exit_setpoint else 0


class Parameter(object):
    def __init__(self, name: str=None, programmatic_name: str=None, units: str=None, precision: str=None, value: float or list=None, active: bool=True, min_max: list=None, default_value: list=None, hint_active: str=None):
        self.name = name
        self.programmatic_name = programmatic_name
        self.units = units
        self.precision = precision
        self.values = value
        self.active = active
        self.min_max = min_max
        self.hint_active = hint_active

        if default_value is not None:
            self.default_value = default_value
            self.min_default = default_value[0]
            self.max_default = default_value[1]

    def dict(self):
        return {
            "name": self.name,
            "programmatic_name": self.programmatic_name,
            "units": self.units,
            "precision": self.precision,
            "values": self.values,
            "active": self.active,
            "min_max": self.min_max,
            "hint_active": self.hint_active
        }


class TestInfo(object):
    def __init__(self, name: str, test_number: str, number_of_layers: int, number_of_test_structures: int, raft: bool, parameter_one: Parameter, parameter_two: Parameter, number_of_substructures: int, other_parameters: list,
                 hint_init: str, hint_valid: str="Inspect the printed test structure. Select one combination of parameters which results in the best test structure.",
                 parameter_three: Parameter=None):
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
        self.hint_init = hint_init
        self.hint_valid = hint_valid

    def dict(self):
        return {
            "name": self.name,
            "test_number": self.test_number,
            "number_of_layers": self.number_of_layers,
            "number_of_test_structures": self.number_of_test_structures,
            "number_of_substructures": self.number_of_substructures,
            "raft": self.raft,
            "parameter_one": self.parameter_one.dict(),
            "parameter_two": self.parameter_two.dict(),
            "parameter_three": self.parameter_three.dict() if self.parameter_three is not None else None,
            "other_parameters": [param.dict() for param in self.other_parameters],
            "hint_init": self.hint_init,
            "hint_valid": self.hint_valid,
        }


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
    test_structure_size = 50
    if machine.temperaturecontrollers.extruder.nozzle.size_id > 0.29:
        test_structure_size = 60
        if machine.temperaturecontrollers.extruder.nozzle.size_id > 0.39:
            test_structure_size = 80
            if machine.temperaturecontrollers.extruder.nozzle.size_id > 0.59:
                test_structure_size = 120
                if machine.temperaturecontrollers.extruder.nozzle.size_id > 0.99:
                    test_structure_size = 140

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


def save_session_file_as(persistence: dict, session_id: str, extension: str) -> str:
    """
    Takes a save_session_file_as extension and returns a full file-name based on the following convention:
    'cwd\\folder\\YYYYMMDDxxx_TestNumber.extension' where x is a number character from [0-9a-z] and TestNumber is a
    double-digit zero-padded number.
    :param persistence:
    :param session_id:
    :param extension:
    :return:
    """
    from paths import gcode_folder, json_folder, pdf_folder, stl_folder, png_folder
    from CLI_helpers import separator

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