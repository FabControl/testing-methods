from Definitions import *
import numpy as np

number_of_substructures=4
number_of_test_structures=7


def parameter_reorder_and_activate(parameters: list, actives: list = None, inactives: list = None):
    """
    A helper function for parameter lists used below to cycle through them and either activate or deactivate some of
    them and then reorder them so that the inactive ones would be in the bottom.
    :param parameters:
    :param actives:
    :param inactives:
    :return:
    """
    inactives_list = []
    actives_list = []
    if inactives is not None and actives is None:
        # Cycle through inactives
        for parameter in parameters:
            if parameter.programmatic_name in inactives:
                parameter.active = False
                inactives_list.append(parameter)
            else:
                parameter.active = True
                actives_list.append(parameter)
    elif actives is not None and inactives is None:
        # Cycle through actives
        for parameter in parameters:
            if parameter.programmatic_name in actives:
                parameter.active = True
                actives_list.append(parameter)
            else:
                parameter.active = False
                inactives_list.append(parameter)
    else:
        raise ValueError("Either actives or inactives must be None")
    output_list = actives_list + inactives_list
    return output_list


def get_speed(min_max):
    if min_max == [] or min_max is None:
        return [0, 0]
    else:
        return [min_max[0], min_max[1]]



def get_test_info(persistence):
    nozzle_size_id = persistence["machine"]["temperature_controllers"]["extruder"]["nozzle"]["size_id"]

    other_parameters = []
    if persistence["machine"]["temperature_controllers"]["chamber"]["chamber_heatable"]:
        other_parameters.append(Parameter("chamber temperature", "temperature_chamber_setpoint", "degC", value=persistence["settings"]["temperature_chamber_setpoint"] if "temperature_chamber_setpoint" in persistence["settings"] else None, min_max=[30, persistence["machine"]["temperature_controllers"]["chamber"]["temperature_max"]]))
    if persistence["machine"]["temperature_controllers"]["printbed"]["printbed_heatable"]:
        other_parameters.append(Parameter("print bed temperature", "temperature_printbed_setpoint", "degC", value=persistence["settings"]["temperature_printbed_setpoint"] if "temperature_printbed_setpoint" in persistence["settings"] else None, min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]))
        #other_parameters.append(Parameter("print bed coating", "", "{}", value=persistence["machine"]["temperature_controllers"]["printbed"]["coating"]))
    try:
        if persistence["machine"]["temperature_controllers"]["chamber"]["ventilator_exit"]:
            other_parameters.append(Parameter("exit ventilation power", "ventilator_exit_setpoint", "%", value=persistence["settings"]["ventilator_exit_setpoint"] if "ventilator_exit_setpoint" in persistence["settings"] else None))
    except:
        pass


    if persistence["machine"]["temperature_controllers"]["extruder"]["part_cooling"]:
        other_parameters.append(Parameter("part cooling", "part_cooling_setpoint", "%", value=persistence["settings"]["part_cooling_setpoint"], min_max=[0,100]))

    other_parameters.extend([Parameter("first-layer extrusion temperature", "temperature_extruder_raft", "degC", value=persistence["settings"]["temperature_extruder_raft"], min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]),
                             Parameter("first-layer track width", "track_width_raft", "mm", value=persistence["settings"]["track_width_raft"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id])])

    if persistence["session"]["min_max_parameter_one"] != []:
        values_parameter_one = np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1],number_of_test_structures).tolist()
    else:
        values_parameter_one = []

    if persistence["session"]["test_number"] == "01":
        other_parameters = parameter_reorder_and_activate(other_parameters, inactives=["part_cooling_setpoint"])
        parameter_values_for_comments = TestInfo("first-layer track height vs first-layer printing speed", "01", number_of_layers=1, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=False,
                                                 parameter_one=Parameter("first-layer track height","track_height_raft", "mm", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id*_ for _ in get_minmax_track_height_raft_coef(nozzle_size_id, number_of_test_structures)], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                                 parameter_two=Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", "{:.1f}",
                                                                         value=np.linspace(*get_speed(persistence["session"]["min_max_parameter_two"]),number_of_substructures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "02":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "track_height_raft", "mm", value=persistence["settings"]["track_height_raft"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", value=persistence["settings"]["speed_printing_raft"], min_max=[1, persistence["settings"]["speed_travel"]])])
        other_parameters = parameter_reorder_and_activate(other_parameters, inactives=["part_cooling_setpoint"])

        parameter_values_for_comments = TestInfo("first-layer track width", "02", number_of_layers=1, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=False,
                                                 parameter_one=Parameter("first-layer track width", "track_width_raft", "mm", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id*_ for _ in get_minmax_track_width_raft_coef(nozzle_size_id, number_of_test_structures)], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                                 parameter_two=Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", "{:.1f}",
                                                                         value=[persistence["settings"]["speed_printing_raft"]], min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "03":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "track_height_raft", "mm", value=persistence["settings"]["track_height_raft"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("first-layer track width", "track_width_raft", "mm", value=persistence["settings"]["track_width_raft"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", value=persistence["settings"]["speed_printing_raft"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("extrusion multiplier", "extrusion_multiplier", "-", value=persistence["settings"]["extrusion_multiplier"], min_max=[0.01, 2]),
                                 Parameter("track height", "track_height", "mm", value=persistence["settings"]["track_height"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("track width", "track_width", "mm", value=persistence["settings"]["track_width"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id])])
        other_parameters = parameter_reorder_and_activate(other_parameters, actives=["part_cooling_setpoint",
                                                                                     "track_height"])
        parameter_values_for_comments = TestInfo("extrusion temperature vs printing speed", "03", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("extrusion temperature", "temperature_extruder", "degC", "{:.0f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else get_minmax_temperature(persistence["settings"]["temperature_extruder_raft"], persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"], number_of_test_structures), min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s","{:.1f}",
                                                                         value=np.linspace(*get_speed(persistence["session"]["min_max_parameter_two"]),number_of_substructures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "04":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "track_height_raft", "mm", value=persistence["settings"]["track_height_raft"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("first-layer track width", "track_width_raft", "mm", value=persistence["settings"]["track_width_raft"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", value=persistence["settings"]["speed_printing_raft"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("extrusion multiplier", "extrusion_multiplier", "-", value=persistence["settings"]["extrusion_multiplier"], min_max=[0.01, 2]),
                                 Parameter("extrusion temperature", "temperature_extruder", "degC", value=persistence["settings"]["temperature_extruder"], min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]),
                                 Parameter("track width", "track_width", "mm", value=persistence["settings"]["track_width"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id])])

        parameter_values_for_comments = TestInfo("track height vs printing speed", "04", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("track height", "track_height", "mm", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id*_ for _ in get_minmax_track_height_coef(nozzle_size_id, number_of_test_structures)], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s", "{:.1f}",
                                                                         value=np.linspace(*get_speed(persistence["session"]["min_max_parameter_two"]),number_of_substructures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "05":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "track_height_raft", "mm", value=persistence["settings"]["track_height_raft"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("first-layer track width", "track_width_raft", "mm", value=persistence["settings"]["track_width_raft"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", value=persistence["settings"]["speed_printing_raft"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("extrusion multiplier", "extrusion_multiplier", "-", value=persistence["settings"]["extrusion_multiplier"], min_max=[0.01, 2]),
                                 Parameter("extrusion temperature", "temperature_extruder", "degC", value=persistence["settings"]["temperature_extruder"], min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]),
                                 Parameter("track height", "track_height", "mm", value=persistence["settings"]["track_height"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("printing speed", "speed_printing", "mm/s", value=persistence["settings"]["speed_printing"], min_max=[1, persistence["settings"]["speed_travel"]])])

        parameter_values_for_comments = TestInfo("track width", "05", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("track width", "track_width", "mm", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id * _ for _ in get_minmax_track_width_coef(nozzle_size_id, number_of_test_structures)], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s", "{:.1f}",
                                                                         value=[persistence["settings"]["speed_printing"]], min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "06":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "track_height_raft", "mm", value=persistence["settings"]["track_height_raft"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("first-layer track width", "track_width_raft", "mm", value=persistence["settings"]["track_width_raft"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", value=persistence["settings"]["speed_printing_raft"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("extrusion temperature", "temperature_extruder", "degC", value=persistence["settings"]["temperature_extruder"], min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]),
                                 Parameter("track height", "track_height", "mm", value=persistence["settings"]["track_height"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("track width", "track_width", "mm", value=persistence["settings"]["track_width"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id])])

        parameter_values_for_comments = TestInfo("extrusion multiplier vs printing speed", "06", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("extrusion multiplier", "extrusion_multiplier", "-", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.80, 1.4, number_of_test_structures).tolist(), min_max=[0.01, 2.2]),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s","{:.1f}",
                                                                         value=[persistence["settings"]["speed_printing"]], min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "07":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "track_height_raft", "mm", value=persistence["settings"]["track_height_raft"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("first-layer track width", "track_width_raft", "mm", value=persistence["settings"]["track_width_raft"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", value=persistence["settings"]["speed_printing_raft"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("extrusion multiplier", "extrusion_multiplier", "-", value=persistence["settings"]["extrusion_multiplier"], min_max=[0.01, 2]),
                                 Parameter("extrusion temperature", "temperature_extruder", "degC", value=persistence["settings"]["temperature_extruder"], min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]),
                                 Parameter("track height", "track_height", "mm", value=persistence["settings"]["track_height"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("track width", "track_width", "mm", value=persistence["settings"]["track_width"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id])])

        parameter_values_for_comments = TestInfo("printing speed", "07", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("printing speed", "speed_printing", "mm/s", "{:.1f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.80*persistence["settings"]["speed_printing"], 1.75*persistence["settings"]["speed_printing"],number_of_test_structures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 parameter_two=Parameter(None, None, None, value=[]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "08":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "track_height_raft", "mm", value=persistence["settings"]["track_height_raft"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("first-layer track width", "track_width_raft", "mm", value=persistence["settings"]["track_width_raft"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", value=persistence["settings"]["speed_printing_raft"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("track height", "track_height", "mm", value=persistence["settings"]["track_height"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("track width", "track_width", "mm", value=persistence["settings"]["track_width"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("extrusion multiplier", "extrusion_multiplier", "-", value=persistence["settings"]["extrusion_multiplier"], min_max=[0.01, 2]),
                                 Parameter("printing speed", "speed_printing", "mm/s", value=persistence["settings"]["speed_printing"], min_max=[1, persistence["settings"]["speed_travel"]])])

        parameter_values_for_comments = TestInfo("extrusion temperature vs retraction distance", "08", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("extrusion temperature", "temperature_extruder", "degC", "{:.0f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(persistence["settings"]["temperature_extruder"]-5, persistence["settings"]["temperature_extruder"]+5, number_of_test_structures).tolist(), min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]),
                                                 parameter_two=Parameter("retraction distance", "retraction_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.0, 4.0, number_of_substructures).tolist(), min_max=[0, 20]),
                                                 parameter_three=Parameter("retraction speed", "retraction_speed", "mm/s", "{:.1f}",
                                                                         value=persistence["session"]["min_max_parameter_three"] if persistence["session"]["min_max_parameter_three"] != [] else [60, 120], min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "09":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "track_height_raft", "mm", value=persistence["settings"]["track_height_raft"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("first-layer track width", "track_width_raft", "mm", value=persistence["settings"]["track_width_raft"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", value=persistence["settings"]["speed_printing_raft"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("track height", "track_height", "mm", value=persistence["settings"]["track_height"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("track width", "track_width", "mm", value=persistence["settings"]["track_width"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("extrusion temperature", "temperature_extruder", "degC", value=persistence["settings"]["temperature_extruder"], min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]),
                                 Parameter("extrusion multiplier", "extrusion_multiplier", "-", value=persistence["settings"]["extrusion_multiplier"], min_max=[0.01, 2]),
                                 Parameter("retraction speed", "retraction_speed", "mm/s", value=persistence["settings"]["retraction_speed"], min_max=[1, persistence["settings"]["speed_travel"]])])

        parameter_values_for_comments = TestInfo("retraction distance vs printing speed", "09", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("retraction distance", "retraction_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 4.0, number_of_test_structures).tolist(), min_max=[0, 20]),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s", "{:.1f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.80*persistence["settings"]["speed_printing"], 1.75*persistence["settings"]["speed_printing"], number_of_substructures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "10":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "track_height_raft", "mm", value=persistence["settings"]["track_height_raft"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("first-layer track width", "track_width_raft", "mm", value=persistence["settings"]["track_width_raft"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", value=persistence["settings"]["speed_printing_raft"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("track height", "track_height", "mm", value=persistence["settings"]["track_height"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("track width", "track_width", "mm", value=persistence["settings"]["track_width"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("printing speed", "speed_printing", "mm/s", value=persistence["settings"]["speed_printing"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("extrusion temperature", "temperature_extruder", "degC", value=persistence["settings"]["temperature_extruder"], min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]),
                                 Parameter("extrusion multiplier", "extrusion_multiplier", "-", value=persistence["settings"]["extrusion_multiplier"], min_max=[0.01, 2]),
                                 Parameter("retraction speed", "retraction_speed", "mm/s", value=persistence["settings"]["retraction_speed"], min_max=[1, persistence["settings"]["speed_travel"]])])

        parameter_values_for_comments = TestInfo("retraction distance", "10", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("retraction distance", "retraction_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 4.0, number_of_test_structures).tolist(), min_max=[0, 20]),
                                                 parameter_two=Parameter(None, None, None),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "11":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "track_height_raft", "mm", value=persistence["settings"]["track_height_raft"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("first-layer track width", "track_width_raft", "mm", value=persistence["settings"]["track_width_raft"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", value=persistence["settings"]["speed_printing_raft"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("track height", "track_height", "mm", value=persistence["settings"]["track_height"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("track width", "track_width", "mm", value=persistence["settings"]["track_width"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("printing speed", "speed_printing", "mm/s", value=persistence["settings"]["speed_printing"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("extrusion temperature", "temperature_extruder", "degC", value=persistence["settings"]["temperature_extruder"], min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]),
                                 Parameter("extrusion multiplier", "extrusion_multiplier", "-", value=persistence["settings"]["extrusion_multiplier"], min_max=[0.01, 2])])

        parameter_values_for_comments = TestInfo("retraction distance vs retraction speed", "11", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=4, raft=True,
                                                 parameter_one=Parameter("retraction distance", "retraction_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 4.0, number_of_test_structures).tolist(), min_max=[0, 20]),
                                                 parameter_two=Parameter("retraction speed", "retraction_speed", "mm/s", "{:.1f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.75*persistence["settings"]["retraction_speed"], 1.25*persistence["settings"]["retraction_speed"], number_of_substructures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "12": #TODO
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "track_height_raft", "mm", value=persistence["settings"]["track_height_raft"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("first-layer track width", "track_width_raft", "mm", value=persistence["settings"]["track_width_raft"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", value=persistence["settings"]["speed_printing_raft"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("track height", "track_height", "mm", value=persistence["settings"]["track_height"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("track width", "track_width", "mm", value=persistence["settings"]["track_width"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("printing speed", "speed_printing", "mm/s", value=persistence["settings"]["speed_printing"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("extrusion temperature", "temperature_extruder", "degC", value=persistence["settings"]["temperature_extruder"], min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]),
                                 Parameter("extrusion multiplier", "extrusion_multiplier", "-", value=persistence["settings"]["extrusion_multiplier"], min_max=[0.01, 2])])

        parameter_values_for_comments = TestInfo("retraction-restart distance vs coasting distance", "12", number_of_layers=1, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("retraction-restart distance", "retraction_restart_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 1.0, number_of_test_structures).tolist(), min_max=[0, 5]),
                                                 parameter_two=Parameter("coasting distance", "coasting_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 1.0, number_of_test_structures).tolist(), min_max=[0, 5]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "13":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "track_height_raft", "mm", value=persistence["settings"]["track_height_raft"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("first-layer track width", "track_width_raft", "mm", value=persistence["settings"]["track_width_raft"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", value=persistence["settings"]["speed_printing_raft"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("track height", "track_height", "mm", value=persistence["settings"]["track_height"], min_max=[0.1*nozzle_size_id, nozzle_size_id]),
                                 Parameter("track width", "track_width", "mm", value=persistence["settings"]["track_width"], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id]),
                                 Parameter("printing speed", "speed_printing", "mm/s", value=persistence["settings"]["speed_printing"], min_max=[1, persistence["settings"]["speed_travel"]]),
                                 Parameter("extrusion temperature", "temperature_extruder", "degC", value=persistence["settings"]["temperature_extruder"], min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]]),
                                 Parameter("extrusion multiplier", "extrusion_multiplier", "-", value=persistence["settings"]["extrusion_multiplier"], min_max=[0.01, 2]),
                                 Parameter("retraction distance", "retraction_distance", "mm", value=persistence["settings"]["retraction_distance"], min_max=[0, 30]),
                                 Parameter("retraction speed", "retraction_speed", "mm/s", value=persistence["settings"]["retraction_speed"], min_max=[1, 200]),
                                 Parameter("bridging part cooling", "bridging_part_cooling", "%", value=persistence["settings"]["bridging_part_cooling"], min_max=[0, 100])])

        parameter_values_for_comments = TestInfo("bridging extrusion multiplier vs bridging printing speed", "13", number_of_layers=8, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("bridging extrusion multiplier", "bridging_extrusion_multiplier", "-", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(1.0, 2.0, number_of_test_structures).tolist(), min_max=[0.01, 2]),
                                                 parameter_two=Parameter("bridging printing speed", "bridging_speed_printing","mm/s", "{:.1f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.75*persistence["settings"]["speed_printing"], 1.5*persistence["settings"]["speed_printing"], number_of_substructures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters)

    return parameter_values_for_comments


def get_comment(parameter_values_for_comments: TestInfo):
    comment = ""
    for parameter, order_number in zip(parameter_values_for_comments.other_parameters, range(len(parameter_values_for_comments.other_parameters))):
        if hasattr(parameter, "values"):
            if parameter.values is not None:
                if parameter.values != []:
                    comment_to_add = str(
                        "; --- {}: {} {}".format(parameter.name, parameter.precision, parameter.units)).format(parameter.values)
            else:
                comment_to_add = str("; --- {} was not tested".format(parameter.name))
            if order_number == len(parameter_values_for_comments.other_parameters) - 1:
                comment += comment_to_add
            else:
                comment += comment_to_add + "\n"

    return comment