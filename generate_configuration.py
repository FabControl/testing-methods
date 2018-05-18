import re
from collections import OrderedDict
from Globals import persistence as persistence
from CLI_helpers import exclusive_write
import json
import datetime
from conversion_dictionary import Slicer, Param, Params

slicer = str(persistence["session"]["slicer"]).lower()

persistence_flat = dict(persistence["settings"], **persistence["machine"]["nozzle"])
persistence_flat["material_name"] = persistence["material"]["name"]
persistence_flat["density_rt"] = persistence["material"]["density_rt"]


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
    except TypeError:
        return value


def read_ini(path: str, output_type: object = OrderedDict):
    """
    Parses an ini file and returns an ordered dictionary with parameters as keys.
    Dict item contains a value and a percentage flag.
    :rtype: OrderedDict
    :param path: path to the ini file to read
    :param output_type:
    :return: returns an ordered dict
    """
    with open(path, mode='r') as file:
        config_string = file.read()
        config = re.findall(r'(.+) = ([^%\n]*)(%)?', config_string)
        file.close()

    dictionary = OrderedDict() if output_type == OrderedDict else {}
    for x in config:
        dictionary[x[0]] = {"value": numeral_eval(x[1])}
        dictionary[x[0]]["percentage"] = True if "%" in x else False

    return dictionary


def assemble_ini(dictionary: OrderedDict):
    """
    Accepts an OrderedDict object, and writes it line by line by iterating through the OrderedDict.
    :param dictionary: read_ini()
    :return:
    :rtype: str
    """
    outstring = ""
    outstring += "# Created with Mass Portal Material Testing Suite\n"

    for key, values in dictionary.items():
        value = values["value"]
        percentage = values["percentage"]
        line_start = "{0} = {1}".format(key, str(value) if value is not None else "")
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
    output = "{0}_{1}_{2}_{3}.{4}".format(persistence["material"]["manufacturer"],
                                          persistence["material"]["name"],
                                          "{:.2f}".format(persistence["material"]["size_od"]).replace(".", "-"),
                                          "{:.0f} um".format(persistence["machine"]["nozzle"]["size_id"] * 1000).replace(".", "-"),
                                          extension)
    return output.replace(' ', '_')


params = Params("conversion.json")
defaults = read_ini("config.ini", output_type=dict)
for key, value in defaults.items():
    defaults[key] = value["value"]
    del key, value
params.populate(defaults, auto=True)
params.populate(persistence_flat, auto=True)


if "prusa" in slicer.lower():
    """
    Writes a Prusa Slic3r config
    """
    settings = persistence["settings"]
    material = persistence["material"]
    session = persistence["session"]

    configuration = read_ini("config.ini")

    for item in configuration:
        param = params.get(item, mode="prusa")
        if param is not None:
            configuration[item]["value"] = param.prusa.value

    exclusive_write(output_name("ini"), assemble_ini(configuration))

elif slicer == "simplify3d":
    import xml.etree.ElementTree as ET

    tree = ET.parse('simplify_config.fff')
    root = tree.getroot()
    root.attrib["name"] = "{0} {1} {2} for {3} um nozzle".format(persistence["material"]["manufacturer"],
                                                                 persistence["material"]["name"],
                                                                 str(persistence["material"]["size_od"]).format("{:.2f}"),
                                                                 str(persistence["machine"]["nozzle"]["size_id"]*1000))
    root.attrib["version"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for param in params.parameters:
        if param.simplify3d.parameter is not None:
            element = root.find(param.simplify3d.parameter)
            if element is None:
                element = root.find("extruder").find(param.simplify3d.parameter)
            if "temperature" in param.parameter:
                temp_controllers = root.findall("temperatureController")
                for controller in temp_controllers:
                    if controller.attrib["name"] == param.simplify3d.parameter:
                        setpoints = controller.findall("setpoint")
                        if len(setpoints) > 1:
                            if param.parameter == "temperature_extruder":
                                element = setpoints[-1]
                            else:
                                element = setpoints[0]
                        else:
                            element = controller.find("setpoint")
                        element.attrib["temperature"] = str(param.simplify3d.value)
                continue
            if param.parameter == "ventilator_part_cooling":
                element = root.find("fanSpeed").findall("setpoint")[-1]
                element.attrib["speed"] = str(param.simplify3d.value)
                continue
            if element is not None:
                if element.text is not None:
                    element.text = str(numeral_eval(param.simplify3d.value))
                elif param.parameter == "":
                    element.attrib = str(numeral_eval(param.simplify3d.value))

    tree.write(output_name("fff"), xml_declaration=True, encoding="utf-8")
    print("{} succesfully written".format(output_name("fff")))

