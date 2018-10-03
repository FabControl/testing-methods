from CLI_helpers import separator
import json
import jsonpickle
import math
import numpy as np
import os
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
        self.price_eur_per_kg = price_eur_per_kg
        self.drying = None


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


class Printbed(object):
    """
    printbed_heatable
    """
    def __init__(self, printbed_heatable: bool, temperature_printbed_max: float, temperature_printbed_min: float, *args, **kwargs):
        self.printbed_heatable = printbed_heatable
        self.temperature_printbed_max = temperature_printbed_max
        self.temperature_printbed_min = temperature_printbed_min


class Ventilators(object):
    """
    ventilator_part_cooling
    ventilator_entry
    ventilator_exit
    """

    def __init__(self, ventilator_part_cooling: bool, ventilator_entry: bool, ventilator_exit: bool, *args, **kwargs):
        self.part_cooling = ventilator_part_cooling
        self.entry = ventilator_entry
        self.exit = ventilator_exit


class Software(object):
    """
    version
    """

    def __init__(self, version: str, *args, **kwargs):
        self.version = version


class Firmware(object):
    """
    fw_type
    version
    """

    def __init__(self, fw_type: str, version: str, *args, **kwargs):
        self.fw_type = fw_type
        self.version = version


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

    def __init__(self, aim=None, material=None, nozzle=None, speed_travel = None, track_width=None, track_width_raft =None, track_height=None, track_height_raft=None, temperature_extruder_raft=None,
                 speed_printing_raft=None, temperature_extruder=None, temperature_printbed=None, extrusion_multiplier=None,
                 speed_printing=None, retraction_distance=None, retraction_restart_distance=None, retraction_speed=None, coasting_distance=None,
                 ventilator_part_cooling=None, ventilator_entry=None, ventilator_exit=None, raft_density=None,
                 optimize_temperature_printbed=None, optimize_speed_printing=None, optimize_track_height=None, get_track_width=None, get_track_height=None,
                 perimeter=None, overlap=None, matrix_size=None, layers=None, *args, **kwargs):

        self.aim = aim

        self.speed_travel = speed_travel

        self.material = Material(None, None, None, None, None) # TODO why 1.75
        self.track_width = track_width
        self.track_width_raft = track_width_raft
        self.track_height = track_height
        self.track_height_raft = track_height_raft
        self.speed_printing = speed_printing
        self.speed_printing_raft = speed_printing/2 if speed_printing_raft is None else speed_printing_raft

        self.temperature_extruder_raft = temperature_extruder_raft
        self.temperature_printbed = temperature_printbed

        self.temperature_extruder = temperature_extruder
        self.extrusion_multiplier = 1 if extrusion_multiplier is None else extrusion_multiplier

        self.extrusion_multiplier_raft = self.extrusion_multiplier

        self.retraction_distance = retraction_distance
        self.retraction_restart_distance = retraction_restart_distance
        self.retraction_speed = retraction_speed
        self.coasting_distance = coasting_distance

        self.ventilator_part_cooling = ventilator_part_cooling  # (%)
        self.ventilator_entry = ventilator_entry  # (%)
        self.ventilator_exit = ventilator_exit # (%)

        self.raft_density = 100 if raft_density is None else raft_density  # (%)
        self.optimize_temperature_printbed = optimize_temperature_printbed  # True if ones wants to optimize temperature_printbed
        self.optimize_speed_printing = optimize_speed_printing  # True if ones wants to optimize speed_printing
        self.optimize_track_height = optimize_track_height  # True if ones wants to optimize track_height
        self.get_track_width = get_track_width  # True if ones wants to get track_width values
        self.get_track_height = get_track_height  # True if ones wants to get track_height values
        #self.material_name = None if material is None else material.name
        self.nozzle = nozzle


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
    temperature_extruder_max - maximum heating block temperature (degC)
    moment_max - maximum torque of the motor (N m)
    gear_size_od - gear OD (m)
    heater_power - total heaters power (W)
    """

    def __init__(self, id: str=None, manufacturer: str=None, model: str=None, sn: str=None, form: str=None, buildarea_maxdim1: float=None, buildarea_maxdim2: float=None, temperature_extruder_max: float=None, temperature_extruder_min: float=None,
                 temperature_printbed_max: float = None, temperature_printbed_min: float = None, moment_max: float=None, gear_size_od: float=12, heater_power: float=80, *args, **kwargs):

        self.id = id
        self.manufacturer = manufacturer
        self.model = model
        self.sn = sn
        self.form = form
        self.buildarea_maxdim1 = buildarea_maxdim1  # respect the units: mm
        self.buildarea_maxdim2 = buildarea_maxdim2  # respect the units: mm
        self.temperature_extruder_max = temperature_extruder_max  # the maximum achievable temperature: degC
        self.temperature_extruder_min = temperature_extruder_min  # the minimum achievable temperature: degC
        self.temperature_printbed_max = temperature_printbed_max  # the maximum achievable temperature: degC
        self.temperature_printbed_min = temperature_printbed_min  # the minimum achievable temperature: degC

        if moment_max is not None: self.moment_max = moment_max  # maximum moment: N m
        if gear_size_od is not None: self.gear_size_od = gear_size_od  # gear radius: m
        if heater_power is not None: self.heater_power = heater_power

        self.nozzle = Nozzle(**kwargs["nozzle"])
        self.ventilators = Ventilators(**kwargs["ventilators"])
        self.software = Software(**kwargs["software"])
        self.firmware = Firmware(**kwargs["firmware"])
        self.printbed = Printbed(**kwargs["printbed"])
        #self.settings = None


class TestInfo(object):
    def __init__(self, name: str, parameter: str, units: str, precision: str, number_of_layers: int, number_of_test_structures: int, raft: bool=True, number_of_substructures: int=None, default_value: list=None):
        self.name = name
        self.parameter = parameter
        self.units = units
        self.precision = precision
        self.number_of_layers = number_of_layers
        self.number_of_test_structures = number_of_test_structures
        self.number_of_substructures = number_of_substructures
        self.raft = raft

        if default_value is not None:
            self.min_default = default_value[0]
            self.max_default = default_value[1]


def minmax_track_width(machine: Machine, number_of_test_structures: int):
    if machine.nozzle.size_id <= 0.6:
        coef_w_min = 0.90
        coef_w_max = 1
    if machine.nozzle.size_id > 0.6:
        coef_w_min = 0.90
        coef_w_max = machine.nozzle.size_od / machine.nozzle.size_id
    if machine.nozzle.size_id >= 0.8:
        coef_w_min = 1.0
        coef_w_max = 1.15 * machine.nozzle.size_od / machine.nozzle.size_id
    if machine.nozzle.size_id >= 1.0:
        coef_w_min = 0.9
        coef_w_max = 1.3 * machine.nozzle.size_od / machine.nozzle.size_id

    coef_w_all = np.linspace(coef_w_min, coef_w_max, number_of_test_structures)
    coef_w_mean = (coef_w_min + coef_w_max) / 2

    return coef_w_all, coef_w_mean


def minmax_track_height(machine: Machine, number_of_test_structures: int):
    if machine.nozzle.size_id == 0.1:
        coef_h_min = 0.10
        coef_h_max = 0.50
    else:
        coef_h_min = 1./5.
        coef_h_max = 2./3.

    coef_h_all = np.linspace(0.9*coef_h_min, 1.1*coef_h_max, number_of_test_structures).tolist()

    return coef_h_all


def minmax_track_width_height_raft(machine: Machine, number_of_test_structures=None):
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
        coef_h_min_raft = 0.30
        coef_h_max_raft = 0.50
    elif machine.nozzle.size_id >= 1.0:
        coef_w_min_raft = 1.0
        coef_w_max_raft = 2.0
        coef_h_min_raft = 0.30
        coef_h_max_raft = 0.75
    else:
        coef_h_min_raft = 1 / 4
        coef_h_max_raft = 1 / 2

    coef_h_raft = (coef_h_min_raft + coef_h_max_raft)/2
    coef_w_raft = (coef_w_min_raft + coef_w_max_raft)/2

    if number_of_test_structures is not None:
        coef_h_raft_all = np.linspace(0.9*coef_h_min_raft, 1.1*coef_h_max_raft, number_of_test_structures).tolist()
        coef_w_raft_all = np.linspace(0.95*coef_w_min_raft, 1.15*coef_w_max_raft, number_of_test_structures).tolist()
        return coef_h_raft, coef_w_raft, coef_h_raft_all, coef_w_raft_all
    else:
        return coef_h_raft, coef_w_raft


def minmax_temperature(material: Material, machine: Machine, number_of_test_structures: int):
    temperature_all = None

    temperature_extruder_min = machine.settings.temperature_extruder_raft

    temperature_extruder_max = 1.060 * (machine.settings.temperature_extruder + 273.15) - 273.15

    if material.temperature_destr < machine.temperature_extruder_max:
        if temperature_extruder_max < material.temperature_destr:
            temperature_all = np.linspace(temperature_extruder_min,
                                          temperature_extruder_max, number_of_test_structures).tolist()
        else:
            temperature_all = np.linspace(temperature_extruder_min,
                                          0.975 * (material.temperature_destr + 273.15) - 273.15, number_of_test_structures).tolist()
    elif material.temperature_destr >= machine.temperature_extruder_max:
        if temperature_extruder_max < machine.temperature_extruder_max:
            temperature_all = np.linspace(temperature_extruder_min,
                                          0.975 * (temperature_extruder_max + 273.15) - 273.15, number_of_test_structures).tolist()
        elif temperature_extruder_max >= machine.temperature_extruder_max:
            temperature_all = np.linspace(temperature_extruder_min,
                                          temperature_extruder_max, number_of_test_structures).tolist()
    else:
        pass

    return temperature_all


def get_test_structure_size(machine):
    test_structure_size = 55
    if machine.nozzle.size_id > 0.29:
        test_structure_size = 75
        if machine.nozzle.size_id > 0.39:
            test_structure_size = 100
            if machine.nozzle.size_id > 0.59:
                test_structure_size = 125
                if machine.nozzle.size_id > 0.99:
                    test_structure_size = 150

    return test_structure_size


def flow_rate(height, width, speed_printing, extrusion_multiplier=1):
    if height < width / (2 - math.pi / 2):
        flow_rate = extrusion_multiplier * speed_printing * (height * (width - height) + math.pi * (height / 2) ** 2)
    else:
        flow_rate = extrusion_multiplier * speed_printing * height * width
    return flow_rate


def sum_of_list_elements(my_list, index):
    sum_of_elements = [sum(my_list[0:x + 1]) for x in range(0, index + 1)]
    return sum_of_elements[-1]
