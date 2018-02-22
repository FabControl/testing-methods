from ast import literal_eval
from os import system, name
import re


def evaluate(input):
    """
    Evaluates a given input string and outputs either an int, float, list or tuple.
    :param input:
    :return:
    """
    try:
        output = literal_eval(input)
    except:
        output = input

    if output == "":
        return None
    else:
        return output


def clear():
    """
    Clears the terminal screen. OS sensitive.
    :return:
    """
    system('cls' if name == 'nt' else 'clear')


def extruded_filament(path):
    """
    Takes a path to a gcode and returns a sum of all E values.
    :param path:
    :return:
    """
    with open(path) as gcode:
        gcode = gcode.read()

    extrusion_values = re.findall(r'(?<=E)[0-9.-]+(?=\s)', gcode)

    total_extrusion = 0
    for value in extrusion_values:
        try:
            total_extrusion = total_extrusion + float(value)
        except:
            total_extrusion = total_extrusion + literal_eval(value)

    return round(total_extrusion)
