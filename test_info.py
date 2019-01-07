from Globals import Parameter, TestInfo
import numpy as np

number_of_substructures=4

def test_info(persistence):
    if persistence["session"]["test_name"] == "01":
        test_info = TestInfo("first-layer track height vs first-layer printing speed", number_of_layers=1, number_of_test_structures=7, number_of_substructures=number_of_substructures, raft=False,
                                parameter_one=Parameter("first-layer track height", "mm", "{:.3f}"),
                                parameter_two=Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=np.linspace(persistence["session"]["min_max_parameter_two"][0],persistence["session"]["min_max_parameter_two"][1],number_of_substructures).tolist()),
                                other_parameters=[Parameter("printbed temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_printbed"]),
                                                  Parameter("first-layer extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder_raft"]),
                                                  Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"])])
    elif persistence["session"]["test_name"] == "02":
        test_info = TestInfo("first-layer track width", number_of_layers=1, number_of_test_structures=7, number_of_substructures=1, raft=False,
                                parameter_one=Parameter("first-layer track width", "mm", "{:.3f}"),
                                parameter_two=Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                other_parameters=[Parameter("printbed temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_printbed"]),
                                                  Parameter("first-layer extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder_raft"]),
                                                  Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                                  Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"])])
    elif persistence["session"]["test_name"] == "03":
        test_info = TestInfo("extrusion temperature vs printing speed", number_of_layers=2, number_of_test_structures=7, number_of_substructures=number_of_substructures, raft=True,
                                parameter_one=Parameter("extrusion temperature", "degC", "{:.0f}"),
                                parameter_two=Parameter("printing speed","mm/s","{:.1f}",value=np.linspace(persistence["session"]["min_max_parameter_two"][0],persistence["session"]["min_max_parameter_two"][1],number_of_substructures).tolist()),
                                other_parameters=[Parameter("printbed temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_printbed"]),
                                                  Parameter("first-layer extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder_raft"]),
                                                  Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                                  Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                                  Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                                  Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                                  Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"])])
    elif persistence["session"]["test_name"] == "04":
        test_info = TestInfo("track height vs printing speed", number_of_layers=2, number_of_test_structures=7, number_of_substructures=number_of_substructures, raft=True,
                                parameter_one=Parameter("track height","mm", "{:.3f}"),
                                parameter_two=Parameter("printing speed", "mm/s", "{:.1f}"),
                                other_parameters=[Parameter("printbed temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_printbed"]),
                                                  Parameter("first-layer extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder_raft"]),
                                                  Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                                  Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                                  Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                                  Parameter("extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder"]),
                                                  Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"])])
    elif persistence["session"]["test_name"] == "05":
        test_info = TestInfo("track width", number_of_layers=2, number_of_test_structures=7, number_of_substructures=number_of_substructures, raft=True,
                                parameter_one=Parameter("track width", "mm", "{:.3f}"),
                                parameter_two=Parameter("printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing"]),
                                other_parameters=[Parameter("printbed temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_printbed"]),
                                                  Parameter("first-layer extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder_raft"]),
                                                  Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                                  Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                                  Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                                  Parameter("extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder"]),
                                                  Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                                  Parameter("printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing"])])
    elif persistence["session"]["test_name"] == "06":
        test_info = TestInfo("extrusion multiplier vs printing speed", number_of_layers=2, number_of_test_structures=7, number_of_substructures=number_of_substructures, raft=True,
                                parameter_one=Parameter("extrusion multiplier", "-", "{:.3f}",default_value=[0.80, 1.40]),
                                parameter_two=Parameter("printing speed","mm/s","{:.1f}"),
                                other_parameters=[Parameter("printbed temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_printbed"]),
                                                  Parameter("first-layer extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder_raft"]),
                                                  Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                                  Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                                  Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                                  Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                                  Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"])])
    elif persistence["session"]["test_name"] == "07":
        test_info = TestInfo("printing speed", number_of_layers=2, number_of_test_structures=7, number_of_substructures=1, raft=True,
                             parameter_one=Parameter("printing speed", "mm/s", "{:.1f}",default_value=[0.80, 1.75]),
                             parameter_two=Parameter(None, None, None),
                             other_parameters=[Parameter("printbed temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_printbed"]),
                                               Parameter("first-layer extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder_raft"]),
                                               Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                               Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                               Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                               Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                               Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"]),
                                               Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"])])
    elif persistence["session"]["test_name"] == "08":
        test_info = TestInfo("retraction distance", number_of_layers=3, number_of_test_structures=7, number_of_substructures=1, raft=True,
                                parameter_one=Parameter("retraction distance", "mm", "{:.3f}", default_value=[0.0, 4.0]),
                                parameter_two=Parameter(None, None, None),
                                other_parameters=[Parameter("printbed temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_printbed"]),
                                                  Parameter("first-layer extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder_raft"]),
                                                  Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                                  Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                                  Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                                  Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                                  Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"]),
                                                  Parameter("printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing"]),
                                                  Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"]),
                                                  Parameter("retraction speed", "mm/s", "{:.1f}", value=persistence["settings"]["retraction_speed"])])
    elif persistence["session"]["test_name"] == "09":
        test_info = TestInfo("retraction-restart distance vs coasting distance", number_of_layers=1, number_of_test_structures=7, number_of_substructures=number_of_substructures, raft=True,
                                parameter_one=Parameter("retraction-restart distance", "mm", "{:.3f}", default_value=[0.0, 1.0]),
                                parameter_two=Parameter("coasting distance", "mm", "{:.3f}", default_value=[0.0, 1.0]),
                                other_parameters=[Parameter("printbed temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_printbed"]),
                                                  Parameter("first-layer extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder_raft"]),
                                                  Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                                  Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                                  Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                                  Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                                  Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"]),
                                                  Parameter("printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing"]),
                                                  Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"])])
    elif persistence["session"]["test_name"] == "10":
        test_info = TestInfo("bridging extrusion-multiplier vs bridging printing speed", number_of_layers=8, number_of_test_structures=7, number_of_substructures=number_of_substructures, raft=True,
                                parameter_one=Parameter("bridging extrusion multiplier", "-", "{:.3f}",default_value=[1.0, 2.0]),
                                parameter_two=Parameter("bridging printing speed", "mm/s", "{:.1f}"),
                                other_parameters=[Parameter("printbed temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_printbed"]),
                                                  Parameter("first-layer extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder_raft"]),
                                                  Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                                  Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                                  Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                                  Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                                  Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"]),
                                                  Parameter("printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing"]),
                                                  Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"]),
                                                  Parameter("retraction distance", "mm", "{:.3f}", value=persistence["settings"]["retraction_distance"]),
                                                  Parameter("retraction speed", "mm/s", "{:.1f}", value=persistence["settings"]["retraction_speed"])])
    elif persistence["session"]["test_name"] == "11":
        test_info = TestInfo("extrusion temperature vs retraction distance", number_of_layers=3, number_of_test_structures=7, number_of_substructures=number_of_substructures, raft=True,
                                parameter_one=Parameter("extrusion temperature", "degC", "{:.1f}"),
                                parameter_two=Parameter("retraction distance", "mm", "{:.3f}"),
                                other_parameters=[Parameter("printbed temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_printbed"]),
                                                  Parameter("first-layer extrusion temperature", "degC", "{:.0f}", value=persistence["settings"]["temperature_extruder_raft"]),
                                                  Parameter("first-layer track height", "mm", "{:.3f}", value=persistence["settings"]["track_height_raft"]),
                                                  Parameter("first-layer track width", "mm", "{:.3f}", value=persistence["settings"]["track_width_raft"]),
                                                  Parameter("first-layer printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing_raft"]),
                                                  Parameter("track height", "mm", "{:.3f}", value=persistence["settings"]["track_height"]),
                                                  Parameter("track width", "mm", "{:.3f}", value=persistence["settings"]["track_width"]),
                                                  Parameter("printing speed", "mm/s", "{:.1f}", value=persistence["settings"]["speed_printing"]),
                                                  Parameter("extrusion multiplier", "-", "{:.3f}", value=persistence["settings"]["extrusion_multiplier"])])

    return test_info