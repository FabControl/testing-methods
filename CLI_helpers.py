from ast import literal_eval
from os import system, name, listdir, devnull
from paths import blender_path, slic3r_path, cwd, test_sample_path, gcode_folder
import re
import subprocess


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
    Clears the terminal screen. OS aware.
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
        print("{} successfully saved.".format(path))

    except:
        split = re.split(r'(\d{3}(?=\.))*(\.[0-9a-zA-Z]+?$)', path)
        path = list(filter(lambda x: str(x).startswith(split[0]), listdir()))[-1]
        split = re.split(r'(\d{3}(?=\.))*(\.[0-9a-zA-Z]+?$)', path)
        if split[1] is not None and int(split[1]) > 999 and limit:
            raise ValueError(
                '%s%s is likely overflowing and has reached 1000 or more instances.' % (split[0], split[2]))
        underscore = "_" if not split[0].endswith("_") else ""
        path = split[0] + underscore + str(int(split[1] if split[1] is not None else 0) + 1).zfill(3) + split[2]
        with open(path, "x") as file:
            file.write(output)
        print("{} successfully saved.".format(path))


def generate_gcode(orientation: str, count: int, rotation: float or int, file: str, config: str):
    """
    Creates a subprocesses of Blender and Slic3r in order to generate an ISO527 test specimen geometry and slice it with an appropriate
    Slic3r configuration file.
    :param orientation:
    :param count:
    :param rotation:
    :param file:
    :param config:
    :return:
    """
    output = cwd + gcode_folder + separator() + file.replace(".stl", ".gcode")
    geometry = cwd + test_sample_path + separator() + file
    subprocess.run([blender_path, "-b", "-P", str(cwd + "stl_modifier.py"), "--", orientation, str(count),
         str(rotation), cwd + test_sample_path + separator() + file, cwd + separator() + test_sample_path], stderr=open(devnull, 'wb'))
    subprocess.run([slic3r_path, "--load", config, "-o", output, "--dont-arrange", geometry])


def separator(input=None):
    """
    Takes an input value and separates it with an OS aware directory separator. Returns a separator if no input is given.
    :param input:
    :return:
    """
    if input is None:
        if name == "nt":
            return "\\"
        else:
            return "/"
    else:
        if name == "nt":
            return "\\{}\\".format(input)
        else:
            return "/{}/".format(input)



builtins_round = round


def round(input: float, depth: int = 3):
    """
    A wrapper for the built-in round function which handles the datatype casting in a more intuitive fashion.
    :param input:
    :param depth:
    :return:
    """
    return float(str(builtins_round(input, depth)))
