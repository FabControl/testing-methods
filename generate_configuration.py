import re
from collections import OrderedDict
from Globals import import_json_dict as json_dict
from CLI_helpers import exclusive_write
import json
import datetime

slicer = str(json_dict["session"]["slicer"]).lower()


def numeral_eval(value):
    """
    Attempts to parse int and float values. Leaves the other values as they are
    :param value:
    :return:
    """
    try:
        return float(value) if not float(value).is_integer() else int(value)
    except ValueError:
        return value


def read_ini(path):
    """
    Parses an ini file and returns an ordered dictionary with parameters as keys.
    Dict item contains a value and a percentage flag.
    :param path:
    :return:
    """
    with open(path, mode='r') as file:
        file = file.read()
        config = re.findall(r'(.+) = ([^%\n]*)(%)?', file)
        del file

    dictionary = OrderedDict()
    for x in config:
        dictionary[x[0]] = {"value": numeral_eval(x[1])}
        dictionary[x[0]]["percentage"] = True if "%" in x else False

    config = dictionary
    del dictionary

    return config


def assemble_ini(dictionary: OrderedDict):
    """
    Accepts an OrderedDict object, and writes it line by line by iterating through the OrderedDict.
    :param dictionary:
    :return:
    """
    outstring = ""
    outstring += "# Created with Mass Portal Material Testing Suite\n"

    for key, values in dictionary.items():
        value = values["value"]
        percentage = values["percentage"]
        line_start = "%s = %s" % (key, str(value) if value is not None else "")
        line_end = "%\n" if percentage else "\n"
        outstring += line_start + line_end

    return outstring


def output_name(extension: str):
    """
    Creates a filename based on material manufacturer, name, outer diameter and nozzle diameter.
    Accepts a file extension as an input parameter.
    :param extension:
    :return:
    """
    output = "{0}_{1}_{2}_{3}.{4}".format(json_dict["material"]["manufacturer"],
                                          json_dict["material"]["name"],
                                          str(json_dict["material"]["size_od"]).format("{:.2f}").replace(".", "-"),
                                          str(json_dict["machine"]["nozzle"]["size_id"]).format("{:.1f}").replace(".", "-"),
                                          extension)
    return output


with open("relational_dict.json") as file:
    relational_dict = json.load(file)

if slicer == "prusa":
    """
    Writes a Prusa Slic3r config
    """
    settings = json_dict["settings"]
    material = json_dict["material"]
    session = json_dict["session"]

    configuration = read_ini("config.ini")

    configuration["bed_temperature"]["value"] = numeral_eval(settings["temperature_printbed"])
    configuration["cooling"]["value"] = 1 if settings["ventilator_part_cooling"] != 0 else 0
    configuration["fan_always_on"]["value"] = 1 if settings["ventilator_part_cooling"] != 0 else 0
    configuration["extrusion_width"]["value"] = numeral_eval(settings["path_width"])
    configuration["top_infill_extrusion_width"]["value"] = numeral_eval(1.05*settings["path_width"])
    configuration["infill_extrusion_width"]["value"] = numeral_eval(settings["path_width"])
    configuration["solid_infill_extrusion_width"]["value"] = numeral_eval(settings["path_width"])
    configuration["perimeter_extrusion_width"]["value"] = numeral_eval(settings["path_width"])
    configuration["external_perimeter_extrusion_width"]["value"] = numeral_eval(settings["path_width"])
    configuration["extrusion_multiplier"]["value"] = numeral_eval(settings["extrusion_multiplier"])
    configuration["first_layer_bed_temperature"]["value"] = numeral_eval(settings["temperature_printbed_raft"])
    configuration["first_layer_extrusion_width"]["value"] = numeral_eval(settings["path_width_raft"])
    configuration["first_layer_height"]["value"] = numeral_eval(settings["path_height_raft"])
    configuration["first_layer_speed"]["value"] = numeral_eval(settings["speed_printing_raft"])
    configuration["first_layer_temperature"]["value"] = numeral_eval(settings["temperature_extruder_raft"])
    configuration["layer_height"]["value"] = numeral_eval(settings["path_height"])
    configuration["nozzle_diameter"]["value"] = numeral_eval(json_dict["machine"]["nozzle"]["size_id"])
    configuration["temperature"]["value"] = numeral_eval(settings["temperature_extruder"])
    configuration["retract_restart_extra"]["value"] = numeral_eval(settings["retraction_restart_distance"])
    configuration["retract_length"]["value"] = numeral_eval(settings["retraction_distance"])
    configuration["retract_speed"]["value"] = numeral_eval(settings["retraction_speed"])
    configuration["deretract_speed"]["value"] = numeral_eval(settings["retraction_speed"])
    configuration["perimeter_speed"]["value"] = numeral_eval(0.95*settings["speed_printing"])
    configuration["external_perimeter_speed"]["value"] = numeral_eval(0.90*settings["speed_printing"])
    configuration["infill_speed"]["value"] = numeral_eval(0.90*settings["speed_printing"])
    configuration["solid_infill_speed"]["value"] = numeral_eval(0.90*settings["speed_printing"])
    configuration["top_solid_infill_speed"]["value"] = numeral_eval(0.90*settings["speed_printing"])
    configuration["small_perimeter_speed"]["value"] = numeral_eval(0.33*settings["speed_printing"])
    configuration["filament_diameter"]["value"] = numeral_eval(material["size_od"])
    configuration["max_volumetric_speed"]["value"] = numeral_eval(session["previous_tests"][-1]["selected_volumetric_flow_rate_value"]) # TODO is not recognized by slicer under filament settings - > advanced
    configuration["max_print_speed"]["value"] = max(numeral_eval(settings["speed_printing"]),numeral_eval(settings["speed_printing_raft"]))
    configuration["min_print_speed"]["value"] = min(numeral_eval(settings["speed_printing"]),numeral_eval(settings["speed_printing_raft"]))
    configuration["max_layer_height"]["value"] = max(numeral_eval(settings["path_height"]),numeral_eval(settings["path_height_raft"]))
    configuration["min_layer_height"]["value"] = min(numeral_eval(settings["path_height"]),numeral_eval(settings["path_height_raft"]))
    configuration["support_material_threshold"]["value"] = numeral_eval(settings["critical_overhang_angle"])
    configuration["external_perimeters_first"]["value"] = 0 if numeral_eval(settings["critical_overhang_angle"]) < 45 else 1
    configuration["infill_first"]["value"] = 1 if numeral_eval(settings["critical_overhang_angle"]) < 45 else 0

    exclusive_write(output_name("ini"), assemble_ini(configuration))

elif slicer == "simplify3d":
    import xml.etree.ElementTree as ET

    tree = ET.parse('simplify_config.fff')
    root = tree.getroot()
    root.attrib["name"] = "{0} {1} {2} for {3} mm nozzle".format(json_dict["material"]["manufacturer"],
                                                                 json_dict["material"]["name"],
                                                                 str(json_dict["material"]["size_od"]).format("{:.2f}"),
                                                                 str(json_dict["machine"]["nozzle"]["size_id"]).format("{:.2f}"))
    root.attrib["version"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for key, value in relational_dict.items():
        foo = root.find(relational_dict[key]["simplify3d"]["parameter"])
        if foo is None:
            foo = root.find("extruder").find(relational_dict[key]["simplify3d"]["parameter"])
        if "temperature" in key:
            temp_controllers = root.findall("temperatureController")
            for controller in temp_controllers:
                if controller.attrib["name"] == relational_dict[key]["simplify3d"]["parameter"]:
                    foo = controller.find("setpoint")
        if key == "part_cooling":
            foo = root.find("fanSpeed").findall("setpoint")[-1]

        if foo is not None:
            if value["simplify3d"]["modifier"] != "":
                x = json_dict["settings"][key]
                if value["simplify3d"]["parent_parameter"] != "":
                    y = json_dict["settings"][value["simplify3d"]["parent_parameter"]]
                new_val = numeral_eval(eval(value["simplify3d"]["modifier"]))
            elif key == "size_id":
                new_val = numeral_eval(json_dict["machine"]["nozzle"]["size_id"])
            else:
                new_val = numeral_eval(json_dict["settings"][key])
            if foo.text is not None:
                foo.text = str(new_val)
            else:
                if key == "part_cooling":
                    foo.attrib["speed"] = str(new_val)
                else:
                    foo.attrib["temperature"] = str(new_val)
    tree.write(output_name("fff"), xml_declaration=True, encoding="utf-8")
    print("{} succesfully written".format(output_name("fff")))
