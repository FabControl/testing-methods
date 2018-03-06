from ast import literal_eval
from os import system, name, listdir
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


def exclusive_write(path: str, output, limit=True):
    """
    Takes a path and output stream, attempts to write the stream to the path,
    if it exists, alters the path to either have a 3x zero padded number before the extension,
    or add padding and increase an existing number by 1.
    A boolean limit argument is used to prevent the file writing from overflowing and writing
    too many instances of a file.

    Used to prevent file overwriting.

    split[0] is the filename,
    split[1] is either a number or NoneType
    split[2] is a file extension
    :param path:
    :param output:
    :param limit:
    :return:
    """
    try:
        with open(path, "x") as file:
            file.write(output)
        print("%s successfully saved." % (path))

    except:
        split = re.split(r'(\d{3}(?=\.))*(\.[0-9a-zA-Z]+?$)', path)
        path = list(filter(lambda x: split[0] in x, listdir()))[-1]
        split = re.split(r'(\d{3}(?=\.))*(\.[0-9a-zA-Z]+?$)', path)
        underscore = "_" if not split[0].endswith("_") else ""
        path = split[0] + underscore + str(int(split[1] if split[1] is not None else 0) + 1).zfill(3) + split[2]
        with open(path, "x") as file:
            file.write(output)
        print("%s successfully saved." % (path))