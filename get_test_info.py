from Definitions import *
import numpy as np

number_of_substructures=4
number_of_test_structures=7


def get_test_info(persistence):
    nozzle_size_id = persistence["machine"]["temperature_controllers"]["extruder"]["nozzle"]["size_id"]

    other_parameters = []
    if persistence["machine"]["temperature_controllers"]["chamber"]["chamber_heatable"]:
        other_parameters.append(Parameter("chamber temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_chamber_setpoint"] if "temperature_chamber_setpoint" in persistence["settings"] else None))
    if persistence["machine"]["temperature_controllers"]["printbed"]["printbed_heatable"]:
        other_parameters.append(Parameter("printbed temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_printbed_setpoint"] if "temperature_printbed_setpoint" in persistence["settings"] else None))
        other_parameters.append(Parameter("printbed coating", "", "{}", value=persistence["machine"]["temperature_controllers"]["printbed"]["coating"]))
    if persistence["machine"]["temperature_controllers"]["chamber"]["ventilator_exit"]:
        other_parameters.append(Parameter("exit ventilation power", "%", "{:.0f}", value=persistence["settings"]["ventilator_exit_setpoint"] if "ventilator_exit_setpoint" in persistence["settings"] else None))
    if persistence["machine"]["temperature_controllers"]["extruder"]["part_cooling"]:
        other_parameters.append(Parameter("part cooling", "%", "{:.0f}", value=persistence["settings"]["part_cooling_setpoint"]))

    other_parameters.extend([Parameter("first-layer extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder_raft"]),
                             Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"])])

    if persistence["session"]["min_max_parameter_one"] != []:
        values_parameter_one = np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1],number_of_test_structures).tolist()
    else:
        values_parameter_one = []

    if persistence["session"]["test_number"] == "01":
        parameter_values_for_comments = TestInfo("first-layer track height vs first-layer printing speed", "01", number_of_layers=1, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=False,
                                                 parameter_one=Parameter("first-layer track height", "mm", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id*_ for _ in get_minmax_track_height_raft_coef(nozzle_size_id, number_of_test_structures)]),
                                                 parameter_two=Parameter("first-layer printing speed", "mm/s", "{:.1f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0],persistence["session"]["min_max_parameter_two"][-1],number_of_substructures).tolist()),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "02":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                 Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"])])

        parameter_values_for_comments = TestInfo("first-layer track width", "02", number_of_layers=1, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=False,
                                                 parameter_one=Parameter("first-layer track width", "mm", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id*_ for _ in get_minmax_track_width_raft_coef(nozzle_size_id, number_of_test_structures)]),
                                                 parameter_two=Parameter("first-layer printing speed", "mm/s", "{:.1f}",
                                                                         value=[persistence["settings"]["speed_printing_raft"]]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "03":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                 Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                 Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                 Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"]),
                                 Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                 Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"])])

        parameter_values_for_comments = TestInfo("extrusion temperature vs printing speed", "03", number_of_layers=2, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("extrusion temperature", "degC", "{:.0f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else get_minmax_temperature(persistence["settings"]["temperature_extruder_raft"], persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"], number_of_test_structures)),
                                                 parameter_two=Parameter("printing speed","mm/s","{:.1f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0],persistence["session"]["min_max_parameter_two"][-1],number_of_substructures).tolist()),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "04":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                 Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                 Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                 Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"]),
                                 Parameter("extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder"]),
                                 Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"])])

        parameter_values_for_comments = TestInfo("track height vs printing speed", "04", number_of_layers=2, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("track height","mm", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id*_ for _ in get_minmax_track_height_coef(nozzle_size_id, number_of_test_structures)]),
                                                 parameter_two=Parameter("printing speed", "mm/s", "{:.1f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0],persistence["session"]["min_max_parameter_two"][-1],number_of_substructures).tolist()),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "05":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                 Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                 Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                 Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"]),
                                 Parameter("extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder"]),
                                 Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                 Parameter("printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing"])])

        parameter_values_for_comments = TestInfo("track width", "05", number_of_layers=2, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("track width", "mm", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id * _ for _ in get_minmax_track_width_coef(nozzle_size_id, number_of_test_structures)]),
                                                 parameter_two=Parameter("printing speed", "mm/s", "{:.1f}",
                                                                         value=[persistence["settings"]["speed_printing"]]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "06":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                 Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                 Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                 Parameter("extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder"]),
                                 Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                 Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"])])

        parameter_values_for_comments = TestInfo("extrusion multiplier vs printing speed", "06", number_of_layers=2, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("extrusion multiplier", "-", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.80, 1.4, number_of_test_structures).tolist()),
                                                 parameter_two=Parameter("printing speed","mm/s","{:.1f}",
                                                                         value=[persistence["session"]["speed_printing"]]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "07":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                 Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                 Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                 Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"]),
                                 Parameter("extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder"]),
                                 Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                 Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"])])

        parameter_values_for_comments = TestInfo("printing speed", "07", number_of_layers=2, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("printing speed", "mm/s", "{:.1f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.80*persistence["settings"]["speed_printing"], 1.75*persistence["settings"]["speed_printing"],number_of_test_structures).tolist()),
                                                 parameter_two=Parameter(None, None, None, value=[]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "08":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                 Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                 Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                 Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                 Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"]),
                                 Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"]),
                                 Parameter("printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing"])])

        parameter_values_for_comments = TestInfo("extrusion temperature vs retraction distance", "08", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("extrusion temperature", "degC", "{:.1f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(persistence["settings"]["temperature_extruder"]-5, persistence["settings"]["temperature_extruder"]+5, number_of_test_structures).tolist()),
                                                 parameter_two=Parameter("retraction distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.0, 4.0, number_of_substructures).tolist()),
                                                 parameter_three=Parameter("retraction speed", "mm/s", "{:.1f}",
                                                                         value=persistence["session"]["min_max_parameter_three"] if persistence["session"]["min_max_parameter_three"] != [] else [60, 120]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "09":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                 Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                 Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                 Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                 Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"]),
                                 Parameter("extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder"]),
                                 Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"]),
                                 Parameter("retraction speed", "mm/s", "{:.1f}", value=persistence["settings"]["retraction_speed"])])

        parameter_values_for_comments = TestInfo("retraction distance vs printing speed", "09", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("retraction distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 4.0, number_of_test_structures).tolist()),
                                                 parameter_two=Parameter("printing speed", "mm/s", "{:.1f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.80*persistence["settings"]["speed_printing"], 1.75*persistence["settings"]["speed_printing"], number_of_substructures).tolist()),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "10":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                 Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                 Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                 Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                 Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"]),
                                 Parameter("printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing"]),
                                 Parameter("extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder"]),
                                 Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"]),
                                 Parameter("retraction speed", "mm/s", "{:.1f}", value=persistence["settings"]["retraction_speed"])])

        parameter_values_for_comments = TestInfo("retraction distance", "10", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("retraction distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 4.0, number_of_test_structures).tolist()),
                                                 parameter_two=Parameter(None, None, None),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "11":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                 Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                 Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                 Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                 Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"]),
                                 Parameter("printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing"]),
                                 Parameter("extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder"]),
                                 Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"])])

        parameter_values_for_comments = TestInfo("retraction distance vs retraction speed", "11", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("retraction distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 4.0, number_of_test_structures).tolist()),
                                                 parameter_two=Parameter("retraction speed", "mm/s", "{:.1f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.75*persistence["settings"]["retraction_speed"], 1.25*persistence["settings"]["retraction_speed"], number_of_substructures).tolist()),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "12": #TODO
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                 Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                 Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                 Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                 Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"]),
                                 Parameter("printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing"]),
                                 Parameter("extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder"]),
                                 Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"])])

        parameter_values_for_comments = TestInfo("retraction-restart distance vs coasting distance", "12", number_of_layers=1, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("retraction-restart distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 1.0, number_of_test_structures).tolist()),
                                                 parameter_two=Parameter("coasting distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 1.0, number_of_test_structures).tolist()),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "13":
        other_parameters.pop()
        other_parameters.extend([Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                 Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                 Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                 Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                 Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"]),
                                 Parameter("printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing"]),
                                 Parameter("extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder"]),
                                 Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"]),
                                 Parameter("retraction distance", "mm", "{:.3f}", value=persistence["settings"]["retraction_distance"]),
                                 Parameter("retraction speed", "mm/s", "{:.1f}", value=persistence["settings"]["retraction_speed"]),
                                 Parameter("bridging part cooling", "%", "{:.0f}", value=persistence["settings"]["bridging_part_cooling"])])

        parameter_values_for_comments = TestInfo("bridging extrusion multiplier vs bridging printing speed", "13", number_of_layers=8, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("bridging extrusion multiplier", "-", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(1.0, 2.0, number_of_test_structures).tolist()),
                                                 parameter_two=Parameter("bridging printing speed", "mm/s", "{:.1f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.75*persistence["settings"]["speed_printing"], 1.5*persistence["settings"]["speed_printing"], number_of_substructures).tolist()),
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