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
        if len(min_max) == 1:
            return [min_max[0], min_max[0]]
        else:
            return [min_max[0], min_max[1]]


def get_test_info(persistence):
    hint_active_generic = "Set this value to proceed" # when a non-testable parameter has to be put in by a user
    hint_active_testable = hint_active_generic + ". Perform the corresponding test if you want to fine-tune this value" # when a testable parameter has to be put in by a user
    hint_inactive_testable = "This value was determined in the previous test(s) and cannot be changed"

    temperature_chamber_setpoint = Parameter("chamber temperature", "temperature_chamber_setpoint", "degC", "{:.0f}",
                                             value=persistence["settings"]["temperature_chamber_setpoint"] if "temperature_chamber_setpoint" in persistence["settings"] else None,
                                             min_max=[30, persistence["machine"]["temperature_controllers"]["chamber"]["temperature_max"]])
    temperature_printbed_setpoint = Parameter("print bed temperature", "temperature_printbed_setpoint", "degC", "{:.0f}",
                                              value=persistence["settings"]["temperature_printbed_setpoint"] if "temperature_printbed_setpoint" in persistence["settings"] else None,
                                              min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]])
    part_cooling_setpoint = Parameter("part cooling", "part_cooling_setpoint", "%", "{:.0f}",
                                      value=persistence["settings"]["part_cooling_setpoint"],
                                      min_max=[0,100],
                                      hint_active="Set part cooling. Active part cooling is required when printing using high deposition rates or when printing fine details")

    nozzle_size_id = persistence["machine"]["temperature_controllers"]["extruder"]["nozzle"]["size_id"]

    temperature_extruder_raft = Parameter("first-layer extrusion temperature", "temperature_extruder_raft", "degC", "{:.0f}",
                                          value=persistence["settings"]["temperature_extruder_raft"],
                                          min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]],
                                          hint_active=hint_active_generic)

    track_height_raft = Parameter("first-layer track height", "track_height_raft", "mm", "{:.2f}",
                                  value=persistence["settings"]["track_height_raft"],
                                  min_max=[0.1 * nozzle_size_id, nozzle_size_id],
                                  hint_active=hint_active_testable)
    track_width_raft = Parameter("first-layer track width", "track_width_raft", "mm", "{:.2f}",
                                 value=persistence["settings"]["track_width_raft"],
                                 min_max=[0.5 * nozzle_size_id, 2 * nozzle_size_id],
                                 hint_active="For this test this value is equal to the nozzle inner diameter, but, if needed, it can be tested in a separate test")
    speed_printing_raft = Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", "{:.0f}",
                                    value=persistence["settings"]["speed_printing_raft"],
                                    min_max=[1, persistence["settings"]["speed_travel"]],
                                    hint_active=hint_active_testable,
                                    hint_inactive = hint_inactive_testable)
    track_height = Parameter("track height", "track_height", "mm", "{:.2f}",
                             value=persistence["settings"]["track_height"],
                             min_max=[0.1 * nozzle_size_id, nozzle_size_id],
                             hint_active=hint_active_generic+". This value will determine the resolution and surface quality of your print")
    track_width = Parameter("track width", "track_width", "mm", "{:.2f}",
                            value=persistence["settings"]["track_width"],
                            min_max=[0.5 * nozzle_size_id, 2 * nozzle_size_id],
                            hint_active="For this test this value is equal to the nozzle inner diameter, but, if needed, it can be tested in a separate test")
    speed_printing = Parameter("printing speed", "speed_printing", "mm/s", "{:.0f}",
                               value=persistence["settings"]["speed_printing"],
                               min_max=[1, persistence["settings"]["speed_travel"]],
                               hint_active=hint_active_testable,
                               hint_inactive=hint_inactive_testable)
    temperature_extruder = Parameter("extrusion temperature", "temperature_extruder", "degC", "{:.0f}",
                                     value=persistence["settings"]["temperature_extruder"],
                                     min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]],
                                     hint_active=hint_active_testable)
    extrusion_multiplier = Parameter("extrusion multiplier", "extrusion_multiplier", "-", "{:.3f}",
                                     value=persistence["settings"]["extrusion_multiplier"],
                                     min_max=[0.01, 2],
                                     hint_active="For this test this value is equal to unity, but, if needed, it can be tested in a separate test")
    retraction_distance = Parameter("retraction distance", "retraction_distance", "mm", "{:.3f}",
                                    value=persistence["settings"]["retraction_distance"],
                                    min_max=[0, 30],
                                    hint_active=hint_active_testable)
    retraction_speed = Parameter("retraction speed", "retraction_speed", "mm/s", "{:.0f}",
                                 value=persistence["settings"]["retraction_speed"],
                                 min_max=[1, 200],
                                 hint_active=hint_active_testable)
    bridging_part_cooling = Parameter("bridging part cooling", "bridging_part_cooling", "%", "{:.0f}",
                                      value=persistence["settings"]["bridging_part_cooling"] if persistence["settings"]["bridging_part_cooling"] != [] else 100,
                                      min_max=[0, 100],
                                      hint_active=hint_active_generic)

    other_parameters = []
    if persistence["machine"]["temperature_controllers"]["chamber"]["chamber_heatable"]:
        other_parameters.append(temperature_chamber_setpoint)
    if persistence["machine"]["temperature_controllers"]["printbed"]["printbed_heatable"]:
        other_parameters.append(temperature_printbed_setpoint)
        #other_parameters.append(Parameter("print bed coating", "", "{}", value=persistence["machine"]["temperature_controllers"]["printbed"]["coating"]))
    try:
        if persistence["machine"]["temperature_controllers"]["chamber"]["ventilator_exit"]:
            other_parameters.append(Parameter("exit ventilation power", "ventilator_exit_setpoint", "%", "{:.0f}", value=persistence["settings"]["ventilator_exit_setpoint"] if "ventilator_exit_setpoint" in persistence["settings"] else None))
    except:
        pass

    if persistence["machine"]["temperature_controllers"]["extruder"]["part_cooling"]:
        other_parameters.append(part_cooling_setpoint)

    other_parameters.extend([temperature_extruder_raft,
                             track_width_raft])

    if persistence["session"]["min_max_parameter_one"] != []:
        values_parameter_one = np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1],number_of_test_structures).tolist()
    else:
        values_parameter_one = []

    if persistence["session"]["test_number"] == "01":
        other_parameters = parameter_reorder_and_activate(other_parameters, inactives=["part_cooling_setpoint"])
        parameter_values_for_comments = TestInfo("first-layer track height vs first-layer printing speed", "01", number_of_layers=1, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=False,
                                                 parameter_one=Parameter("first-layer track height","track_height_raft", "mm", "{:.2f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id*_ for _ in get_minmax_track_height_raft_coef(nozzle_size_id, number_of_test_structures)], min_max=[0.1*nozzle_size_id, nozzle_size_id],
                                                                         hint_active="These seven values will be tested at four different <b>First-layer printing speeds</b> (see below). You can change the limiting values"),
                                                 parameter_two=Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", "{:.0f}",
                                                                         value=np.linspace(*get_speed(persistence["session"]["min_max_parameter_two"]),number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [0, 0] else np.linspace(*get_speed([10, 30]), number_of_substructures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]],
                                                                         hint_active="Set the values in the range of 5-15 mm/s for printing flexible materials; for harder materials, you can go up to 10-30 mm/s"),
                                                 other_parameters=other_parameters,
                                                 hint_init="In this test two parameters will be optimized:<br><b>First-layer track height</b> and <b>First-layer printing speed</b>",
                                                 hint_valid="Inspect the printed test structure.<small><br>Select one combination of parameters which results in the best test structure.<br>If the print does not adhere to the build platform, increase the <b>First-layer extrusion temperature</b> and re-run the test.<br>If this does not help, increase the <b>Printbed temperature</b> or apply different coating/spray on the build platform.<br>If you cannot find acceptable combination of two parameters, re-run the test with different <b>First-layer-extrusion-temperature</b> value and/or using different <b>Printing-speed</b> range.</small>")

    elif persistence["session"]["test_number"] == "02":
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 speed_printing_raft])
        other_parameters = parameter_reorder_and_activate(other_parameters, inactives=["part_cooling_setpoint"])

        parameter_values_for_comments = TestInfo("first-layer track width", "02", number_of_layers=1, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=False,
                                                 parameter_one=Parameter("first-layer track width", "track_width_raft", "mm", "{:.2f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id*_ for _ in get_minmax_track_width_raft_coef(nozzle_size_id, number_of_test_structures)], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id],
                                                                         hint_active="These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values"),
                                                 parameter_two=Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", "{:.0f}",
                                                                         value=[persistence["settings"]["speed_printing_raft"]], active=False, min_max=[1, persistence["settings"]["speed_travel"]],
                                                                         hint_active="This value was determined in the previous test and cannot be changed"),
                                                 other_parameters=other_parameters,
                                                 hint_init="This is an optional test in which one parameter will be determined:<br><b>First-layer track width</b>.<br>Run it only if you see the voids in between the tracks in the previous test. By skipping this test, the <b>First-layer-track-width</b> value will be set to the <b>Nozzle inner diameter</b>",
                                                 hint_valid="Inspect the printed test structure.<br>Select one first-layer track width value which results in the best test structure")

    elif persistence["session"]["test_number"] == "03":
        if persistence["session"]["target"] == "aesthetics":
            hint_active = "Set the desired track height. For your target it should be in the range 0.05-0.10 mm"
            track_height = 0.1
        elif persistence["session"]["target"] == "mechanical_strength":
            hint_active = "Set the desired track height. For your target it should be in the range 0.20-0.25 mm"
            track_height = 0.2
        else:
            hint_active = "Set the desired track height. For your target it should be in the range 0.10-0.35 mm"
            track_height = 0.25

        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 extrusion_multiplier,
                                 Parameter("track height", "track_height", "mm", "{:.2f}",
                                           value=persistence["settings"]["track_height"],
                                           min_max=[0.1 * nozzle_size_id, nozzle_size_id],
                                           hint_active=hint_active + ". This value will determine the resolution and surface quality of your print"),
                                 track_width])

        other_parameters = parameter_reorder_and_activate(other_parameters)
        parameter_values_for_comments = TestInfo("extrusion temperature vs printing speed", "03", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("extrusion temperature", "temperature_extruder", "degC", "{:.0f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else get_minmax_temperature(persistence["settings"]["temperature_extruder_raft"], persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"], number_of_test_structures), min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]],
                                                                         hint_active="These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values"),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s","{:.0f}",
                                                                         value=np.linspace(*get_speed(persistence["session"]["min_max_parameter_two"]),number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [0, 0] else np.linspace(*get_speed([20, 60]), number_of_substructures).tolist(),  min_max=[1, persistence["settings"]["speed_travel"]],
                                                                         hint_active="Set the values in the range of 20-50 mm/s for printing flexible materials; for harder materials, you can go up to 30-70 mm/s"),
                                                 other_parameters=other_parameters,
                                                 hint_init="In this test two parameters will be determined:<br><b>Extrusion temperature</b> and <b>Printing speed</b>.",
                                                 hint_valid="Inspect the printed test structure.<br>Select one combination of parameters which results in the best test structure.")

    elif persistence["session"]["test_number"] == "04":
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 extrusion_multiplier,
                                 temperature_extruder,
                                 track_width])

        parameter_values_for_comments = TestInfo("track height vs printing speed", "04", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("track height", "track_height", "mm", "{:.2f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id*_ for _ in get_minmax_track_height_coef(nozzle_size_id, number_of_test_structures)], min_max=[0.1*nozzle_size_id, nozzle_size_id],
                                                                         hint_active="These seven values will be tested at four <b>Printing speeds</b>. You can change the limiting values"),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s", "{:.0f}",
                                                                         value=np.linspace(*get_speed(persistence["session"]["min_max_parameter_two"]),number_of_substructures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]],
                                                                         hint_active="This value was determined in the previous test and cannot be changed"),
                                                 other_parameters=other_parameters,
                                                 hint_init="In this test one parameter will be determined:<br><b>Track height</b>.",
                                                 hint_valid="Inspect the printed test structure.<br>Select one track height value which results in the best test structure.")

    elif persistence["session"]["test_number"] == "05":
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 extrusion_multiplier,
                                 temperature_extruder,
                                 track_height,
                                 speed_printing])

        parameter_values_for_comments = TestInfo("track width", "05", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("track width", "track_width", "mm", "{:.2f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id * _ for _ in get_minmax_track_width_coef(nozzle_size_id, number_of_test_structures)], min_max=[0.5*nozzle_size_id, 2*nozzle_size_id],
                                                                         hint_active="These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values"),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s", "{:.0f}",
                                                                         value=[persistence["settings"]["speed_printing"]], active=False, min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters,
                                                 hint_init="In this test one parameter will be determined:<br><b>Track width</b>.",
                                                 hint_valid="Inspect the printed test structure.<br>Select one track width value which results in the best test structure.")

    elif persistence["session"]["test_number"] == "06":
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 temperature_extruder,
                                 track_height,
                                 track_width])

        parameter_values_for_comments = TestInfo("extrusion multiplier vs printing speed", "06", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("extrusion multiplier", "extrusion_multiplier", "-", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.80, 1.4, number_of_test_structures).tolist(), min_max=[0.01, 2],
                                                                         hint_active="These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values"),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s","{:.0f}",
                                                                         value=[persistence["settings"]["speed_printing"]], active=False, min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters,
                                                 hint_init="In this test one parameter will be determined:<br><b>Extrusion multiplier</b>.",
                                                 hint_valid="Inspect the printed test structure.<br>Select one extrusion multiplier value which results in the best test structure.")

    elif persistence["session"]["test_number"] == "07":
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 extrusion_multiplier,
                                 temperature_extruder,
                                 track_height,
                                 track_width])

        parameter_values_for_comments = TestInfo("printing speed", "07", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("printing speed", "speed_printing", "mm/s", "{:.0f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.80*persistence["settings"]["speed_printing"], 1.75*persistence["settings"]["speed_printing"],number_of_test_structures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]],
                                                                         hint_active="These seven values will be tested while all other processing parameters are constant. You can change the limiting values"),
                                                 parameter_two=Parameter(None, None, None, value=[]),
                                                 other_parameters=other_parameters,
                                                 hint_init="In this test one parameter will be determined:<br><b>Printing speed</b>.",
                                                 hint_valid="Inspect the printed test structure.<br>Select one printing speed value which results in the best test structure.")

    elif persistence["session"]["test_number"] == "08":
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 track_height,
                                 track_width,
                                 extrusion_multiplier,
                                 speed_printing])

        parameter_values_for_comments = TestInfo("extrusion temperature vs retraction distance", "08", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("extrusion temperature", "temperature_extruder", "degC", "{:.0f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(persistence["settings"]["temperature_extruder"]-5, persistence["settings"]["temperature_extruder"]+5, number_of_test_structures).tolist(), min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]],
                                                                         hint_active="These seven values will be tested at four different <b>Retraction distances</b> (see below). You can change the limiting values"),
                                                 parameter_two=Parameter("retraction distance", "retraction_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.0, 4.0, number_of_substructures).tolist(), min_max=[0, 20],
                                                                         hint_active="Set the values in the range of 1-8 mm for printing with a Bowden extruder; for a direct drive set 0-4 mm"),
                                                 parameter_three=Parameter("retraction speed", "retraction_speed", "mm/s", "{:.0f}",
                                                                         value=persistence["session"]["min_max_parameter_three"] if persistence["session"]["min_max_parameter_three"] != [] else [60, 120], min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters,
                                                 hint_init="In this test three parameters will be determined:<br><b>Extrusion temperature</b>, <b>Retraction distance</b>, and <b>Retraction speed</b>.",
                                                 hint_valid="Inspect the printed test structure.<br>Select one combination of parameters which results in the best test structure. Use slider to select the retraction speed.")

    elif persistence["session"]["test_number"] == "09":
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 track_height,
                                 track_width,
                                 temperature_extruder,
                                 extrusion_multiplier,
                                 retraction_speed])

        parameter_values_for_comments = TestInfo("retraction distance vs printing speed", "09", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("retraction distance", "retraction_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 4.0, number_of_test_structures).tolist(), min_max=[0, 20],
                                                                         hint_active="These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values"),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s", "{:.0f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.80*persistence["settings"]["speed_printing"], 1.75*persistence["settings"]["speed_printing"], number_of_substructures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters,
                                                 hint_init="In this test two parameters will be determined:<br><b>Retraction distance</b> and <b>Printing speed</b>.",
                                                 hint_valid="Inspect the printed test structure.<b>Select one combination of parameters which results in the best test structure.")

    elif persistence["session"]["test_number"] == "10":
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 track_height,
                                 track_width,
                                 speed_printing,
                                 temperature_extruder,
                                 extrusion_multiplier,
                                 retraction_speed])

        parameter_values_for_comments = TestInfo("retraction distance", "10", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("retraction distance", "retraction_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 4.0, number_of_test_structures).tolist(), min_max=[0, 20],
                                                                         hint_active="These seven values will be tested. You can change the limiting values"),
                                                 parameter_two=Parameter(None, None, None),
                                                 other_parameters=other_parameters,
                                                 hint_init = "In this test one parameter will be determined:<br><b>Retraction distance</b>.",
                                                 hint_valid="Inspect the printed test structure.<br>Select one retraction distance value which results in the best test structure.")

    elif persistence["session"]["test_number"] == "11":
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 track_height,
                                 track_width,
                                 speed_printing,
                                 temperature_extruder,
                                 extrusion_multiplier])

        parameter_values_for_comments = TestInfo("retraction distance vs retraction speed", "11", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=4, raft=True,
                                                 parameter_one=Parameter("retraction distance", "retraction_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 4.0, number_of_test_structures).tolist(), min_max=[0, 20],
                                                                         hint_active="These seven values will be tested at four different <b>Retraction speeds</b> (see below). You can change the limiting values"),
                                                 parameter_two=Parameter("retraction speed", "retraction_speed", "mm/s", "{:.0f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.75*persistence["settings"]["retraction_speed"], 1.25*persistence["settings"]["retraction_speed"], number_of_substructures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]]),
                                                 other_parameters=other_parameters,
                                                 hint_init="In this test two parameters will be determined:<br><b>Retraction distance</b> and <b>Retraction speed</b>.",
                                                 hint_valid = "Inspect the printed test structure.<br>Select one combination of parameters which results in the best test structure.")

    elif persistence["session"]["test_number"] == "12": #TODO
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 track_height,
                                 track_width,
                                 speed_printing,
                                 temperature_extruder,
                                 extrusion_multiplier])

        parameter_values_for_comments = TestInfo("retraction-restart distance vs coasting distance", "12", number_of_layers=1, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("retraction-restart distance", "retraction_restart_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 1.0, number_of_test_structures).tolist(), min_max=[0, 5]),
                                                 parameter_two=Parameter("coasting distance", "coasting_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 1.0, number_of_test_structures).tolist(), min_max=[0, 5]),
                                                 other_parameters=other_parameters)

    elif persistence["session"]["test_number"] == "13":
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 track_height,
                                 track_width,
                                 speed_printing,
                                 temperature_extruder,
                                 extrusion_multiplier,
                                 retraction_distance,
                                 retraction_speed,
                                 bridging_part_cooling])

        parameter_values_for_comments = TestInfo("bridging extrusion multiplier vs bridging printing speed", "13", number_of_layers=8, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("bridging extrusion multiplier", "bridging_extrusion_multiplier", "-", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(1.0, 2.0, number_of_test_structures).tolist(), min_max=[0.01, 2],
                                                                         hint_active="These seven values will be tested at four different <b>Bridging printing speeds</b> (see below). You can change the limiting values"),
                                                 parameter_two=Parameter("bridging printing speed", "bridging_speed_printing","mm/s", "{:.0f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.75*persistence["settings"]["speed_printing"], 1.5*persistence["settings"]["speed_printing"], number_of_substructures).tolist(), min_max=[1, persistence["settings"]["speed_travel"]],
                                                                         hint_active="Use the values in the range of 10-25 mm/s for printing flexible materials; for harder materials, you can go up to 15-35 mm/s"),
                                                 other_parameters=other_parameters,
                                                 hint_init="In this test two parameters will be determined:<br><b>Bridging extrusion multiplier</b> and <b>Bridging printing speed</b>.",
                                                 hint_valid = "Inspect the printed test structure.<br>Select one combination of parameters which results in the best test structure.")

    return parameter_values_for_comments


def get_comment(parameter_values_for_comments: TestInfo):
    comment = ""
    for parameter, order_number in zip(parameter_values_for_comments.other_parameters, range(len(parameter_values_for_comments.other_parameters))):
        if hasattr(parameter, "values"):
            if parameter.values is not None:
                if parameter.values != []:
                    comment_to_add = str("; --- {}: {} {}".format(parameter.name, parameter.precision, parameter.units)).format(parameter.values)
            else:
                comment_to_add = str("; --- {} was not tested".format(parameter.name))
            if order_number == len(parameter_values_for_comments.other_parameters) - 1:
                comment += comment_to_add
            else:
                comment += comment_to_add + "\n"

    return comment