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
    hint_active_testable = hint_active_generic + ". Perform the corresponding test to fine-tune this value" # when a testable parameter has to be put in by a user
    hint_inactive_testable = "This value was determined in the previous test(s) and cannot be changed"

    temperature_chamber_setpoint = Parameter("chamber temperature", "temperature_chamber_setpoint", "degC", "{:.0f}",
                                             value=persistence["settings"]["temperature_chamber_setpoint"] if "temperature_chamber_setpoint" in persistence["settings"] else None,
                                             min_max=[30, persistence["machine"]["temperature_controllers"]["chamber"]["temperature_max"]],
                                             hint_active=hint_active_generic)

    part_cooling_setpoint = Parameter("part cooling", "part_cooling_setpoint", "%", "{:.0f}",
                                      value=persistence["settings"]["part_cooling_setpoint"],
                                      min_max=[0,100],
                                      hint_active="Set part cooling. Active part cooling is required when printing using high deposition rates or when printing fine details")

    nozzle_size_id = persistence["machine"]["temperature_controllers"]["extruder"]["nozzle"]["size_id"]

    # should work well with old sessions, that does not contain 'min_extrusion_temperature' key
    material_avg_temp = persistence['material'].get('min_extrusion_temperature')
    if material_avg_temp is not None:
        material_avg_temp = (material_avg_temp + persistence['material'].get('max_extrusion_temperature')) / 2
    raft_temp = persistence["settings"]["temperature_extruder_raft"]
    temperature_extruder_raft = Parameter("first-layer extrusion temperature", "temperature_extruder_raft", "degC", "{:.0f}",
                                          value=material_avg_temp if material_avg_temp is not None and (raft_temp is None or raft_temp < 30) else raft_temp,
                                          min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]],
                                          hint_active=hint_active_generic)
    track_height_raft = Parameter("first-layer track height", "track_height_raft", "mm", "{:.2f}",
                                  value=persistence["settings"]["track_height_raft"],
                                  min_max=[0.1*nozzle_size_id, nozzle_size_id],
                                  hint_active=hint_active_testable)
    track_width_raft = Parameter("first-layer track width", "track_width_raft", "mm", "{:.2f}",
                                 value=persistence["settings"]["track_width_raft"],
                                 min_max=[0.5*nozzle_size_id, 2*nozzle_size_id],
                                 hint_active="The default value is equal to the nozzle inner diameter, but you can perform the corresponding test to fine-tune this value")
    speed_printing_raft = Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", "{:.0f}",
                                    value=persistence["settings"]["speed_printing_raft"],
                                    min_max=[1, persistence["settings"]["speed_travel"]],
                                    hint_active=hint_active_testable,
                                    hint_inactive = hint_inactive_testable)
    track_height = Parameter("track height", "track_height", "mm", "{:.2f}",
                             value=persistence["settings"]["track_height"],
                             min_max=[0.1*nozzle_size_id, nozzle_size_id],
                             hint_active=hint_active_generic+". This value will determine the resolution and surface quality of your print")
    track_width = Parameter("track width", "track_width", "mm", "{:.2f}",
                            value=persistence["settings"]["track_width"],
                            min_max=[0.5*nozzle_size_id, 2*nozzle_size_id],
                            hint_active="The default value is equal to the nozzle inner diameter, but you can perform the corresponding test to fine-tune this value")
    speed_printing = Parameter("printing speed", "speed_printing", "mm/s", "{:.0f}",
                               value=persistence["settings"]["speed_printing"],
                               min_max=[1, persistence["settings"]["speed_travel"]+100],
                               hint_active=hint_active_testable,
                               hint_inactive=hint_inactive_testable)

    extruder_temp = persistence["settings"]["temperature_extruder"]
    temperature_extruder = Parameter("extrusion temperature", "temperature_extruder", "degC", "{:.0f}",
                                     value=material_avg_temp if material_avg_temp is not None and (extruder_temp is None or extruder_temp < 30) else extruder_temp,
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
                                 hint_active=hint_active_testable,
                                 hint_inactive=hint_inactive_testable)
    bridging_part_cooling = Parameter("bridging part cooling", "bridging_part_cooling", "%", "{:.0f}",
                                      value=persistence["settings"]["bridging_part_cooling"] if persistence["settings"]["bridging_part_cooling"] != [] else 100,
                                      min_max=[0, 100],
                                      hint_active=hint_active_generic)
    offset_z = Parameter("z-offset", "offset_z", "mm", "{:.3f}",
                         value=persistence["settings"]["offset_z"] if persistence["settings"]["offset_z"] else 0,
                         min_max=[-2.5, 2.5],
                         hint_active=hint_active_generic)

    other_parameters = []

    if persistence["machine"]["extruder_type"] == "bowden":
        speed_printing_default = [30, 80]
        speed_printing_raft_default = [5, 20]
        retraction_distance_default = [0, 6]
        retraction_speed_default = [60, 120]
    else:
        speed_printing_default = [15, 40]
        speed_printing_raft_default = [5, 15]
        retraction_distance_default = [0, 3]
        retraction_speed_default = [40, 90]

    if persistence["machine"]["temperature_controllers"]["chamber"]["chamber_heatable"]:
        other_parameters.append(temperature_chamber_setpoint)
    if persistence["machine"]["temperature_controllers"]["printbed"]["printbed_heatable"]:
        temperature_printbed_setpoint = Parameter("print bed temperature", "temperature_printbed_setpoint", "degC", "{:.0f}",
                                                  value=persistence["settings"]["temperature_printbed_setpoint"] if "temperature_printbed_setpoint" in persistence["settings"] else None,
                                                  min_max=[0, persistence["machine"]["temperature_controllers"]["printbed"]["temperature_max"]],
                                                  hint_active=hint_active_generic)

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
                             track_width_raft,
                             offset_z])

    if persistence["session"]["min_max_parameter_one"] != []:
        values_parameter_one = np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1],number_of_test_structures).tolist()
    else:
        values_parameter_one = []

    if persistence["session"]["test_number"] == "00":
        other_parameters.pop()
        other_parameters = parameter_reorder_and_activate(other_parameters, inactives=["part_cooling_setpoint"])
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft])

        parameter_values_for_comments = TestInfo("z-offset", "00", number_of_layers=2, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=False,
                                                 parameter_one=Parameter("z-offset", "offset_z", "mm", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0, 0.45, number_of_test_structures).tolist(), min_max=[-2.5, 2.5]),
                                                 parameter_two=Parameter(None, None, None),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test is needed to find Z-offset value in case of non-level print bed or printbed coating.",
                                                 hint_valid="")

    elif persistence["session"]["test_number"] == "01":
        other_parameters = parameter_reorder_and_activate(other_parameters, inactives=["part_cooling_setpoint"])
        parameter_values_for_comments = TestInfo("first-layer track height vs first-layer printing speed", "01", number_of_layers=1, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=False,
                                                 parameter_one=Parameter("first-layer track height","track_height_raft", "mm", "{:.2f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id*_ for _ in get_minmax_track_height_raft_coef(nozzle_size_id, number_of_test_structures)],
                                                                         min_max=[0.1*nozzle_size_id, nozzle_size_id],
                                                                         hint_active="These seven values will be tested at four different <b>First-layer printing speeds</b> (see below). You can change the limiting values"),
                                                 parameter_two=Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", "{:.0f}",
                                                                         value=np.linspace(*get_speed(persistence["session"]["min_max_parameter_two"]),number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [0, 0] else np.linspace(*get_speed(speed_printing_raft_default), number_of_substructures).tolist(),
                                                                         min_max=[1, persistence["settings"]["speed_travel"] + 100],
                                                                         hint_active="Set the range to 5-15 mm/s for printing flexible materials, or to 10-30 mm/s for printing harder materials"),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test is needed to establish good first layer printing settings. A good first layer is essential to achieving good prints.",
                                                 hint_valid=""
                                                            "<ul><li>If the print does not adhere to the build platform, increase the <b>First-layer extrusion temperature</b> and re-run the test.</li>"
                                                            "<li>If this does not help, increase the <b>Printbed temperature</b> or apply different coating/spray on the build platform.</li>"
                                                            "<li>If you cannot find acceptable combination of two parameters, re-run the test with different <b>First-layer-extrusion-temperature</b> value and/or using different <b>Printing-speed</b> range.</li></ul>")

    elif persistence["session"]["test_number"] == "02":
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 speed_printing_raft])
        other_parameters = parameter_reorder_and_activate(other_parameters, inactives=["part_cooling_setpoint"])

        parameter_values_for_comments = TestInfo("first-layer track width", "02", number_of_layers=1, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=False,
                                                 parameter_one=Parameter("first-layer track width", "track_width_raft", "mm", "{:.2f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else [nozzle_size_id*_ for _ in get_minmax_track_width_raft_coef(nozzle_size_id, number_of_test_structures)],
                                                                         min_max=[0.5*nozzle_size_id, 2*nozzle_size_id],
                                                                         hint_active="These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values"),
                                                 parameter_two=Parameter("first-layer printing speed", "speed_printing_raft", "mm/s", "{:.0f}",
                                                                         value=[persistence["settings"]["speed_printing_raft"]], active=False, min_max=[1, persistence["settings"]["speed_travel"] + 100],
                                                                         hint_active=hint_inactive_testable),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test is needed to solve possible issues with adhesion between tracks if there are any. Good weld-together is essential to achieving good mechanical properties in any printed part."
                                                           "<br>Run it only if you see the voids in between the tracks in the previous test. By skipping this test, the <b>First-layer-track-width</b> value will be set to the <b>Nozzle inner diameter</b>",
                                                 hint_valid="")

    elif persistence["session"]["test_number"] == "03":
        if persistence["session"]["target"] == "aesthetics":
            hint_active = hint_active_generic + ". For your target it should be in the range 0.05-0.10 mm"
            track_height = 0.1
        elif persistence["session"]["target"] == "mechanical_strength":
            hint_active = hint_active_generic + ". For your target it should be in the range 0.20-0.25 mm"
            track_height = 0.2
        else:
            hint_active = hint_active_generic + ". For your target it should be in the range 0.10-0.35 mm"
            track_height = 0.25

        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 extrusion_multiplier,
                                 Parameter("track height", "track_height", "mm", "{:.2f}",
                                           value=persistence["settings"]["track_height"] or track_height,
                                           min_max=[0.1 * nozzle_size_id, nozzle_size_id],
                                           hint_active=hint_active + ". This value will determine the resolution and surface quality of your print"),
                                 track_width])
        parameter_values_for_comments = TestInfo("extrusion temperature vs printing speed", "03", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("extrusion temperature", "temperature_extruder", "degC", "{:.0f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else get_minmax_temperature(material_avg_temp if material_avg_temp is not None and (raft_temp is None or raft_temp < 30) else raft_temp, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"], number_of_test_structures),
                                                                         min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]],
                                                                         hint_active="These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values"),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s","{:.0f}",
                                                                         value=np.linspace(*get_speed(persistence["session"]["min_max_parameter_two"]),number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [0, 0] else np.linspace(*get_speed(speed_printing_default), number_of_substructures).tolist(),
                                                                         min_max=[1, persistence["settings"]["speed_travel"] + 100],
                                                                         hint_active="Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials"),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test helps you find a base temperature and printing speed. These will be optimized further in later tests. Since there can be different parameter combinations that work, but are not optimal for your intended target, this is an essential test.",
                                                 hint_valid="")

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
                                                                         value=np.linspace(*get_speed(persistence["session"]["min_max_parameter_two"]),number_of_substructures).tolist(), min_max=[1, persistence["settings"]["speed_travel"] + 100],
                                                                         hint_active="Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials"),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test is needed to find the limits of printing resolution (layer thickness).",
                                                 hint_valid="")

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
                                                                         value=[persistence["settings"]["speed_printing"]], active=False, min_max=[1, persistence["settings"]["speed_travel"] + 100],
                                                                         hint_active="Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials"),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test is needed to avoid gaps between tracks and find the limits of horizontal resolution with a given nozzle.",
                                                 hint_valid="")

    elif persistence["session"]["test_number"] == "06":
        other_parameters.pop()
        other_parameters.extend([track_height_raft,
                                 track_width_raft,
                                 speed_printing_raft,
                                 speed_printing,
                                 temperature_extruder,
                                 track_height,
                                 track_width])

        parameter_values_for_comments = TestInfo("extrusion multiplier vs printing speed", "06", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=1, raft=True,
                                                 parameter_one=Parameter("extrusion multiplier", "extrusion_multiplier", "-", "{:.3f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.80, 1.4, number_of_test_structures).tolist(),
                                                                         min_max=[0.01, 2],
                                                                         hint_active="These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values"),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s","{:.0f}",
                                                                         value=[persistence["settings"]["speed_printing"]],
                                                                         active=False,
                                                                         min_max=[1, persistence["settings"]["speed_travel"] + 100],
                                                                         hint_active="Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials"),
                                                 other_parameters=other_parameters,
                                                 hint_init="This is an additional test to avoid under-extrusion.",
                                                 hint_valid="")

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
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.80*persistence["settings"]["speed_printing"], 1.75*persistence["settings"]["speed_printing"],number_of_test_structures).tolist(),
                                                                         min_max=[1, persistence["settings"]["speed_travel"] + 100],
                                                                         hint_active="These seven values will be tested while all other processing parameters are constant. You can change the limiting values"),
                                                 parameter_two=Parameter(None, None, None, value=[]),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test is needed to arrive at the most optimal flow-rate.",
                                                 hint_valid="")

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
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(persistence["settings"]["temperature_extruder"]-5, persistence["settings"]["temperature_extruder"]+5, number_of_test_structures).tolist(),
                                                                         min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]],
                                                                         hint_active="These seven values will be tested at four different <b>Retraction distances</b> (see below). You can change the limiting values"),
                                                 parameter_two=Parameter("retraction distance", "retraction_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(retraction_distance_default[0], retraction_distance_default[1], number_of_substructures).tolist(),
                                                                         min_max=[0, 20],
                                                                         hint_active="Set the range of <b>Retraction distances</b> to be tested"),
                                                 parameter_three=Parameter("retraction speed", "retraction_speed", "mm/s", "{:.0f}",
                                                                           value=persistence["session"]["min_max_parameter_three"] if persistence["session"]["min_max_parameter_three"] != [] else retraction_speed_default,
                                                                           min_max=[1, persistence["settings"]["speed_travel"] + 100]),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test is needed to find reliable settings for retraction. The best combination of 3 parameters are determined simulataneously.",
                                                 hint_valid="")

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
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(retraction_distance_default[0], retraction_distance_default[1], number_of_test_structures).tolist(),
                                                                         min_max=[0, 20],
                                                                         hint_active="These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values"),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s", "{:.0f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.80*persistence["settings"]["speed_printing"], 1.75*persistence["settings"]["speed_printing"], number_of_substructures).tolist(),
                                                                         min_max=[1, persistence["settings"]["speed_travel"] + 100]),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test is needed to avoid stringing.",
                                                 hint_valid="")

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
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(retraction_distance_default[0], retraction_distance_default[1], number_of_test_structures).tolist(),
                                                                         min_max=[0, 20],
                                                                         hint_active="These seven values will be tested. You can change the limiting values"),
                                                 parameter_two=Parameter(None, None, None),
                                                 other_parameters=other_parameters,
                                                 hint_init="This is a core test which helps finding a working retraction distance under general conditions.",
                                                 hint_valid="")

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
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(retraction_distance_default[0], retraction_distance_default[1], number_of_test_structures).tolist(),
                                                                         min_max=[0, 20],
                                                                         hint_active="These seven values will be tested at four different <b>Retraction speeds</b> (see below). You can change the limiting values"),
                                                 parameter_two=Parameter("retraction speed", "retraction_speed", "mm/s", "{:.0f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(retraction_speed_default[0], retraction_speed_default[1],  number_of_substructures).tolist(),
                                                                         min_max=[1, persistence["settings"]["speed_travel"] + 100]),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test is needed to avoid stringing.",
                                                 hint_valid="")

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
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s", "{:.0f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0.80*persistence["settings"]["speed_printing"], 1.75*persistence["settings"]["speed_printing"], number_of_substructures).tolist(),
                                                                         min_max=[1, persistence["settings"]["speed_travel"] + 100]),
                                                 parameter_three=Parameter("coasting distance", "coasting_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_three"][0], persistence["session"]["min_max_parameter_three"][-1], 2).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0.0, 1.0, 2).tolist(), min_max=[0, 5]),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test is needed to find the best retraction restart distance and coasting settings.",
                                                 hint_valid="")

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
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] not in [[], [0,0]] else np.linspace(0.25*persistence["settings"]["speed_printing"], 0.75*persistence["settings"]["speed_printing"], number_of_substructures).tolist(), min_max=[1, 2*persistence["settings"]["speed_travel"]],
                                                                         hint_active="Set the range to 10-25 mm/s for printing flexible materials, or 15-35 mm/s for harder materials"),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test is needed to find the best bridging settings.",
                                                 hint_valid="")
        
    elif persistence["session"]["test_number"] == "14":
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
                                 retraction_speed])
        parameter_values_for_comments = TestInfo("support pattern spacing vs support contact distance", "14", number_of_layers=9, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("support pattern spacing", "support_pattern_spacing", "mm", "{:.2f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_one"][0], persistence["session"]["min_max_parameter_one"][-1], number_of_test_structures).tolist() if persistence["session"]["min_max_parameter_one"] != [] else np.linspace(0, 5, number_of_test_structures).tolist(),
                                                                         min_max=[0, 10],
                                                                         hint_active="These seven support spacing distances will be tested against four different support contact distances"),
                                                 parameter_two=Parameter("support contact distance", "support_contact_distance", "mm", "{:.3f}",
                                                                         value=np.linspace(persistence["session"]["min_max_parameter_two"][0], persistence["session"]["min_max_parameter_two"][-1], number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [] else np.linspace(0, 0.3, number_of_substructures).tolist(),
                                                                         min_max=[0, 3 * persistence["machine"]["temperature_controllers"]["extruder"]["nozzle"]["size_id"]],
                                                                         hint_active="0 mm is generally best for soluble materials. PrusaSlicer recommends 0.2 mm for detachable supports."),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test helps you find settings at which break-away support will perform the best.",
                                                 hint_valid="")

    elif persistence["session"]["test_number"] == "15":
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
                                 retraction_speed])
        parameter_values_for_comments = TestInfo("soluble support adhesion", "15", number_of_layers=3, number_of_test_structures=number_of_test_structures, number_of_substructures=number_of_substructures, raft=True,
                                                 parameter_one=Parameter("extrusion temperature", "temperature_extruder", "degC", "{:.0f}",
                                                                         value=values_parameter_one if persistence["session"]["min_max_parameter_one"] != [] else get_minmax_temperature(persistence["settings"]["temperature_extruder_raft"], persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"], number_of_test_structures),
                                                                         min_max=[30, persistence["machine"]["temperature_controllers"]["extruder"]["temperature_max"]],
                                                                         hint_active="These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values"),
                                                 parameter_two=Parameter("printing speed", "speed_printing", "mm/s","{:.0f}",
                                                                         value=np.linspace(*get_speed(persistence["session"]["min_max_parameter_two"]),number_of_substructures).tolist() if persistence["session"]["min_max_parameter_two"] != [0, 0] else np.linspace(*get_speed(speed_printing_default), number_of_substructures).tolist(),
                                                                         min_max=[1, persistence["settings"]["speed_travel"] + 100],
                                                                         hint_active="Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials"),
                                                 other_parameters=other_parameters,
                                                 hint_init="This test helps you find settings at which soluble material will adhere to base material.",
                                                 hint_valid="")

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
