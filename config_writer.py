import re
from collections import OrderedDict
from Globals import import_json_dict as json
from CLI_helpers import exclusive_write


def numeral_eval(value):
    """
    Attempts to parse int and float values. Leaves the other values as they are
    :param value:
    :return:
    """
    try:
        try:
            return int(value)
        except ValueError:
            return float(value)
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


"""
Writes a Prusa Slic3r config
"""
settings = json["settings"]
material = json["material"]
configuration = read_ini("config.ini")
configuration["bed_temperature"]["value"] = settings["temperature_printbed"]
configuration["cooling"]["value"] = 1 if settings["part_cooling"] != 0 else 0
configuration["fan_always_on"]["value"] = 1 if settings["part_cooling"] != 0 else 0
configuration["extrusion_width"]["value"] = settings["path_width"]
configuration["extrusion_multiplier"]["value"] = settings["extrusion_multiplier"]
configuration["first_layer_bed_temperature"]["value"] = settings["temperature_printbed_raft"]
configuration["first_layer_extrusion_width"]["value"] = settings["path_width_raft"]
configuration["first_layer_height"]["value"] = settings["path_height_raft"]
configuration["first_layer_speed"]["value"] = settings["speed_printing_raft"]
configuration["first_layer_temperature"]["value"] = settings["temperature_extruder_raft"]
configuration["layer_height"]["value"] = settings["path_height"]
configuration["nozzle_diameter"]["value"] = json["machine"]["nozzle"]["size_id"]
configuration["temperature"]["value"] = settings["temperature_extruder"]
configuration["retract_restart_extra"]["value"] = settings["retraction_restart_distance"]
configuration["retract_length"]["value"] = settings["retraction_distance"]
configuration["perimeter_speed"]["value"] = settings["speed_printing"]
configuration["solid_infill_speed"]["value"] = settings["speed_printing"]
configuration["filament_diameter"]["value"] = material["size_od"]
output_name = "%s_%s_%s_%s.ini" % (material["manufacturer"], material["name"],
                                   str(material["size_od"]).format("%.2f").replace(".", "-"),
                                   str(json["machine"]["nozzle"]["size_id"]).format("%.1f").replace(".", "-"))

exclusive_write(output_name, assemble_ini(configuration))
