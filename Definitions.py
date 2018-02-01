# based on gcodeTools
import json
import math
import os

import jsonpickle
import numpy as np

header = r'header'
footer = r'footer'


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

    def __init__(self, name, manufacturer, id = None, size_od: float = None,
                 temperature_melting=None, temperature_destr=None, temperature_glass=None, temperature_vicat=None,
                 mvr=None, mfi=None, temperature_mfr=None, load_mfr=None, capillary_length_mfr=None,
                 capillary_diameter_mfr=None, time_mfr=None, density_rt=None, lcte=None, heat_capacity=None, *args, **kwargs):
        self.name = name
        self.manufacturer = manufacturer
        self.id = id
        self.size_od = size_od
        self.temperature_melting =  temperature_melting
        self.temperature_destr = temperature_destr
        self.temperature_glass = temperature_glass
        self.temperature_vicat = temperature_vicat
        self.mvr = mvr
        self.mfi = mfi
        self.temperature_mfr = 220 if temperature_mfr is None else temperature_mfr
        self.capillary_diameter_mfr = capillary_diameter_mfr  # respect the units: mm
        self.capillary_length_mfr = capillary_length_mfr  # respect the units: mm
        self.time_mfr = 5 if time_mfr is None else time_mfr  # respect the units: min
        self.density_rt = density_rt  # respect the units: g/cm3
        self.lcte = lcte
        self.load_mfr = load_mfr  # respect the units: kg
        self.heat_capacity = heat_capacity  # respect the units: J / K / g

    def print(self):
        print('This is %s filament. Its outer diameter is %.2f mm and its ID is %s' % (
        self.name, self.size_od, self.id))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Nozzle(object):
    """
    definition of the nozzle properties:
    id - nozzle id
    size_id - inner diameter of the nozzle (mm)
    size_od - outer diameter of the nozzle (mm)
    size_capillary_length - length of the capillary in the nozzle (mm)
    size_angle - angle in the nozzle (deg)
    metal - nozzle metal (e.g. brass or steel)
    """

    def __init__(self, size_id, size_od, size_capillary_length, size_angle, metal, *args, **kwargs):

        self.size_id = size_id  # respect the units: mm
        self.size_od = size_od  # respect the units: mm
        self.size_capillary_length = size_capillary_length  # respect the units: mm
        self.size_angle = math.radians(size_angle)  # respect the units: conversion from angles to radians
        self.metal = metal

    def print(self):
        print('This is a %.1f mm %s nozzle.' % (self.size_id, self.metal))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Settings(object):
    """
    definition of the user's settings:
    path_height - height of the path (mm)
    path_width - width of the path (mm)
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

    def __init__(self, material=None, nozzle=None, path_width=None, path_height=None, path_height_raft = None, temperature_extruder_raft=None,
                 temperature_printbed_raft=None, extrusion_multiplier_raft=None, speed_printing_raft=None, temperature_extruder=None,
                 temperature_printbed=None, extrusion_multiplier=None, speed_printing=None, retraction_distance = None, retraction_restart_distance = None,
                 coasting_distance = None, part_cooling=None, raft_density=None, number_of_test_structures = None, optimize_temperature_printbed = None, optimize_speed_printing = None, optimize_path_height = None,                    get_path_width = None, get_path_height = None, perimeter = None, overlap = None, matrix_size = None, *args, **kwargs):
        self.tests = []
        self.machines = []
        self.aesthetics = []  # aim for aesthetics
        self.speed = []  # aim for fast printing
        self.strength = []  # aim for mechanical strength

        self.material = Material(None, None, None, 1.75)
        self.path_width = path_width  # respect the units: mm
        self.path_height = path_height  # respect the units: mm
        self.path_height_raft = path_height_raft
        self.temperature_printbed_raft = temperature_printbed_raft
        self.temperature_extruder_raft = temperature_extruder_raft  # respect the units: degC
        self.extrusion_multiplier_raft = 1.15 if extrusion_multiplier_raft is None else extrusion_multiplier_raft

        self.temperature_extruder = temperature_extruder  # respect the units: degC
        self.temperature_printbed = temperature_printbed  # respect the units: degC
        self.extrusion_multiplier = 1 if extrusion_multiplier is None else extrusion_multiplier # 0...1
        self.speed_printing = speed_printing  # respect the units: mm/s
        self.speed_printing_raft = speed_printing/2 if speed_printing_raft is None else speed_printing_raft  # respect the units: mm/s
        self.retraction_distance = retraction_distance
        self.retraction_restart_distance = retraction_restart_distance
        self.coasting_distance = coasting_distance
        self.part_cooling = 0 if part_cooling is None else part_cooling  # (%)
        self.raft_density = 100 if raft_density is None else raft_density  # (%)
        self.number_of_test_structures = number_of_test_structures  # number_of_test_structures (should be uneven)
        self.optimize_temperature_printbed = optimize_temperature_printbed  # True if ones wants to optimize temperature_printbed
        self.optimize_speed_printing = optimize_speed_printing  # True if ones wants to optimize speed_printing
        self.optimize_path_height = optimize_path_height  # True if ones wants to optimize path_height
        self.get_path_width = get_path_width  # True if ones wants to get path_width values
        self.get_path_height = get_path_height  # True if ones wants to get path_height values
        self.perimeter = perimeter
        self.overlap = overlap
        self.matrix_size = matrix_size


        if material is None:
            self.material_name = None
        else:
            self.material_name = material.name
        self.nozzle = nozzle

    def print(self):
        print(
            'This is a %s material MP Material Test. It consists of %i separate tests, performed with %i machines. The tests are performed with %s.' % (
            self.tests, len(self.tests), len(self.machines), self.material_name))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Machine(object):
    """
    definition of the machine (i.e. 3D printer):
    id - machine ID
    manufacturer - machine's manufacturer
    model - machine's model
    sn - machine's SN
    size_extruder_id - ID of the extruder (mm)
    buildarea_maxdim1 - maximum buildarea in dimension 1 (mm)
    buildarea_maxdim2 - maximum buildarea in dimension 2 (mm)
    temperature_max - maximum heating block temperature (degC)
    moment_max - maximum torque of the motor (N m)
    gear_size_od - gear OD (m)
    heater_power - total heaters power (W)
    """

    def __init__(self, id: str = None, manufacturer: str = None, model: str = None, sn: str = None, size_extruder_id: float = None,
                 buildarea_maxdim1: float = None,
                 buildarea_maxdim2: float = None, temperature_max: float = None, moment_max: float = None, gear_size_od: float = 12,
                 heater_power: float = 80, settings = None, *args, **kwargs):

        self.id = id
        self.manufacturer = manufacturer
        self.model = model
        self.sn = sn
        self.size_extruder_id = size_extruder_id  # respect the units: mm
        self.buildarea_maxdim1 = buildarea_maxdim1  # respect the units: mm
        self.buildarea_maxdim2 = buildarea_maxdim2  # respect the units: mm
        self.temperature_max = temperature_max  # the maximum achievable temperature: degC
        if moment_max is not None: self.moment_max = moment_max  # maximum moment: N m
        if gear_size_od is not None: self.gear_size_od = gear_size_od  # gear radius: m
        if heater_power is not None: self.heater_power = heater_power
        self.nozzle = Nozzle(**kwargs["nozzle"])
        self.settings = None

    def getid(self):
        return self.id

    def print(self):
        print('This is a %s %s machine (SN: %s). The maximum dimensions of the build area are %s mm x %s mm' % (
            self.manufacturer, self.model, self.sn, self.buildarea_maxdim1, self.buildarea_maxdim2))

    def setnozzle(self, size_id: float, size_od: float, size_capillary_length: float, size_angle: float, metal: str):
        self.nozzle = Nozzle(size_id, size_od, size_capillary_length, size_angle, metal)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def minmax_path_width(machine: Machine):
    coef_w_min = 0.90

    if machine.nozzle.size_id <= 0.6:
        coef_w_max = 1
    else:
        coef_w_max = machine.nozzle.size_od / machine.nozzle.size_id

    coef_w_all = np.linspace(coef_w_min, coef_w_max, machine.settings.number_of_test_structures)
    coef_w_mean = (coef_w_min + coef_w_max) / 2

    return coef_w_all, coef_w_mean


def minmax_path_height(machine: Machine, number_of_test_structures):
    if machine.nozzle.size_id == 0.1:
        coef_h_min = 0.10
        coef_h_max = 0.50
    else:
        coef_h_min = 1 / 5
        coef_h_max = 2 / 3

    coef_h_all = np.linspace(0.9*coef_h_min, 1.1*coef_h_max, number_of_test_structures).tolist()
    coef_h_mean = (coef_h_min + coef_h_max)/2

    return coef_h_all, coef_h_mean


def minmax_path_width_height_raft(machine: Machine):
    coef_w_max_raft = machine.nozzle.size_od/machine.nozzle.size_id
    coef_w_min_raft = 1.0

    if machine.nozzle.size_id == 0.1:
        coef_h_min_raft = 0.50
        coef_h_max_raft = 0.70
    elif machine.nozzle.size_id == 0.2:
        coef_h_min_raft = 0.50
        coef_h_max_raft = 0.75
    elif machine.nozzle.size_id == 0.4:
        coef_h_min_raft = 0.33
        coef_h_max_raft = 0.50
    elif machine.nozzle.size_id == 0.6:
        coef_h_min_raft = 0.30
        coef_h_max_raft = 0.66
    elif machine.nozzle.size_id == 0.8:
        coef_h_min_raft = 0.416
        coef_h_max_raft = 0.500 #  h_raft = 0.42 mm Original value of 0.5 doesn't work for FPU77D at 245 degC
    elif machine.nozzle.size_id == 1.0:
        coef_h_min_raft = 0.30
        coef_h_max_raft = 0.50
    elif machine.nozzle.size_id == 1.2:
        coef_h_min_raft = 0.30
        coef_h_max_raft = 0.50
    elif machine.nozzle.size_id == 1.4:
        coef_h_min_raft = 0.28
        coef_h_max_raft = 0.50
    else:
        coef_h_min_raft = 1 / 4
        coef_h_max_raft = 1 / 2

    coef_h_raft = (coef_h_min_raft + coef_h_max_raft)/2
    coef_w_raft = (coef_w_min_raft + coef_w_max_raft)/2

    coef_h_raft_all = np.linspace(0.9*coef_h_min_raft, 1.1*coef_h_max_raft, machine.settings.number_of_test_structures).tolist()

    return coef_h_raft, coef_h_min_raft, coef_h_max_raft, coef_w_raft, coef_h_raft_all


def minmax_temperature(material: Material, machine: Machine):
    temperature_all = None
    temperature_extruder_min = 0.975 * (machine.settings.temperature_extruder + 273.15) - 273.15
    temperature_extruder_max = 1.060 * (machine.settings.temperature_extruder + 273.15) - 273.15

    if material.temperature_destr < machine.temperature_max:
        if temperature_extruder_max < material.temperature_destr:
            temperature_all = np.linspace(temperature_extruder_min,
                                          temperature_extruder_max, machine.settings.number_of_test_structures).tolist()
        else:
            temperature_all = np.linspace(temperature_extruder_min,
                                          0.975 * (material.temperature_destr + 273.15) - 273.15, machine.settings.number_of_test_structures).tolist()
    elif material.temperature_destr >= machine.temperature_max:
        if temperature_extruder_max < machine.temperature_max:
            temperature_all = np.linspace(temperature_extruder_min,
                                          0.975 * (temperature_extruder_max + 273.15) - 273.15, machine.settings.number_of_test_structures).tolist()
        elif temperature_extruder_max >= machine.temperature_max:
            temperature_all = np.linspace(temperature_extruder_min,
                                          temperature_extruder_max, machine.settings.number_of_test_structures).tolist()
    else:
        pass

    return temperature_all


def minmax_speed_printing(machine: Machine):

    speed_printing_all = np.linspace(0.25 * machine.settings.speed_printing,
                                     1.50 * machine.settings.speed_printing,
                                     machine.settings.number_of_test_structures).tolist()

    return speed_printing_all


def minmax_extrusion_multiplier(machine: Machine):
    extrusion_multiplier_all = np.linspace(0.75 * machine.settings.extrusion_multiplier,
                                           1.50 * machine.settings.extrusion_multiplier,
                                           machine.settings.number_of_test_structures).tolist()

    return extrusion_multiplier_all


def get_test_structure_size(machine):
    if machine.nozzle.size_id > 0.4:
        test_structure_size = 100
    if 0.2<machine.nozzle.size_id <=0.4:
        test_structure_size = 75
    elif machine.nozzle.size_id <= 0.2:
        test_structure_size = 55

    return test_structure_size


def json_to_obj(path):
    # Creates a new object (Obj) instance with json dictionary (path) as attributes
    with open(path) as file:
        return jsonpickle.decode(file.read())


def file_check(file):
    # checks whether or not a file exists, returns boolean
    return os.path.isfile(file)


def write_json(name, surname, object, path = None):
    # Encodes a Python object to a pickled JSON. Takes two parameters (name, surname) as file naming arguments
    file_name = str('%s %s.json' % (name, surname))
    if path is None:
        with open(file_name, mode='w') as file:
            file.write(jsonpickle.encode(object))
    else:
        with open(str(path + '/' + file_name), mode='w') as file:
            file.write(jsonpickle.encode(object))